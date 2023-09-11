## GNU Makefile for PyFX::Dispatch::Oanda

ifndef PYTHON
PYTHON:=		$(shell if [ -n "$(which python3 2>/dev/null)" ]; then echo python3; else echo python; fi)
endif
PYVENV_DIR?=		env
REQUIREMENTS_IN?=	requirements.in
REQUIREMENTS_TXT?=	requirements.txt
REQUIREMENTS_DEPS?=	pyproject.toml ${REQUIREMENTS_IN} $(wildcard requirements.local)
PYVENV_DEPS?=		${PYVENV_DIR}/pyvenv.cfg
PROJECT_PY?=		project.py

ifndef PYVENV_BINDIR
PYVENV_BINDIR:=		$(shell if [ "$$(${PYTHON} -c 'import sys; print(sys.platform)')" = "win32" ]; then readlink -f "${PYVENV_DIR}/Scripts"; else readlink -f "${PYVENV_DIR}/bin"; fi)
endif

FETCH?=			${PYTHON} ${PROJECT_PY} fetch
FETCH_DEPS?=		${PROJECT_PY}

all: sync

env: ${PYVENV_DIR}/pyvenv.cfg

projects: ${BUILDDIR}/oanda/pyproject.toml

requirements: ${REQUIREMENTS_TXT}

${PYVENV_DIR}/pyvenv.cfg:
	if ! [ -e "${PYVENV_DIR}" ]; then \
		${PYTHON} ${PROJECT_PY} ensure_env ${PYVENV_DIR}; \
		${PYVENV_BINDIR}/pip ${PIP_ARGS} install --upgrade pip wheel; \
	fi

${PYVENV_BINDIR}/pip-compile: ${PYVENV_DIR}/pyvenv.cfg
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install pip-tools; fi

${REQUIREMENTS_TXT}: ${REQUIREMENTS_DEPS} ${PYVENV_BINDIR}/pip-compile
	${PYVENV_BINDIR}/pip-compile -v --pip-args "${PIP_ARGS}" -o $@ ${REQUIREMENTS_DEPS}

sync: ${REQUIREMENTS_TXT} ${PYVENV_BINDIR}/pip-compile
## --no-build-isolation may prevent errors during tmpdir deletion on Windows
	${PYVENV_BINDIR}/pip-sync -v --pip-args "--no-build-isolation ${PIP_ARGS}"

${PYVENV_BINDIR}/flake8:
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install flake8; fi

${PYVENV_BINDIR}/pytest:
	if ! [ -e "${@}" ]; then ${PYVENV_BINDIR}/pip ${PIP_ARGS} install pytest; fi

lint: ${REQUIREMENTS_TXT} ${PYVENV_BINDIR}/flake8 ${PYVENV_BINDIR}/pytest
## adapted from .github/workflows/python.yml
# stop the build if there are Python syntax errors or undefined names
	${PYVENV_BINDIR}/flake8 --extend-exclude src/pyfx/dispatch/oanda/models --count --select=E9,F63,F7,F82 --show-source --statistics src
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	${PYVENV_BINDIR}/flake8 --extend-exclude src/pyfx/dispatch/oanda/models --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics src

tests: ${REQUIREMENTS_TXT} ${PYVENV_BINDIR}/pytest
	${PYVENV_BINDIR}/pytest test
