##
## Configuration for the API client
##

import configparser as cf
import logging 
import os

from .configuration import Configuration, ConfigError
from .util import expand_path

def load_config(path: os.PathLike) -> Configuration:
    '''Parse and return the contents of a configuration file,
as a Configuration object for the API client.

## Syntax

- `path`: Pathname for the configuration file. Relative pathnames
  will be interpreted as relative to os.getcwd()

Exceptions and Logging:
- If `path` does not denote an existing file, raises ConfigError

Returns: The initialized `Configuration` object.

Caveats:
- If a `Configuration` section does not exist in the file,
  a warning message will be logged and the Configuration 
  object will be initialized with all default values.

## File Format

The file should be of an INI format and should include
a section named `Configuration`. Each entry in this 
section should denote an instance field of the class,
`Configuration`, for example:

```
[Configuration]
access_token = <private_token>
host = https://api-fxpractice.oanda.com/v3
```

The file should be created with access permissions
limiting all file operations to the creating user.

'''
    abspath = expand_path(path)
    if not os.path.exists(abspath):
        raise ConfigError("File not found", abspath)
    parser = cf.ConfigParser()
    parser.read(abspath)
    if 'Configuration' in parser.keys():
        return Configuration(**parser['Configuration'])
    else:
        logger = logging.getLogger(__name__)
        logger.warn("No Configuration section in INI file %s",
                    os.path.abspath(path))
        return Configuration()
