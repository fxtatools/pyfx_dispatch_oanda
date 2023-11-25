# pyfx.dispatch.oanda

## Overview

The pyfx.dispatch.oanda project provides a Python API supporting
asynchronous IO for HTTP operations with the OANDA v20 REST API.

The [OpenAPI specification for the OANDA v20 REST API](https://github.com/oanda/v20-openapi)
defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

## Origin

In its first incarnation, the pyfx.dispatch.oanda source code was automatically
generated with an application of the [OpenAPI Generator](https://openapi-generator.tech).

Build Information:

- OANDA v20 REST API version: 3.0.25
- pyfx.dispatch.oanda version: 1.0.0
- Generator: [python](https://openapi-generator.tech/docs/generators/python/)
- Build package: `org.openapitools.codegen.languages.PythonClientCodegen`

Subsequently, the API has been revised. Changes include:
- Updating the API model definitions for Pydantic 2
- Using HTTPX, HTTPCore, and hpack for HTTP/2 support
- Integrating ijson for asynchronous JSON decoding
- Revising the asyncio support in the original `DefaultApi` and `ApiClient` classes, towards a futures-oriented methodology for request/response processing

Revisions in protoyping (Work in Progress)
- Revising the original request/response model in the `DefaultApi` and `ApiClient` classes
  - Applications and testing for basic HTTP requests (REST API)
  - Adding support for requests with OANDA fxTrade v20 streaming endpoints
  - Adding suport for iterative processing with responses containing a request URL 'link' in response headers and responses containing a sequence of request URLs in the JSON body of the reply
- Adding support for account data persistence with ZODB
- Integrating Pandas, numpy, numba and numexpr with data available from API endpoints, for applications in market data analysis
  - Developing a technial indicators API for application with quotes (candlesticks) data and price (ask/bid) data from API endpoints
  - User interface support for technical analysis
  - Integration with IPythona and Jupyter kernels
  - API generalization, with initial prototyping for the OANDA fxTrade v20 API
- User interface models for account information, technical analysis applications, and live trading support

For more information about the OANDA v20 REST API, please visit
[the OANDA developer portal](http://developer.oanda.com/rest-live-v20/introduction/)

For more information about the OpenAPI Generator, please visit
[openapi-generator.tech](https://openapi-generator.tech/).

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.

## Requirements

This project depends on the asyncio TaskGroup API, as available in Python 3.11 and more recent releases of the Python (cpython) platform.

## Installation & Usage

pyfx.dispatch.oanda is available for installation from source. The project source code can be retrieved
using `git` and installed via `pip`.

Pursuant with the first official relase of the project,  the codebase will be published for installation
directly from PyPI packages.

### pip install (Git)

The following shell commands can be used to create a Python virtual
environment, then installing the `pyfx.dispatch.oanda` source code
within that virtual environment.

The path to the environment's `activate` script may vary, by host
platform.

**Example: Direct Installation Using Pip Git Support**
```sh
python -m venv --prompt pyfx env
source env/bin/activate
pip install git+https://github.com/fxtatools/pyfx_dispatch_oanda.git
```

### Git and Setuptools

When the source code has been cloned using `git`, the project
can be installed directly from the working tree, using `pip`

**Example: Direct installation From Source**
```sh
if ! [ -e "env/pyvenv.cfg" ]; then python -m venv --prompt "pyfx" env; fi
source env/bin/activate
pip install --use-pep517 --verbose -e .
```

Optional components may be specified with `pip install -e.[<optional>`

The following optional components are supported:
* `socks` : Install optional socks proxy support (testing)
* `dev` : Install development dependencies

**Example: Direct Installation With Optional Dependencies**
```sh
if ! [ -e "env/pyvenv.cfg" ]; then python -m venv --prompt "pyfx" env; fi
source env/bin/activate
pip install --use-pep517 --verbose -e ".[socks, dev]"
```

### Installation with GNU Make

Beginning with a source tree for the project, the installation can
be automated with [GNU make](https://www.gnu.org/software/make/).

The `make sync` target will ensure a Python virtual environment
is created, then installing this project and a set of initial
dependencies within that virtual environment.

The `make sync` task will use the set of optional dependencies
specified in `requirements.in` as well as any dependencies listed
in the optional `requirements.local` file, if the file exists.
Lastly, the main runtime dependencies will be selected as
enumerated in `pyproject.toml`. The dependency selection is managed
with `pip-compile` ([pip-tools](https://pypi.org/project/pip-tools/)).

**Caveats**
* During installation, a file `requirements.txt` will be created,
  using `pip-compile`. Annotations in this file will indicate the
  origins of any dependencies installed with this approach.

* Called under `make sync`, the `pip-sync` task will query the user
  before installing or uninstalling any components within the Python
  virtual environment.

* OS X users may wish to run `brew install gmake` before proceeding
  with the following example.

* This assumes a shell in the style of `sh(1)`, e.g BASH or ZSH.

**Example: Installing Dependencies**
```sh
MAKE=$(if which gmake &>/dev/null; then echo gmake; else echo make; fi)
${MAKE} sync
```

The following GNU make tasks are available.
* `${MAKE} sync` : Ensure virtual environment; Install dependencies
* `${MAKE} lint` : Ensure virtual environment; Run `flake8`
* `${MAKE} tests` : Ensure virtual environment; Run `pytest`
* `${MAKE} check-tests` : Check for errors in the testing system
  and in the baseline API. On success, `pytest` will print the
  collected testing series to the console output stream

### Verifying the Installation

The installation can be verified using the `lint` and/or `tests` tasks
with GNU make.

### Examples

A small set of example applications are provided in [examples/](./examples/README.md).

A brief illustration is provided below, under [_Getting Started_](#getting-started).
This illustration also provides an introduction to the configuration INI system used
in this project.

**Examples: Args, Configuration**

The example applications will use a common configuration INI file,
stored under the user's home directory. To initialize this file,
the user will be queried for an API token on the first run,
whenever the file does not exist.

When creating the configuration INI file, the
configuration framework will ensure that the file
is not group- or other-readable.

The example applications will also accept a pathname for the
configuration file.

Each application provides a `--help` commandline arg,
illustrating the range of supported command line args
for that example.

Usage e.g:
```sh
source env/bin/activate
python -O examples/quotes_async.py
```

### Tests

Tests may be run with the the `lint` and `tests` tasks under GNU Make.

## Getting Started

After [installation](#installation--usage), the following example can be
used to print a summary of account codes for an account with an
authorized API token.

**Caveats**
* Information about the OANDA v20 API is available at the
  [OANDA Developer Hub](https://developer.oanda.com/rest-live-v20/introduction/).
  The Hub provides an introduction to the OANDA v20 API, with illustrations of
  each v20 API endpoint and references about the response data types defined
  in the v20 API schema.
* An API token is available for OANDA demo accounts,
  [via OANDA](https://www.oanda.com/demo-account/tpa/personal_token).
  Once created, the token should be stored securely.
* For purpose of example, the token may be substituted in place of the
  `<private_api_token>` text, below.
* OANDA provides separate trading servers for demo accounts and live
  trading. This example will use the OANDA v20 server for demo trading
  accounts.
* This assumes an asynchronous environment is available at the script
  top level. The example - with API token - may be evaluated directly,
  with [IPython](https://pypi.org/project/ipython/).
* For direct evaluation within `python` programs, please refer to the
  more detailed [examples](./examples/README.md)

```python
import pyfx.dispatch.oanda as dispatch
from pprint import pprint

# Configure a debug-level console logger for the API
from pyfx.dispatch.oanda.util.log import configure_debug_logger

# Set host information and token for API requests
#
# The API will use OANDA fxPractice endpoints, by default.
#
configuration = dispatch.Configuration(
    access_token = '<private_api_token_>',
    fxpractice = True
)

api_response = None

# Create an asynchronous context with an instance of the API client
async with dispatch.ApiClient(configuration) as api_client:
    ## Create an instance of the API class
    api_instance = dispatch.DefaultApi(api_client)
    ## Send a single API request
    api_response = await api_instance.list_accounts()

# print the result of the API query
if api_response:
    pprint(api_response.accounts)

```

<a id="examples"></a>
## Example Scripts

Additional examples are available in the [examples/](./examples/README.md) directory.

Examples in this directory will use a `config.ini` file, located at
{...} <app_dir>/config.ini

The file should use the following syntax. For the fxPractice v20 server:

```ini
[Configuration]
access_token = <private_api_token>
```

For fxLive accounts:
```ini
[Configuration]
access_token = <private_api_token>
fxpractice = False
```

The INI file syntax supports [extended interpolation][extended_interpolation].
When encoding string values within the file, the dollar sign `"$"`
should be escaped, e.g

```ini
datetime_format = $$ %a, %d %b %Y %H:%M:%S %Z
```

Additional Caveats:
- The `examples/account.ini` file should be created with filesystem
  permissions limiting file operations to the creating user.


## Author

The [OANDA v20 OpenAPI spec](https://github.com/oanda/v20-openapi) is
published by OANDA at GitHub.

The version of the OANDA v20 OpenAPI used in creating this project:
[3.0.25](https://github.com/oanda/v20-openapi/releases/tag/3.0.25)

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.

[extended_interpolation]: https://docs.python.org/3.11/library/configparser.html#configparser.ExtendedInterpolation]

<!--  LocalWords:  OANDA OpenAPI openapi venv env Setuptools fi dev txt
 -->
<!--  LocalWords:  pyqt PyQt pyside PySide PyPI PythonQwt QtPy FIXME
 -->
<!--  LocalWords:  pyproject toml gmake ZSH pytest api
 -->
<!--  LocalWords:  HTTPS IPython pprint async ApiClient DefaultApi auth
 -->
<!--  LocalWords:  Oanda acounts ini filesystem walkthrough
 -->
