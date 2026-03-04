# Makefile – convenience targets for PyTraffic development
#
# All game data (themes, music, UI files, …) is already in the checkout, so
# the only thing that needs compiling before running from the source tree is
# the _hint C extension.
#
# Common workflows
# ----------------
#   make            → build _hint.so in the project root (same as 'make build')
#   make run        → build then launch the game
#   make install    → install into the active Python environment via pip
#   make install-user → install into ~/.local (no root required)
#   make clean      → remove build artefacts (keeps the inplace .so)
#   make distclean  → full clean including the inplace .so

PYTHON   ?= python3
PIP      ?= $(PYTHON) -m pip

# Detect the in-place extension name from Python's sysconfig so this works
# across CPython versions and architectures.
EXT_SUFFIX := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
HINT_SO    := _hint$(EXT_SUFFIX)

.PHONY: all build run install install-user clean distclean

all: build

## build: compile _hint C extension into the project root (for running in-place)
build: $(HINT_SO)

$(HINT_SO): src/hint/globals.c src/hint/asci.c src/hint/debug.c \
            src/hint/hint.c src/hint/masterfile.c src/hint/base.c \
            src/hint/extract.c src/hint/gtraffic.c src/hint/hint_wrap.c \
            src/hint/precompute.c
	$(PYTHON) setup.py build_ext --inplace
	@echo "Built: $(HINT_SO)"

## run: build the extension then launch the game
run: build
	$(PYTHON) Main.py

## install: build and install into the active Python environment
install:
	$(PIP) install .

## install-user: install into ~/.local (no root needed)
install-user:
	$(PIP) install --user .

## clean: remove setuptools build/ directory but keep the inplace .so
clean:
	rm -rf build/ *.egg-info/ dist/ __pycache__/ pytraffic.egg-info/
	find src -name '*.o' -delete

## distclean: full clean including the compiled extension
distclean: clean
	rm -f $(HINT_SO)
