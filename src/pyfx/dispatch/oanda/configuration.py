# coding: utf-8

import copy
import httpx
import os
import sys
from typing import Optional, Union


# JSON_SCHEMA_VALIDATION_KEYWORDS = {
#     'multipleOf', 'maximum', 'exclusiveMaximum',
#     'minimum', 'exclusiveMinimum', 'maxLength',
#     'minLength', 'pattern', 'maxItems', 'minItems'
# }


class ConfigError(RuntimeError):
    """Common Configuration Error"""
    pass

class Configuration(object):
    """This class contains various settings of the API client.

    :param host: Base url.
    :param access_token: Access token.
    :param server_index: Index to servers configuration.
    :param server_variables: Mapping with string values to replace variables in
      templated server configuration. The validation of enums is performed for
      variables with defined enum values before.
    :param server_operation_index: Mapping from operation ID to an index to server
      configuration.
    :param server_operation_variables: Mapping from operation ID to a mapping with
      string values to replace variables in templated server configuration.
      The validation of enums is performed for variables with defined enum values before.
    :param ssl_ca_cert: str - the path to a file of concatenated CA certificates
      in PEM format.
    """

    _default = None

    def __init__(self, host: str,
                 access_token=None,
                 server_index=None, server_variables=None,
                 server_operation_index=None, server_operation_variables=None,
                 ssl_ca_cert=None,
                 ):
        """Constructor
        """
        self._base_path = host
        """Default Base url
        """
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        """Default server index
        """
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}
        """Default server variables
        """
        self.temp_folder_path = None
        """Temp file folder for downloading files
        """

        self.access_token = access_token
        """Access token
        """

        self.debug = False
        """Debug switch
        """

        self.verify_ssl = True
        """SSL/TLS verification
           Set this to false to skip verifying SSL certificate when calling API
           from https server.
        """
        self.ssl_ca_cert = ssl_ca_cert
        """Set this to customize the certificate file to verify the peer.
        """
        self.cert_file = None
        """client certificate file
        """
        self.key_file = None
        """client key file
        """
        self.assert_hostname = None
        """Set this to True/False to enable/disable SSL hostname verification.
        """
        self.tls_server_name = None
        """SSL/TLS Server Name Indication (SNI)
           Set this to the SNI value expected by the server.
        """

        self.max_connections = 100
        """Maximum number of concurrent HTTP connections.
           Default values is 100, None means no-limit.
        """

        self.max_keepalive_connections = 20

        ## HTTP/2 keepalive expiration period, in seconds
        ## https://www.python-httpx.org/advanced/#pool-limit-configuration
        self.keepalive_expiry = 5

        ## configure an HTTPS proxy for requests, if defined in os.environ.
        ## all requests for this API will be transmitted via HTTPS
        if 'https_proxy' in os.environ:
            self.proxy = httpx.Proxy(os.environ["https_proxy"])
        elif 'HTTPS_PROXY' in os.environ:
            self.proxy = httpx.Proxy(os.environ["HTTPS_PROXY"])
        else:
            self.proxy = None

        self.proxy_headers = None
        """Proxy headers
        """
        self.safe_chars_for_path_param = ''
        """Safe chars for path_param
        """
        self.retries = 5
        """Connection retry limit [int], zero for none
        """
        # Enable client side validation
        self.client_side_validation = True

        self.socket_options = None
        """Options to pass down to the underlying TCP socket
        """

        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        """datetime format
        """

        self.date_format = "%Y-%m-%d"
        """date format
        """

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        result.debug = self.debug
        return result


    @classmethod
    def set_default(cls, default):
        """Set default instance of configuration.

        It stores default configuration, which can be
        returned by get_default_copy method.

        :param default: object of Configuration
        """
        cls._default = default

    @classmethod
    def get_default_copy(cls):
        """Deprecated. Please use `get_default` instead.

        Deprecated. Please use `get_default` instead.

        :return: The configuration object.
        """
        return cls.get_default()

    @classmethod
    def get_default(cls):
        """Return the default configuration.

        This method returns newly created, based on default constructor,
        object of Configuration class or returns a copy of default
        configuration.

        :return: The configuration object.
        """
        if cls._default is None:
            cls._default = Configuration()
        return cls._default

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self._debug = value

    @property
    def proxy(self) -> httpx.Proxy:
        return self._proxy

    @proxy.setter
    def proxy(self, value: Optional[Union[str, dict[str, Optional[str]], httpx.Proxy]]):
        prx = value if value is None or isinstance(value, httpx.Proxy) else httpx.Proxy(value)
        self._proxy = prx

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth = {}
        return auth

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 3.0.25\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)

    def get_host_settings(self):
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                'url': "/v3",
                'description': "No description provided",
            }
        ]

    def get_host_from_settings(self, index, variables=None, servers=None):
        """Gets host URL based on the index and variables
        :param index: array index of the host settings
        :param variables: hash of variable and the corresponding value
        :param servers: an array of host settings or None
        :return: URL based on host settings
        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers)))

        url = server['url']

        # go through variables and replace placeholders
        for variable_name, variable in server.get('variables', {}).items():
            used_value = variables.get(
                variable_name, variable['default_value'])

            if 'enum_values' in variable \
                    and used_value not in variable['enum_values']:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(
                        variable_name, variables[variable_name],
                        variable['enum_values']))

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @property
    def host(self):
        """Return generated host."""
        return self.get_host_from_settings(self.server_index, variables=self.server_variables)

    @host.setter
    def host(self, value):
        """Fix base path."""
        self._base_path = value
        self.server_index = None
