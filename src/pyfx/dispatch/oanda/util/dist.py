## dist.py

from importlib_metadata import distribution, Distribution, PackageNotFoundError
from importlib.util import find_spec
from importlib.machinery import NamespaceLoader, SourceFileLoader, ExtensionFileLoader
import os
import sys
from typing import Union

from .paths import Pathname
from .naming import ModuleLike, ModuleType


def module_distribution(module: ModuleLike) -> Distribution:
    """Return the `importlib_metadata.Distribution` providing a module.

    The `module` may be provided as a string, a module object, or generally
    any object providing a `__name__` property denoting a module name.

    Raises `importlib_metadata.PackageNotFoundError` if no distribution
    can be located for the module.
    """
    name = module if isinstance(module, str) else module.__name__
    try:
        return distribution(name)
    except PackageNotFoundError:
        basepkg = module.rsplit(".", maxsplit=1)[0]
        if basepkg == module:
            raise
        else:
            return module_distribution(basepkg)

def class_distribution(cls: type) -> Distribution:
    """Return the `importlib_metadata.Distribution` for the
    distribution providing a class definition.

    The `cls` may be specified as any object providing a
    `__module__` property denoting a module name string.

    Raises `ValueError` if the class' module cannot be determined,
    generally as when the class' `__module__` property holds the
    value `None`.

    Raises `importlib_metadata.PackageNotFoundError` if no distribution
    can be located for the class' module.
    """
    if __debug__:
        if not isinstance(cls, type):
            raise AssertionError("Arg is not a class", cls)
    m = cls.__module__
    if m:
        return module_distribution(m)
    else:
        raise ValueError("Class does not provide a __module__", cls)


def module_dir(module: ModuleLike) -> Pathname:
    """Return the pathname of the directory containing a module's code

    Raises ValueError if the module denotes a namesapace module provided
    from more than one directory under the Python environment.

    If the module is provided as a string and the named module is not
    present in `sys.modules`, the pathname will be determined using importlib.
    """
    if isinstance(module, str):
        if module in sys.modules:
            return module_dir(sys.modules[module])
        else:
            spec = find_spec(module)
            if not spec:
                raise ValueError("Module not found", module)
            loader = spec.loader
            if isinstance(loader, SourceFileLoader):
                return os.path.dirname(loader.path)
            elif isinstance(loader, NamespaceLoader) and hasattr(loader, "_path"):
                paths = loader._path
                if len(paths) is int(1):
                    return paths[0]
                else:
                    raise ValueError("Unable to locate a single path for namespace module", module,  paths)
            elif isinstance(loader, ExtensionFileLoader):
                # test interactively with e.g "mypyc.ir.class_ir"
                return os.path.dirname(loader.get_filename())
            else:
                raise ValueError("Module loader not recognized", loader, spec)
    elif isinstance(module, ModuleType):
        if hasattr(module, "__path__"):
            paths = module.__path__
            if len(paths) is int(1):
                return paths[0]
            else:
                raise ValueError("Unable to locate a single path for namespace module", module,  paths)
        elif hasattr(module, "__file__"):
            file = module.__file__
            return os.path.dirname(file)
    raise ValueError("Unrecognized module", module)


__all__ = ("module_distribution", "class_distribution", "module_dir")
