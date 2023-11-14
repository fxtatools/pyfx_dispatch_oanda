# pyfx.dispatch.oanda

## Overview

The pyfx.dispatch.oanda project provides a Python API supporting
asynchronous IO for HTTP operations with the OANDA v20 REST API.

The [OpenAPI specification for the OANDA v20 REST API](https://github.com/oanda/v20-openapi)
defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

## Origin

The pyfx.dispatch.oanda source code was automatically generated with an
application of the [OpenAPI Generator](https://openapi-generator.tech).

Build Information:

- OANDA v20 REST API version: 3.0.25
- pyfx.dispatch.oanda version: 1.0.0
- Generator: [python](https://openapi-generator.tech/docs/generators/python/)
- Build package: `org.openapitools.codegen.languages.PythonClientCodegen`

For more information about the OANDA v20 REST API, please visit
[the OANDA developer portal](http://developer.oanda.com/rest-live-v20/introduction/)

For more information about the OpenAPI Generator, please visit
[openapi-generator.tech](https://openapi-generator.tech/).

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.

## Requirements

Python 3.11

## Installation & Usage

### pip install (Git)

The following shell commands can be used to create a Python virtual
environment, then installing the `pyfx.dispatch.oanda` source code
within the same environment.

The path to the environment's `activate` script may vary, by host
platform.

**Example: Direct Installation Using Pip Git Support**
```sh
python -m venv env
source env/bin/activate
pip install git+https://github.com/fxtatools/pyfx_dispatch_oanda.git
```

### Setuptools

This project can be installed from source, using `pip`

**Example: Direct installation From Source**
```sh
if ! [ -e "env/pyvenv.cfg" ]; then python -m venv env; fi
source env/bin/activate
pip install -e .
```

Optional components may be specified with `pip install -e.`

The following optional components are supported:
* `socks` : Install optional socks proxy support (testing)
* `dev` : Install development dependencies

For Qt application development in `pyfx.dispatch.oanda`, one or more of
the following optional components may be installed:
* `app-common` : Generalized application support, should be installed with
   at least one of the following
* `app-pyqt5` : PyQt5 support
* `app-pyqt6` : PyQt6 support
* `app-pyside2` : PySide2 support (Qt5). On Microsoft Windows platforms,
   this feature may not be available outside of the `anaconda` framework,
   or when using PyPI with Python 3 releases previous to 3.10.
* `app-pyside6` : PySide6 support (Qt6)

The following example shows how to install a subset of optional
dependencies, within an existing Git working tree for this project.

**Example: Direct Installation With Optional Dependencies**
```sh
if ! [ -e "env/pyvenv.cfg" ]; then python -m venv env; fi
source env/bin/activate
pip install -e ".[socks, app-pyqt6, dev]"
```


### Qt Framework Selection

Similar to [PythonQwt](https://pythonqwt.readthedocs.io/en/latest/), this project
uses [QtPy](https://github.com/spyder-ide/qtpy/).

With QtPy, when multiple frameworks are installed for Qt in Python, the `QT_API`
environment variable can be used to select which environment will be used in
applications.

For the `pyfx.dispatch.oanda` project, the PyQt5 and PySide2 frameworks may be
supported for purposes of testing.

Primary development is oriented to PySide6, with additional testing for PyQt6.

### Installation with GNU Make

For purposes of development, the installation can be automated with
[GNU make](https://www.gnu.org/software/make/).

The `make sync` target will ensure a Python virtual environment
is created, then installing this project and a set of optional
dependencies within that virtual environment.

For Python dependency selection, the `make sync` task will use the set
of optional dependencies specified in `requirements.in` as well as any
dependencies listed in the optional `requirements.local` file, if the
file exists. Lastly, the main runtime dependencies will be selected
as enumerated in `pyproject.toml`. The dependency selection is managed
with `pip-compile` ([pip-tools](https://pypi.org/project/pip-tools/)).

**Caveats**
* During installation, a file `requirements.txt` will be created,
  using `pip-compile`. This file will indicate the origins of any
  dependencies installed with this method.

* Called under `make sync`, the `pip-sync` task will query the user before
  installing or uninstalling any components within the Python virtual
  environment.

* OS X users may wish to run `brew install gmake` before proceeding
  with the following example.

* This assumes a shell in the style of `sh(1)`, e.g BASH or ZSH.

**Example: Installing Dependencies**
```sh
MAKE=$(if which gmake &>/dev/null; then echo gmake; else echo make; fi)
${MAKE} sync
```

Subsequent of installing GNU make, the following tasks will be available:
* `${MAKE} sync` : Ensure virtual environment; Install dependencies
* `${MAKE} lint` : Ensure virtual environment; Run `flake8`
* `${MAKE} tests` : Ensure virtual environment; Run `pytest`

### Verifying the Installation

The `lint` and `tests` tasks may be used to verify the installation using GNU Make,
as denoted above, [_"Installation with GNU Make"_](#installation-with-gnu-make)

A small set of example applications are provided in [examples/](./examples/README.md).

A brief illustration is provided below, under [_Getting Started_](#getting-started)

### Tests

Tests may be run with the the `lint` and `tests` tasks under GNU Make.

## Getting Started

After [installation](#installation--usage), the following example can be
used to print a summary of account codes for an account with an
authorized API token.

**Caveats**
* Information about the OANDA v20 API is available at the [OANDA Developer Hub](https://developer.oanda.com/rest-live-v20/introduction/). The Hub provides an introduction to the OANDA v20 API, with illustrations of each v20 API endpoint and a complete reference about the data types defined in the v20 API schema.
* An API token is available for OANDA demo accounts,
  [via OANDA](https://www.oanda.com/demo-account/tpa/personal_token).
  Once created, the token should be stored securely.
* For purpose of example, the token may be substituted in place of the
  `<private_api_token>` text, below.
* The `'Bearer '` prefix must be present in the token specified to the API
  server. This token must also include the intermediate  space character
  (`' '`) before the contents of the private API token.
* OANDA provides separate trading servers for demo accounts and live
  trading. This example will access the OANDA v20 server for demo trading
  accounts, via HTTPS.
* This assumes an asynchronous testing environment is available
  at the script top level. The example - plus API token - may be
  evaluated directly, with [IPython](https://pypi.org/project/ipython/).
* For direct evaluation with `python`, please refer to the more detailed
  [examples](./examples/README.md)

```python
import pyfx.dispatch.oanda as dispatch
from pprint import pprint

# Configure a debug-level console logger for the API
from pyfx.dispatch.oanda.util.log import configure_debug_logger

# Set host information and token for API requests
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

Examples in this directory will use an `acounts.ini` file.

The file should use the following syntax - illustrated here for
the demo v20 server.

```ini
[Configuration]
access_token = <private_api_token>
host = https://api-fxpractice.oanda.com/v3
```

The `examples/account.ini` file should be created with filesystem permissions
limiting all file operations to the creating user.

## Author

The [OANDA v20 OpenAPI spec](https://github.com/oanda/v20-openapi) is
published by OANDA at GitHub.

The version of the OANDA v20 OpenAPI used in creating this project:
[3.0.25](https://github.com/oanda/v20-openapi/releases/tag/3.0.25)

This project is not affiliated with OANDA, the OpenAPI Generator, or any
of their associated institutions.

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
