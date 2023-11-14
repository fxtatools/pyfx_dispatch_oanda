"""Utility functions for module imports"""

import importlib
import os
import sys
from pathlib import Path
import stat
from tempfile import mkstemp
from textwrap import fill

from .paths import Pathname, expand_path


def gen_imports(dst_name, *,
                dst_file: Pathname = "__imports__.py",
                overwrite: bool = False,
                template="from {module_name} import {obj_name}"
                ):
    if dst_name in sys.modules:
        dst_m = sys.modules[dst_name]
    else:
        dst_m = importlib.import_module(dst_name, dst_name)

    dst_m_path = Path(dst_m.__file__)
    dst_m_dir = dst_m_path.parent

    out_file = Path(expand_path(dst_file, dst_m_dir))

    if out_file.exists() and not overwrite:
        raise RuntimeError("File exists", str(out_file.absolute()))

    handle, tmpf = mkstemp(prefix=".gen_imports_", dir=dst_m_dir, text=True)
    all = []
    with open(handle, "w") as stream:
        for m_file in sorted(dst_m_dir.glob("*.py"), key=lambda p: p.name):
            # FIXME alternate iter: for name in filter(match("*.py"), rstrip(line) for line in {{git grep -l '' <dir>}}.lines()) ...
            name = m_file.stem
            existing_names = []
            if "#" not in name and "__" not in name:
                src_m = importlib.import_module("." + name, dst_name)
                if hasattr(src_m, "__all__"):
                    names = getattr(src_m, "__all__")
                    for name in names:
                        if hasattr(src_m,  name):
                            if not hasattr(dst_m, name):
                                obj = getattr(src_m, name)
                                setattr(dst_m, name, obj)
                                existing_names.append(name)
                                text = template.format(obj_name=name, module_name=src_m.__name__)
                                print(text, file=stream)
                        else:
                            print("Name not found: %s in %s" % (name, src_m.__name__,))
                    all.extend(existing_names)
                else:
                    print("No __all__ in module " + src_m.__name__)

        all_text = fill(", ".join('"' + name + '"' for name in all), initial_indent="    ", subsequent_indent="    ")
        print("__all__ = (" + os.linesep + all_text + "," + os.linesep + ")", file=stream)


    if out_file.exists():
        out_file.unlink()
    tmp_path = Path(tmpf)
    tmp_path.rename(out_file)
    tmp_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)


__all__ = ("gen_imports",)
