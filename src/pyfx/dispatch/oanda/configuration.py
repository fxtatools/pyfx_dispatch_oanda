# Configuration for ApiClient

from enum import StrEnum
from collections import ChainMap
from contextlib import contextmanager  # TBD
from contextvars import Context, ContextVar, Token, copy_context  # TBD
from pydantic import BaseModel, Field, ConfigDict, SecretStr, ValidationError
from pydantic.fields import PydanticUndefined

from .util import exporting
import copy
import httpx
import os
from os import PathLike
import sys
import sysconfig
from typing import Any, List, Literal, Mapping, Optional, Self, Sequence, Union
from typing_extensions import Annotated, ClassVar, TypeAlias

from . import __version__
from .credential import Credential
from .hosts import FxHostInfo


class ProfileName(StrEnum):
    fxPractice: str = FxHostInfo.fxPractice.name
    fxLive: str = FxHostInfo.fxLive.name


def environ_proxy() -> Optional[str]:
    """default_factory for ConfigurartionBase.proxy

    If either of the environment variables `https_proxy` or `HTTPS_PROXY` is set,
    returns the value of that envrionment variable, else returns None

    Implementation Notes:
    - This function is used as a `default_factory` for the Configuration.proxy field
    """
    return os.environ["https_proxy"] if "https_proxy" in os.environ else os.environ["HTTPS_PROXY"] if "HTTPS_PROXY" in os.environ else None


class ConfigurationModel(BaseModel):
    '''Configuration settings for the API client.

    Initialization:

    ```python
    Configuration(host = <host>, access_token = <token>, ... )
    ```

    Instance fields, available as keyword arguments for initialization:
    - fxpractice (bool) (default: True) If True, use fxTrade Practice endpoints, else use fxTrade Live endpoints
    - access_token (str) [required]
    - datetime_format (str)
    - max_connections (optional int)
    - max_keepalive_connections (int)
    - keepalive_expiry (int, in units of seconds)
    - retries (int)
    - proxy (optional string, httpx.Proxy, or literal False): False to disable proxying, Null to use OS environ
    - verify_ssl (bool) default: True
    - ssl_ca_cert (path-like) default: Use Certifi cert
    - ssl_cert_file, ssl_key_file (path-like) both must be set if either is provided
    - tls_server_name (string)
    - socket_options (sequence of sequences) socket options, provided as a sequence in sequence
    '''

    model_config: ClassVar[ConfigDict] = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True, validate_assignment=True,
        # extra="allow"
    )

    fxpractice: bool = True
    '''if True, use fxTrade Practice endpoints, else use fxTrade Live endpoints'''

    access_token: Annotated[Credential, Field(...)]
    '''Access token for the v20 API'''

    datetime_format: str = "%x %X %Z"
    '''datetime format for the console user interface'''

    timezone: str = os.environ["TZ"] if "TZ" in os.environ else "UTC"
    '''Timezone for console user interface.

    The default value will be initialized from `TZ` if `TZ` is set
    in `os.environ`, else using UTC'''

    max_thread_workers: Optional[int] = None
    '''Maximum number of workers for response processing

    `None` implies to use the system default.
    '''

    max_connections: Optional[int] = 100
    '''Client-side limit for number of concurrent HTTP connections.
    Default value is 100, None means no limit.
    '''

    max_keepalive_connections: int = 10
    '''Client-side limit for number of conccurrent HTTP keepalive connections'''

    keepalive_expiry: int = 10
    '''HTTP/2 keepalive expiration, in units of seconds.

    For more information, documentation from the HTTPX project:
    https://www.python-httpx.org/advanced/#pool-limit-configuration'''

    retries: int = 5
    '''Connection retry limit, zero for none'''

    proxy: Optional[Union[str, httpx.Proxy, Literal[False]]] = Field(default_factory=environ_proxy)
    '''HTTPS proxy for REST client requests.

    If None, the proxy will be determined from the first defined environment
    variable in `https_proxy` and `HTTPS_PROXY` at time of call.

    If False, no proxy will be used.

    If an httpx.Proxy object, the object will be used directly for the REST client.

    If a string, the string should provide the URL for an HTTPS proxy server.

    This value will be used for determining the proxy configuration for the REST
    client of each ApiClient
    '''

    verify_ssl: bool = True
    '''SSL/TLS verification.

    Set this to False to skip verifying the SSL hostname and certificate when calling the API
    '''

    ssl_ca_cert: PathLike = os.path.join(sysconfig.get_paths()['purelib'], "certifi", "cacert.pem")
    '''Pathname for the PEM-formatted SSL CA certificate file '''

    ssl_cert_file: Optional[PathLike] = None
    '''Optional SSL certificate file for the SSL Context.

    If specified, key_file should also be defined'''

    ssl_key_file: Optional[PathLike] = None
    '''Optional SSL key file for the SSL Context.

    If specified, cert_file should also be defined
    '''

    tls_server_name: Optional[PathLike] = None
    '''SSL/TLS Server Name Indication (SNI)

    Set this to the SNI value expected by the server.
    '''

    socket_options: Optional[Sequence[Sequence[int]]] = None
    '''Options to pass to the underlying TCP socket

    See also: socket.getsockopt()
    '''

    def __repr__(self) -> str:
        return "%s(fxpractice=%s, ...)" % (self.__class__.__name__, self.fxpractice,)

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def debug_header(cls):
        '''Return a string of debug header information'''
        return "SDK Debug Report, pyfx.dispatch.oanda\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 3.0.25\n"\
               "SDK Package Version: {sdk}".\
               format(env=sys.platform, pyversion=sys.version, sdk=__version__)



