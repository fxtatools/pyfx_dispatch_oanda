"""Utilities for DataFrame serialization with numpy

Primary functions:
- dataframe_to_npz()
- dataframe_from_npz()
"""

import numpy as np
import os
import pandas as pd
from typing import Collection, Iterator, Mapping, Optional, TypedDict, Union
from itertools import chain

from pyfx.dispatch.oanda.util.paths import Pathname, expand_path


def _dtype_offsets(data: pd.DataFrame) -> Mapping[np.dtype, list[int]]:
    # utility function for collate_by_dtype
    #
    # return a mapping of {dtype: [column_offset...]} for each column in data
    #
    n = 0
    last_dt = None
    cols = tuple(data.columns)
    cols_dt = tuple(data.dtypes)

    cols_dtmap = dict(zip(cols, cols_dt))
    s_dtmap = dict(sorted(cols_dtmap.items(), key=lambda it: it[1]))
    # out_dtmap: Mapping[np.dtype, list[int]] = dict()

    inter_dtmap: Mapping[np.dtype, Mapping[int, int]] = dict()
    ## e.g
    # {int64: {4:0, 8:6}, uint64: {5: 5}}

    #
    # compile any mappings {dtype: {end: start}}
    # for dtypes in the input dataframe
    #
    for (c, dt,) in s_dtmap.items():
        colidx = cols.index(c)
        pre: Optional[dict[int, int]] = inter_dtmap.get(dt, None)
        if pre is None:
            inter_dtmap[dt] = {colidx: colidx}
        else:
            index_m1 = colidx - 1
            pre_start = pre.pop(index_m1, None)
            if pre_start is None:
                pre[colidx] = colidx
            else:
                pre[colidx] = pre_start
    #
    # re-sort values in each intermediate slice offset map,
    # discarding dtype keys for the intermediate data
    #
    sorted_dtmap = (dict(sorted(slices.items(), key=lambda elt: elt[0])) for slices in inter_dtmap.values())

    #
    # process the {end: start} slice maps from sorted_dtmap
    #
    # this should preserve the ordering of columns within each dtype column range
    # as well as the contiguous-adjusted ordering of columns within the dataframe
    #
    # firstly, parsing each range for offset/slice objects
    #
    offset_slices = (tuple(start if start == end else slice(start, end + 1) for end, start in slicemap.items()) for slicemap in sorted_dtmap)

    def parse_offset(elt: tuple[Union[int, slice]]):
        val = elt[0]
        return val if isinstance(val, int) else val.start
    # secondly, sorting the offset/slice map by original column offset
    return tuple(sorted(offset_slices, key=parse_offset))


def collate_by_dtype(data: pd.DataFrame, copy=False) -> pd.DataFrame:
    # Known Limitations
    #
    # - does not filter for multi-column labels when collating by dtype
    #
    collate_gen = (data.iloc[:, idx] for bounds in _dtype_offsets(data) for idx in bounds)
    df = pd.concat(list(collate_gen), copy=copy, axis=1)
    df.attrs = data.attrs
    df.set_flags(allows_duplicate_labels=data.flags.allows_duplicate_labels)
    return df


class NPMapLabels(TypedDict):
    #
    # utility type, in effect a data scheme for the npz file
    #
    columns_label: str  # = "__columns__"
    index_label: str  # = "__index__"
    index_name_label: str  # = "__index_name__"
    attrs_label: str  # = "__attrs__"
    colmap_label: str  # = "__colmap__"


def make_npmap_labels(columns_label: str = "__columns__",
                      index_label: str = "__index__",
                      index_name_label: str = "__index_name__",
                      attrs_label: str = "__attrs__",
                      colmap_label: str = "__colmap__"
                      ) -> NPMapLabels:
    #
    # constructor for an NPMapLabels TypedDict
    #
    return NPMapLabels(columns_label=columns_label,
                       index_label=index_label,
                       index_name_label=index_name_label,
                       attrs_label=attrs_label,
                       colmap_label=colmap_label
                       )


def dataframe_to_npmap(data: pd.DataFrame,
                       collate: bool = False,
                       labels: Optional[NPMapLabels] = None
                       ) -> Mapping[str, Collection]:
    # utility function used in dataframe_to_npz()

    schema = labels or make_npmap_labels()
    odata = collate_by_dtype(data, copy=False) if collate else data
    # odata = data  # fallback : no collation
    attrs = data.attrs
    colmap = {}
    cols = tuple(odata.columns)
    idx = data.index
    npidx = idx.to_numpy(copy=False)
    npmap = {
        schema['columns_label']: cols,
        schema['index_label']: npidx,
        schema['index_name_label']: np.array((idx.name,), dtype="O", copy=False),
        schema['attrs_label']: np.array(tuple(attrs.items()), dtype="O", copy=False)
    }
    if collate:
        def sort_key(elt: Union[int, slice]):
            return elt if isinstance(elt, int) else elt.stop
        idxmap: Iterator[Union[int, slice]] = chain.from_iterable(_dtype_offsets(odata))
    else:
        idxmap: Iterator[int] = range(0, len(cols))
    for n, idxsl in enumerate(idxmap):
        iname = str(n)
        colmap[iname] = idxsl
        npmap[iname] = odata.iloc[:, idxsl].to_numpy(copy=False)
    npmap[schema['colmap_label']] = np.array(tuple(colmap.items()), dtype="O", copy=False)
    return npmap


