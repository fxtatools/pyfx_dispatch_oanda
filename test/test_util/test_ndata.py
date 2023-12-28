
import os
import numpy as np
import pandas as pd
from pathlib import Path

from pyfx.dispatch.oanda.test import ComponentTest, run_tests
import pytest
from assertpy import assert_that

#
# The components to test
#
from pyfx.dispatch.oanda.util.ndata import collate_by_dtype, dataframe_from_npz, dataframe_to_npz, dataframe_to_npmap


@pytest.fixture
def collated_df() -> pd.DataFrame:
    df_idx = pd.date_range(end=pd.Timestamp("now"), periods=10, tz="UTC")
    df_dct = dict(
        i0=np.random.randint(0, 254, size=10),
        i1=np.random.randint(0, 254, size=10),
        u0=df_idx.to_numpy(dtype=np.uint64),
        u1=df_idx.to_numpy(dtype=np.uint64)[::-1],
        d0_nd=np.random.random_sample((10, 2,)).tolist(),
        d1_nd=np.random.random_sample((10, 2,)).tolist(),
        d0=np.random.random_sample(10),
        d1=np.random.random_sample(10),
    )
    df = pd.DataFrame(df_dct, index=df_idx, copy=False)
    df.index.name = "time"
    df.attrs["a"] = 1
    df.attrs["b"] = (2, 3, 4,)
    df.attrs["c"] = dict(enumerate(df.attrs["b"]))
    return df


@pytest.fixture
def uncollated_df(collated_df:  pd.DataFrame):
    #
    # returns a generally unaligned dataframe having a
    # random distribution of columns, for purpose of test
    #
    ordered_cols = list(collated_df.columns.copy())
    shuffled_cols = ordered_cols.copy()
    np.random.shuffle(shuffled_cols)
    #
    # Implementation note: For purpose of tests here,
    # using df.loc[:, c] not df[c]
    #
    # If using df[c] the output dataframe might be generally
    # equivalent to the input dataframe, perhaps as some
    # side effect of the method of column reference.
    #
    # This function should produce a dataframe with arbitarily
    # ordered columns, for purpose of tests.
    #
    df_dct = {c + "_uncol": collated_df.loc[:, c].to_numpy(copy=True) for c in shuffled_cols}
    df = pd.DataFrame(df_dct, index=collated_df.index, copy=True)
    # test for the testing framework
    assert df.shape == collated_df.shape
    #
    # ensure attrs and flags are retained
    #
    df.attrs = collated_df.attrs
    df.set_flags(allows_duplicate_labels=collated_df.flags.allows_duplicate_labels)
    return df


