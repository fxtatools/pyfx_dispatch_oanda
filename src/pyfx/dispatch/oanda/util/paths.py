## path utilities

import os
from typing_extensions import Optional
from .naming import exporting

def expand_path(path: os.PathLike, basedir: Optional[os.PathLike] = None) -> os.PathLike:
    '''Return an absolute pathname for `path`

The provided `path` and `basedir` components will be processed as follows:
- If `path` is provided as an absolute pathname, `path` will be returned.

- If `path` is not absolute, then any "~" or "~username" prefix in
  `path` will be expanded as representing a user home directory path,
  per `os.path.expanduser()`. If the resulting path is an absolute
  pathname, that pathname will be returned.

- If `basedir` is provided, then any user homedir prefix in `basedir`
  will be expanded as for `path`. An absolute pathname will be returned,
  representing `path` as relative to the expanded `basedir`.

- Lastly, if `basedir` is not provided, an absolute pathname will be
  returned as representing `path` relative to the pathname returned
  by `os.getcwd()`
'''
    if os.path.isabs(path):
        return path
    path_exp = os.path.expanduser(path)
    if os.path.isabs(path_exp):
        return path_exp
    dir_exp = os.path.expanduser(basedir) if basedir else os.getcwd()
    return os.path.abspath(os.path.join(dir_exp, path_exp))

__all__ = exporting(__name__, ...)

