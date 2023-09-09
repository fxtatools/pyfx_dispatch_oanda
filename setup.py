# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "pyfx_dispatch_oanda"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "aiohttp >= 3.0.0",
    "pydantic >= 1.10.5, < 2",
    "aenum"
]

setup(
    name=NAME,
    version=VERSION,
    description="aio support for OANDA v20 REST API (Unofficial)",
    author="OANDA API Support",
    author_email="spchamp@users.noreply.github.com",
    url="https://github.com/fxtatools/pyfx_dispatch_oanda",
    keywords=["OpenAPI", "OpenAPI-Generator", "OANDA v20 REST API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="MIT",
    long_description_content_type='text/markdown',
    long_description='Asynchronous IO for the OANDA v20 REST API (Unofficial)',
    package_data={"pyfx.dispatch.oanda": ["py.typed"]},
)