class TestNData(ComponentTest):

    def test_collate_ordered(self, collated_df: pd.DataFrame):
        #
        # test collation for a dataframe having initially dtype-ordered columns
        #
        recollated = collate_by_dtype(collated_df)
        assert_that(len(frozenset(recollated.columns))).is_equal_to(len(collated_df.columns))
        assert_that(recollated.shape).is_equal_to(collated_df.shape)
        assert_that(tuple(recollated.columns)).is_equal_to(tuple(collated_df.columns))

        dt_col = frozenset(collated_df.dtypes)
        dt_recol = frozenset(recollated.dtypes)
        assert_that(dt_col).is_equal_to(dt_recol)

        cols = tuple(collated_df.columns)
        col_data = {c: collated_df.loc[:, c].to_numpy(copy=True) for c in cols}
        recol_data = {c: recollated.loc[:, c].to_numpy(copy=True) for c in cols}
        for c in cols:
            assert_that((col_data[c] == recol_data[c]).all()).is_true()

    def test_collate_unordered(self, uncollated_df: pd.DataFrame):

        #
        # test collation for a dataframe derived from a random
        # distribution of columns
        #
        collated = collate_by_dtype(uncollated_df.copy(), copy=True)
        #
        # test metadata (attrs) of the re-collated dataframe
        #
        assert_that(collated.attrs).is_equal_to(uncollated_df.attrs)

        #
        # test shape of the re-collated dataframe
        #
        assert_that(collated.shape).is_equal_to(uncollated_df.shape)
        #
        # ensure non-duplication of columns
        #
        assert_that(len(frozenset(collated.columns))).is_equal_to(len(uncollated_df.columns))

        #
        # The folllowing assertion may represent partly a test for the testing framework.
        #
        # This appears to fail frequently under testing with pytest in vs code,
        # though not failing with direct eval under either pytest or ipython in
        # the console.
        #
        # The failure, at these times, may generally represent an equivalent
        # order of the un-collated dataframe columns and the re-collated
        # dataframe columns, with both having columns in essentially the
        # same order as the initial dataframe. This may represent a
        # well-ordered dataframe.
        #
        # Here, it would be expected that the un-collated dataframe columns would
        # have some randomly distributed order. This appears to be consistently
        # the case, with direct testing under pytest or ipython in the console.
        #
        # It's unclear as to how this differs with pytest under vscode. It may
        # represent a side-effect of code introduced for test orchecstration,
        # or a side-effect of some other feature of the testing environment.
        #
        # workaround: Skipping this part of the test, under vscode
        #
        if os.getenv("TERM_PROGRAM", None) != "vscode":
            assert_that(tuple(collated.columns)).is_not_equal_to(tuple(uncollated_df.columns))

        #
        # test for an equivalent set of dtypes
        #
        dt_uncol = tuple(uncollated_df.dtypes)
        dts_uncol = frozenset(dt_uncol)
        dt_col = tuple(collated.dtypes)
        dts_col = frozenset(dt_col)
        assert_that(dts_uncol).is_equal_to(dts_col)

        cols = tuple(collated.columns)

        #
        # ensure that the dataframe is actually collated by dtype
        #
        # this relies on the precondition that there are two columns
        # for each dtype, in the input data
        #
        ncols = len(cols)
        for n in range(0, ncols, 2):
            assert_that(dt_col[n]).is_equal_to(dt_col[n+1])

        #
        # ensure that the uncollated input data is aligned
        # as sufficient for equivalence test
        #
        left, right = uncollated_df.align(collated, axis=1, copy=False)
        #
        # test equivalence of the data in the respective columns,
        # by column name, for each of the uncollated (input) and
        # re-collated dataframes
        #
        # preconditions here would include that the previous processing
        # functions will not have not produced any duplicate columns from
        # the input data.
        #
        # In this test, the input data columns are all uniquely named.
        #
        uncol_data = {c: left.loc[:, c].to_numpy(copy=True) for c in cols}
        recol_data = {c: right.loc[:, c].to_numpy(copy=True) for c in cols}
        for c in cols:
            assert_that((uncol_data[c] == recol_data[c]).all()).is_true()

    #
    # tests for intermediate functionality in dataframe-to-npz
    #

    # utility functions

    def run_npmap_selftest(self, df: pd.DataFrame, collate: bool = False):
        npmap = dataframe_to_npmap(df, collate=collate)
        assert_that((npmap["__index__"] == df.index.to_numpy()).all()).is_true()
        colmap = npmap["__colmap__"]
        if collate:
            # this part of the tests is based on the structure of the
            # sample dataframes, each of which contains two columns of
            # the same dtype
            colmap = npmap["__colmap__"]
            assert_that(len(colmap)).is_equal_to(len(df.columns) / 2)
        else:
            assert_that(len(colmap)).is_equal_to(len(df.columns))
        return npmap

    def run_npmap_collating_selftest(self, df: pd.DataFrame):
        npmap = self.run_npmap_selftest(df, True)

    # test functions

    def test_npmap_collated_nocollate(self, collated_df: pd.DataFrame):
        self.run_npmap_selftest(collated_df)

    def test_npmap_uncollated_nocollate(self, uncollated_df):
        self.run_npmap_selftest(uncollated_df)

    def test_npmap_collated_collate(self, collated_df):
        self.run_npmap_collating_selftest(collated_df)

    def test_npmap_uncollated_collate(self, uncollated_df):
        self.run_npmap_collating_selftest(uncollated_df)

    #
    # utility functions for dataframe-to-npz read/write tests
    #

    def run_rw_selftest(self, sample_df: pd.DataFrame,
                        tmpdir: Path, collate: bool) -> pd.DataFrame:
        tmp_file: Path = tmpdir / "dataframe.npz"
        try:
            p = dataframe_to_npz(sample_df, tmp_file, overwrite=True, collate=collate)
            assert_that(str(p)).exists()
            assert_that(tmp_file.samefile(p)).is_true()

            in_df: pd.DataFrame = dataframe_from_npz(tmp_file)
            assert_that(in_df.shape).is_equal_to(sample_df.shape)
            assert_that(in_df.attrs).is_equal_to(sample_df.attrs)
            assert_that(in_df.index.name).is_equal_to(sample_df.index.name)

            return in_df
        finally:
            if os.path.exists(tmp_file):
                os.unlink(tmp_file)
            if os.path.exists(tmpdir):
                os.rmdir(tmpdir)

    def run_nocol_selftest(self, sample_df: pd.DataFrame, tmpdir):
        in_df = self.run_rw_selftest(sample_df, tmpdir, False)
        assert_that((in_df == sample_df).all().all()).is_true()
        assert_that(tuple(in_df.columns)).is_equal_to(tuple(sample_df.columns))
        return in_df

    #
    # dataframe-to-npz read/write tests
    #

    def run_collate_selftest(self, sample_df: pd.DataFrame, tmpdir):
        return self.run_rw_selftest(sample_df, tmpdir, True)

    def test_rw_collated_nocol(self, collated_df: pd.DataFrame, tmp_path: Path):
        # test uncollated write, read of an collated dataframe
        self.run_nocol_selftest(collated_df, tmp_path)

    def test_rw_uncollated_nocol(self, uncollated_df: pd.DataFrame, tmp_path: Path):
        # test uncollated write, read of an uncollated dataframe
        self.run_nocol_selftest(uncollated_df, tmp_path)

    def test_rw_collated_col(self, collated_df: pd.DataFrame, tmp_path: Path):
        # test collated write, read of an collated dataframe
        in_df = self.run_collate_selftest(collated_df, tmp_path)
        left, right = in_df.align(collated_df, axis=1, copy=False)
        assert_that((left == right).all().all()).is_true()

    def test_rw_uncollated_col(self, uncollated_df: pd.DataFrame, tmp_path: Path):
        # test collated write, read of an uncollated dataframe
        in_df = self.run_collate_selftest(uncollated_df, tmp_path)
        #
        # given a dataframe with randomly distributed, unaligned columns
        # the dataframe read from the npz file - as previouisly collated
        # under dataframe_to_npz() - should not be equal to the input
        # dataframe
        #
        assert_that((in_df == collated_df).all().all() != True).is_true()
        #
        # it's expected that the re-read dataframe will be equal to the
        # dataframe as collated under collate_by_dtype()
        #
        recol_df: pd.DataFrame = collate_by_dtype(uncollated_df)
        assert_that(tuple(in_df.columns)).is_equal_to(tuple(recol_df.columns))
        assert_that((in_df == recol_df).all().all()).is_true()


if __name__ == "__main__":
    run_tests(__file__)