class ConfigurationMap:
    ## ChainMap integration here
    pass


class Configuration(ConfigurationModel):
    '''Multi-Profile configuration model for pyfx.dispatch.oanda

    ## Configuration Profiles

    This class provides an implementation of configuration profiles,
    using a set of ChainMap as a backing store.

    For each Configuration instance, one configuration profile is
    provided for fxLive configuration, and one configuration profile
    for fxPractice configuration. Each profile is realized with a
    ChainMap unique to that instance.

    A third mapping is provided in each instance, for common field
    values. These values will be applied for both of the fxLive and
    fxPractice configuration profiles, for configuration fields not
    directly set in the respective profile.

    ## The Active Profile

    For each ApiClient/Configuration instance in each thread, exactly
    one of the fxPractice and fxLive configurations may be active at
    any one time.

    At the instance scope, the active profile may be set with any
    of the methods, `use_fxlive_profile()`, `use_fxpractice_profile()`,
    and `use_profile()`

    ## Access for Profile Fields (Active Profile)

    For the active configuration profile, profile field values may
    be accessed with conventional `instance.attribute` accessors or
    with a subscript syntax per the field name.

    Example:

    ```python
    config['proxy'] is config.proxy
    # => True
    config.proxy = "https://10.5.10.1:3128"
    ```

    When setting a field directly on the configuration instance and
    `__debug__` is not a _falsey_ value, then any new value will
    be validated for the corresponding configuration field.

    If  Python is running under command-line `-O` optimizations
    or `__debug__` has otherwise been set to a _falsey_ value, no
    field validation will be performed.

    Fields may be unset in the active configuration profile, using `del`
    ```python
    del config['proxy']
    ```

    The `del` operation is not supported for fields not having a default
    value, mainly the `access_token` field and the effective profile
    designator field, `fxpractice`. The `fxpractice` field will be
    constantly `True` for the `fxpractice` profile, and constantly `False `
    for the `fxlive` profile.

    ## Access for Profile Fields (Common Profile)

    The following methods are provided for access to configuration values
    within the common configuration profile, for each Configuration instance:

    - `set_common(name, value)`
    - `get_common(name)`
    - `unset_common(name)`

    Each of these methods will raise a `pydantic.ValidationError` if the provided
    name does not denote a defined field name.

    For `set_common()`, any field validation will be performed as similar to the
    active profile. The provided value will be validated for the corresponding
    configuration field, when `__debug__`.

    ## Low-Level Backing Store

    The ChainMap for each profile may be accessed directly, with the following
    methods:
    - `get_fxlive_profile()`
    - `get_fxpractice_profile()`

    The Mapping dictionary for the default profile may be accessed with the
    method, `get_common_profile()`

    For any value set directly to the respective ChainMap or set directly to
    the default Mapping, the value will not be validated for the corresponding
    configuration field.

    ## Host Information

    The method `get_host()` will return host information for client requests
    under the active configuration profile. This method will return a value
    defined under the `FxHostInfo` enum.
    '''

    ## backing store for per-profile configuration
    _profiles: Mapping[str, ChainMap[str, Any]]
    ## backing store for user-specified defaults
    _profile_default_map: Mapping[str, Any]
    ## backing store for the active profile configuration.
    ## should be equal to a value in _profiles
    _current_profile: ChainMap[str, Any]
    ## should be equal to a key in _profiles
    _current_profile_name: str

    _profile_data_fields: ClassVar[frozenset[str]] = frozenset({
        "_profiles", "_profile_default_map", "_current_profile", "_current_profile_name"
    })
    _profile_unique_fields: ClassVar[frozenset[str]] = frozenset({
        "access_token", "fxpractice"
    })
    _profile_common_fields: ClassVar[frozenset[str]] = frozenset(ConfigurationModel.model_fields.keys()).difference(_profile_unique_fields)

    def get_host(self):
        if self.fxpractice:
            return FxHostInfo.fxPractice.value
        else:
            return FxHostInfo.fxLive.value

    def get_fxlive_profile(self) -> ChainMap[str, Any]:
        return self.get_profile(ProfileName.fxLive.value)

    def get_fxpractice_profile(self) -> ChainMap[str, Any]:
        return self.get_profile(ProfileName.fxPractice.value)

    def get_profile(self, name: str) -> ChainMap[str, Any]:
        return self._profiles[name]

    def use_fxlive_profile(self) -> ChainMap[str, Any]:
        return self.use_profile(ProfileName.fxLive.value)

    def use_fxpractice_profile(self) -> ChainMap[str, Any]:
        return self.use_profile(ProfileName.fxPractice.value)

    def use_profile(self, name: str) -> ChainMap[str, Any]:
        if name in self._profiles:
            self._current_profile = self._profiles[name]
            self._current_profile_name = name
            return self._current_profile
        else:
            raise ValidationError("Proifle not defined", name)

    def get_common_profile(self) -> Mapping[str, Any]:
        '''Return the Mapping dictionary for default profile configuration
        in this Configuration instance.

        Each key in the mapping will represent a Configuration field name.

        Each value will serve as the default for the denoted field, for
        configuration profiles where the field has not been set directly.

        Fields may be set in the active profile, using dict index syntax

        '''
        return self._profile_default_map

    def set_common(self, name: str, value: Any) -> Self:
        '''Set the default value for a configuration field.

        This value will be shared between fxPractice and fxLive profiles
        where the value has not been set

        If the provided field name is not a configuration field name, raises
        ValidationError
        '''
        model_fields = self.__class__.model_fields
        if name in model_fields:
            if __debug__:
                self.__pydantic_validator__.validate_assignment(self, name, value)
            self._profile_default_map[name] = value
        else:
            raise ValidationError("Configuration field not found", name)

    def get_common(self, name: str) -> Any:
        '''Return the default value for a configuration field.

        If no default value has been set, raises ValidationError

        If the provided field name is not a configuration field name, raises
        ValidationError
        '''
        model_fields = self.__class__.model_fields
        if name in model_fields:
            defaults = self._profile_default_map
            if name in defaults:
                return defaults[name]
            else:
                raise ValueError("No default value defined")
        else:
            raise ValidationError("Configuration field not found", name)

    def unset_common(self, name: str) -> Any:
        '''Unset the default value for a configuration field.

        If a default value has not been set, returns None, else returns the
        previously defined value.

        Implementation Note: For each field not set in the active profile
        and not set in the defult profile, a default value will be determined
        from fields defined at the class scope.

        If the provided field name is not a configuration field name, raises
        ValidationError
        '''
        model_fields = self.__class__.model_fields
        if name in model_fields:
            defaults = self._profile_default_map
            if name in defaults:
                value = defaults[name]
                del defaults[name]
                return value
        else:
            raise ValidationError("Configuration field not found", name)

    def __init__(self, **kwargs):
        '''Create a new Configuration instance

    Instance fields, available as keyword arguments for initialization:
    - fxpractice (bool) (default: True) If True, use fxTrade Practice endpoints, else use fxTrade Live endpoints
    - access_token (str) [required]
    - datetime_format (str)
    - max_connections (optional int)
    - max_keepalive_connections (int)
    - keepalive_expiry (int, in units of seconds)
    - retries (int)
    - proxy (optional string, httpx.Proxy, or literal False): False to disable proxying, Null to use OS environ
    - verify_ssl (bool) default: True
    - ssl_ca_cert (path-like) default: Use Certifi cert
    - ssl_cert_file, ssl_key_file (path-like) both must be set if either is provided
    - tls_server_name (string)
    - socket_options (sequence of sequences) socket options, provided as a sequence in sequence

    Excepting the access token, keyword arguments provided here will be used to initialize
    the default configuration profile
    '''
        profile_args = {}
        for field in self.__class__._profile_data_fields:
            ## move all profile data args into profile_data
            if field in kwargs:
                profile_args[field] = kwargs[field]
                del kwargs[field]

        common_args = {}
        for name in self.__class__._profile_common_fields:
            ## move kwargs to common args for each kwarg not in _profile_unique_fields
            if name in kwargs:
                common_args[name] = kwargs[name]
                del kwargs[name]

        ## verify that no unknown args are in kwargs
        unknown = set(common_args.keys()).difference(self.__class__.model_fields)
        if len(unknown) is not int(0):
            raise ValidationError("Unknown configuration fields", unknown)

        ## initialize required and unique fields for the object via pydantic,
        ## before accessing any instance attributes below
        super().__init__(**kwargs)

        ## initialize profile data
        for field in profile_args:
            setattr(self, profile_args[field])
        if "_profile_default_map" in profile_args:
            self._profile_default_map = profile_args["_profile_default_map"]
        else:
            self._profile_default_map = {}

        if "_profiles" in profile_args:
            self._profiles = profile_args["_profiles"]
        else:
            self._profiles = {}
        profiles = self._profiles

        defaults = self._profile_default_map
        ## initialize defaults
        for key, value in common_args.items():
            defaults[key] = value

        ## initialize a profile map for each ProfileName enum member,
        ## using annotations of ProfileName as an iteration source
        for name in ProfileName.__annotations__.keys():
            if name not in profiles:
                profile_config = {}
                profiles[name] = ChainMap(profile_config, defaults)

        ## set constants fields per profile
        profiles[ProfileName.fxLive.value]['fxpractice'] = False
        profiles[ProfileName.fxPractice.value]['fxpractice'] = True

        if "_current_profile_name" in profile_args:
            self._current_profile_name = profile_args["_current_profile_name"]
        else:
            fxpractice = kwargs.get("fxpractice", True)
            self._current_profile_name = ProfileName.fxPractice if fxpractice else ProfileName.fxLive

        if "_current_profile" in profile_args:
            self._current_profile = profile_args['_current_profile']
        else:
            self._current_profile = self._profiles[self._current_profile_name]

        profile = self._current_profile
        ## re-proceses all profile-uniqe kwargs,
        ## now that the instance profile map is initialized
        for key, value in kwargs.items():
            profile[key] = value

    ##
    ## attribute -> chainmap access for model_fields
    ##

    def __getitem__(self, key: str, assume_model: bool = False) -> Any:
        model_fields = Configuration.model_fields
        if assume_model or key in model_fields:
            if key in self._current_profile:
                return self._current_profile[key]
            else:
                field = model_fields[key]
                default = field.default_factory() if field.default_factory else field.default
                if default is PydanticUndefined:
                    raise KeyError("Field is unset and no default is defined", key)
                else:
                    return default
        else:
            raise KeyError("Configuration field not found", key)

    def __setitem__(self, key: str, value: Any, assume_model: bool = False) -> Any:
        if assume_model or key in Configuration.model_fields:
            if __debug__:
                self.__pydantic_validator__.validate_assignment(self, key, value)
            self._current_profile[key] = value
            self.__pydantic_fields_set__.add(key)
        else:
            raise KeyError("Configuration field not found", key)

    def __delitem__(self, key: str, assume_model: bool = False) -> Any:
        if assume_model or key in Configuration.model_fields:
            profile = self._current_profile
            if key in profile:
                self.__pydantic_fields_set__.remove(key)
                return profile.__delitem__(key)
        else:
            raise KeyError("Configuration field not found", key)

    def __getattribute__(self, name: str, assume_model: bool = False) -> Any:
        if assume_model or name in Configuration.model_fields:
            ## pass through to access the value from the profile backing store,
            ## or return a default if unset
            return Configuration.__getitem__(self, name, True)
        else:
            return BaseModel.__getattribute__(self, name)

    def __getattr__(self, name: str, assume_model: bool = False) -> Any:
        if assume_model or name in Configuration.model_fields:
            return self.__getitem__(name, True)
        else:
            return super().__getattr__(name)

    def __setattr__(self, name: str, value: Any, assume_model: bool = False):
        if assume_model or name in Configuration.model_fields:
            return self.__setitem__(name, value)
        else:
            return super().__setattr__(name, value)
            # return object().__setattr__(name, value)

    def __delattr__(self, name: str, assume_model: bool = False):
        if assume_model or name in self.__class__.model_fields:
            return self.__delitem__(name)
        else:
            return super().__delattr__(name)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result


class ConfigurationMgr():
    profiles: Mapping[str, Configuration]
    pass

current_config: Configuration = ContextVar("current_config")


__all__ = exporting(__name__, ...)
