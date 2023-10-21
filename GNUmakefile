## GNU Makefile for PyFX::Dispatch::Oanda

sinclude .env

ifndef OSKIND
UNAME_O:=		$(shell uname -o)
## _OSKIND_ defines the effective default
_OSKIND_?=		NIX
_OSKIND_Msys?=		NT
_OSKIND_Cygwin?=	NT
OSKIND:=		${_OSKIND_${UNAME_O}}
endif

ifndef PYTHON
PYTHON:=		$(shell if python3 --version 1>/dev/null 2>/dev/null; then echo python3; else echo python; fi)
endif
PYVENV_DIR?=		${CURDIR}/env
REQUIREMENTS_IN?=	requirements.in
REQUIREMENTS_TXT?=	requirements.txt
REQUIREMENTS_DEPS?=	pyproject.toml ${REQUIREMENTS_IN} $(wildcard requirements.local)
PYVENV_DEPS?=		${PYVENV_DIR}/pyvenv.cfg
PROJECT_PY?=		project.py


## goal: configure pip-compile to use the same cache dir as pip
PIP_CACHE?=		$(if ${OSKIND} == "NT",${LOCALAPPDATA}\\pip\\cache,${HOME}/.cache/pip)

## values that may contain spaces within PIP_ARGS should be double quoted, generally
PIP_ARGS?=		${PIP_PROXY_ARGS} -v --cache-dir="${PIP_CACHE}"

ifndef PYVENV_SUBDIR
PYVENV_SUBDIR:=		$(shell if [ "$$(${PYTHON} -c 'import sys; print(sys.platform)')" = "win32" ]; then echo "Scripts"; else echo "bin"; fi)
endif
PYVENV_BINDIR?=		${PYVENV_DIR}/${PYVENV_SUBDIR}

FETCH?=			${PYTHON} ${PROJECT_PY} fetch
FETCH_DEPS?=		${PROJECT_PY}


FLAKE8_LINT_SELECT?=	E9,F63,F7,F82
FLAKE8_LINT_IGNORE?=	E117,E127,E128,E203,E251,E252,E262,E266,W291,E302,E303,E501
FLAKE8_LINT_IGNORE_PER_FILE?=	__init__.py:F401


all: checks


check-vars:
	@echo OSKIND: ${OSKIND}
	@echo PIP_CACHE: ${PIP_CACHE}

env: ${PYVENV_DIR}/pyvenv.cfg

projects: ${BUILDDIR}/oanda/pyproject.toml

requirements: ${REQUIREMENTS_TXT}

test: tests

${PYVENV_DIR}/pyvenv.cfg:
	if ! [ -e "${PYVENV_DIR}" ]; then \
		${PYTHON} ${PROJECT_PY} ensure_env ${PYVENV_DIR}; \
		test -e ${PYVENV_DIR}; \
		${PYVENV_BINDIR}/python -m pip ${PIP_ARGS} install --upgrade pip wheel; \
	fi

${PYVENV_BINDIR}/pip-compile: ${PYVENV_DIR}/pyvenv.cfg
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install pip-tools; fi

${REQUIREMENTS_TXT}: ${REQUIREMENTS_DEPS} ${PYVENV_BINDIR}/pip-compile
	${PYVENV_BINDIR}/pip-compile -v --cache-dir "${PIP_CACHE}" --pip-args '${PIP_ARGS}' -o $@ ${REQUIREMENTS_DEPS}

sync: ${REQUIREMENTS_TXT} ${PYVENV_BINDIR}/pip-compile
	${PYVENV_BINDIR}/pip-sync --ask -v --pip-args '${PIP_ARGS}'

ci-sync: ${REQUIREMENTS_TXT} ${PYVENV_BINDIR}/pip-compile
	${PYVENV_BINDIR}/pip-sync -v --pip-args '${PIP_ARGS}'

${PYVENV_BINDIR}/flake8:
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install flake8; fi

${PYVENV_BINDIR}/pytest:
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install pytest; fi

lint: ${PYVENV_BINDIR}/flake8
## adapted from .github/workflows/python.yml
# stop the build if there are Python syntax errors or undefined names
	${PYVENV_BINDIR}/flake8 --extend-exclude src/pyfx/dispatch/oanda/models --count \
		--select=${FLAKE8_LINT_SELECT} --show-source --statistics src
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	${PYVENV_BINDIR}/flake8 --extend-exclude src/pyfx/dispatch/oanda/models --count --exit-zero \
		--extend-ignore ${FLAKE8_LINT_IGNORE} --max-line-length=127 --statistics \
		--per-file-ignores "${FLAKE8_LINT_IGNORE_PER_FILE}"  src \

tests: ${PYVENV_BINDIR}/pytest
	${PYVENV_BINDIR}/pytest test

check-tests: ${PYVENV_BINDIR}/pytest
	${PYVENV_BINDIR}/pytest --collect-only test

checks: tests lint
