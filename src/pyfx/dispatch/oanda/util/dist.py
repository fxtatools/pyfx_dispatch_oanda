## dist.py

from importlib_metadata import distribution, Distribution, PackageNotFoundError
from importlib.util import find_spec
from importlib.machinery import NamespaceLoader, SourceFileLoader, ExtensionFileLoader
import os
import sys

from .paths import Pathname
from .naming import ModuleLike, ModuleType


def find_distribution(pkg: str) -> Distribution:
    """Return the Distribution for a provided package name"""
    try:
        return distribution(pkg)
    except PackageNotFoundError:
        basepkg = pkg.rsplit(".", maxsplit=1)[0]
        if basepkg == pkg:
            raise
        else:
            return find_distribution(basepkg)


def module_dir(module: ModuleLike) -> Pathname:
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
                ## test interactively with "mypyc.ir.class_ir"
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


__all__ = ("find_distribution", "module_dir")
