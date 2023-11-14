##
## Configuration for API client - YAML prototype
##
## defined previous to the ChainMap interface for Configuration

import configparser as cf
import logging
import os

import yaml
from typing import Any, Mapping, Optional, Union, Self
from typing_extensions import TypeAlias

from .configuration import Configuration
from .util.paths import expand_path, Pathname


logger = logging.getLogger(__name__)

class ConfigError(RuntimeError):
    """Common Configuration Error"""
    pass

def load_config(path: Pathname, overrides: Optional[Mapping[str, Any]] = None) -> Configuration:
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
fxpractice = True
```

The file should be created with access permissions
limiting all file operations to the creating user.

'''
    abspath = expand_path(path)
    if not os.path.exists(abspath):
        raise ConfigError("File not found", abspath)
    parser = cf.ConfigParser(interpolation=cf.ExtendedInterpolation())
    parser.read(abspath)
    cfgopts = parser['Configuration']
    config_model = Configuration.model_fields
    for name in cfgopts.keys():
        if name not in config_model:
            logger.critical("Configuration.load: Not a recognized configuration field, discarding %r in %s", name, abspath)            
            del cfgopts[name]
    if overrides:
        for opt, value in overrides.items():
            if name in config_model:
                cfgopts[opt] = value
            else:
                logger.critical("Configuration.load: Not a recognized configuration field, discarding %r in load_config() overrides", name)                        
    if 'Configuration' in parser.keys():
        return Configuration(**cfgopts)
    else:
        logger.critical("Configuration.load: No 'Configuration' section in INI file, using empty configuration: %s", os.path.abspath(path))
        return Configuration()

##
## YAML configuration prototype
##


# unified type definitions for YAML loaders, Dmpers

YAMLLoader: TypeAlias = Union[yaml.Loader, yaml.FullLoader, yaml.SafeLoader, yaml.UnsafeLoader]
YAMLLoaderType: TypeAlias = Union[type[yaml.Loader], type[yaml.FullLoader], type[yaml.SafeLoader], type[yaml.UnsafeLoader]]

YAMLDumper: TypeAlias = Union[yaml.BaseDumper, yaml.SafeDumper, yaml.Dumper]
YAMLDumperType: TypeAlias = Union[type[yaml.BaseDumper], type[yaml.SafeDumper], type[yaml.Dumper]]


class YamlConfig(Configuration):

    @classmethod
    def get_yaml_tag(cls) -> str:
        if hasattr(cls, "yaml_tag"):
            return cls.yaml_tag
        else:
            return "!python/object:" + cls.__module__ + "." + cls.__name__

    @classmethod
    def set_yaml_tag(cls, tag: str):
        cls.yaml_tag = tag

    @classmethod
    def configure_yaml_writer(cls, dumper: Optional[Union[YAMLDumper, YAMLDumperType]] = None):
        dst = dumper if dumper else yaml
        dst.add_representer(cls, cls.serialize_yaml)

    @classmethod
    def configure_yaml_reader(cls, loader: Optional[Union[YAMLLoader, YAMLLoaderType]] = yaml.SafeLoader):
        tag = cls.get_yaml_tag()
        dst = loader if loader else yaml
        dst.add_constructor(tag, cls.deserialize_yaml)

    @classmethod
    def serialize_yaml(cls, dumper: yaml.BaseDumper, inst: Self):
        ## abstract -> instance (protocol) method
        ## for write_yaml()
        tag = cls.get_yaml_tag()
        return dumper.represent_mapping(tag, inst.to_dict(), flow_style=False)

    @classmethod
    def deserialize_yaml(cls, loader: YAMLLoader, node):
        ## abstract -> instance (protocol) method
        ## for load_yaml()
        args: Mapping = loader.construct_mapping(node)
        host = args['host']
        del args['host']
        return cls(host, **args)

    @classmethod
    def load_yaml(cls, data, loader: Union[YAMLLoader, YAMLLoaderType] = yaml.SafeLoader):
        cls.configure_yaml_reader(loader)
        return yaml.load(data, loader)

    @classmethod
    def write_yaml(cls, instance: Self, io=None,
                   dumper: Union[YAMLDumper, YAMLDumperType] = yaml.SafeDumper):
        cls.configure_yaml_writer(dumper)
        return yaml.dump(instance, io, dumper)