def dataframe_to_npz(data: pd.DataFrame,
                     dest: Pathname,
                     overwrite: bool = False,
                     collate: bool = False,
                     labels: Optional[NPMapLabels] = None,
                     ) -> Pathname:

    #
    # Implementation Notes
    #
    # % The collate option
    #
    # - Developed in a hypothesis about possible I/O latency for array data
    #   columns of contguous or non-contiguous dtype, for write in numpy
    #   savez_compressed() and read in numpy.load()
    #
    # - Under some limited testing, this option may not appear to contribute
    #   substantially for any reduction in I/O latency
    #
    # - As such, this may represent mostly a cosmetic feature
    #
    # - With a non-falsey value for the collate arg, any dataframe loaded
    #   from the subsequent npz file may have a column ordering different
    #   than that of the original dataframe
    #
    # - This function has been tested, to some extent, to ensure data
    #   integrity, as independent of either the 'collate' option or the
    #   order of columns in initial dataframe
    #
    # % Filename Handling
    #
    # If the dest filename does not end in ".npz", np.savez_compressed()
    # will add an "npz" suffix to the filename
    #
    # Furthermore, np.load() will not add any suffix to the filename.
    #
    # The following function develops a workaround for this feature,
    # in an effort to ensure that the filename as provided will be the
    # name of the file at the return of this function. The following
    # approach has some known limitations however. This function will
    # fail if an intermediate <name>.npz file exists, whether or not
    # the <name>.npz filename is the same as the provided destination
    # filename.
    #
    # This failsafe behavior may be overidden by providing an 'overwrite'
    # arg with a truthy value, in which case any existing intermediate
    # file and destination file will be overwritten.
    #
    # Additional Limitations:
    #
    # - This does not provide any backup-file semanitcs
    #
    filename = expand_path(dest)
    stem, type = os.path.splitext(filename)
    npz_file = filename if type == ".npz" else stem + ".npz"
    if os.path.exists(npz_file) and not overwrite:
        raise OSError("Intermediate file exists", npz_file)
    elif os.path.exists(filename) and not overwrite:
        raise OSError("File exists", filename)
    # write the data map
    npmap = dataframe_to_npmap(data, collate=collate, labels=labels)
    np.savez_compressed(npz_file, **npmap)
    # more filename handling
    if npz_file != filename:
        os.rename(npz_file, filename)
    return filename


def dataframe_from_npz(file: Pathname,
                       labels: Optional[NPMapLabels] = None,
                       mmap_mode: Optional[str] = None,
                       encoding: str = 'ASCII') -> pd.DataFrame:

    # encoding: note limitations denoted in the np.load/np.savez_compressed docs

    filename = expand_path(file)
    npmap = np.load(filename, mmap_mode=mmap_mode,
                    encoding=encoding,
                    allow_pickle=True,
                    fix_imports=True)
    schema = labels or make_npmap_labels()
    cols_label = schema['columns_label']
    index_label = schema['index_label']
    index_name_label = schema['index_name_label']
    attrs_label = schema['attrs_label']
    colmap_label = schema['colmap_label']

    colmap_data = dict(npmap[colmap_label])
    cols = npmap[cols_label]

    index_name_data = npmap.get(index_name_label, None)
    index_name = None if index_name_data is None else index_name_data[0]

    index_data = npmap[index_label]

    datamap = {}
    for label, cocoord in colmap_data.items():
        # slice each individual column from single-column
        # or contiguous npdata, to produce a structure for
        # pd.DataFrame init
        npdata = npmap[label]

        if isinstance(cocoord, int):
            colndata = cols[cocoord]
            colname = colndata if isinstance(colndata, str) else tuple(colndata)
            datamap[colname] = npdata
        else:
            # contiguous npdata
            for n, idx in enumerate(range(cocoord.start, cocoord.stop)):
                colndata = cols[idx]
                colname = colndata if isinstance(colndata, str) else tuple(colndata)
                datamap[colname] = npdata[:, n]

    df = pd.DataFrame(
        datamap,
        index=index_data,
        copy=False,
    )
    if index_name is not None:
        df.index.name = index_name
        if index_name in colmap_data:
            df[index_name] = df.index

    attrs = npmap[attrs_label]
    df.attrs.update(attrs)
    return df
