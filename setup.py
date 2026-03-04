"""
setup.py – dynamic portions of the build that cannot be expressed in
pyproject.toml:

  * The _hint C extension (source file list)
  * data_files with glob patterns (themes, icons, …)

All static metadata lives in pyproject.toml.  Run:

    pip install .                  # build + install
    pip install -e .               # editable install (no C extension inplace)
    python setup.py build_ext --inplace   # build _hint.so in the project root
"""

import glob
import os
from setuptools import Extension, setup

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def theme_files(theme_dir, install_base="share/pytraffic"):
    """Return data_files entries for one theme directory."""
    entries = []
    base = os.path.basename(theme_dir)
    parent = os.path.basename(os.path.dirname(theme_dir))
    inst = os.path.join(install_base, parent, base)

    for sub in ("cars", "background", "sound"):
        src_dir = os.path.join(theme_dir, sub)
        if not os.path.isdir(src_dir):
            continue
        files = (
            glob.glob(os.path.join(src_dir, "*.png"))
            + glob.glob(os.path.join(src_dir, "*.ogg"))
            + glob.glob(os.path.join(src_dir, "basepoints"))
        )
        if files:
            entries.append((os.path.join(inst, sub), files))

    # top-level transform file (not all themes have it)
    top_files = glob.glob(os.path.join(theme_dir, "transform"))
    if top_files:
        entries.append((inst, top_files))

    return entries


# ---------------------------------------------------------------------------
# C extension
# ---------------------------------------------------------------------------

ext_modules = [
    Extension(
        "_hint",
        sources=[
            "src/hint/globals.c",
            "src/hint/asci.c",
            "src/hint/debug.c",
            "src/hint/hint.c",
            "src/hint/masterfile.c",
            "src/hint/base.c",
            "src/hint/extract.c",
            "src/hint/gtraffic.c",
            "src/hint/hint_wrap.c",
            "src/hint/precompute.c",
        ],
    )
]

# ---------------------------------------------------------------------------
# Data files
# ---------------------------------------------------------------------------

INST = "share/pytraffic"

data_files = [
    # Core data
    (INST, ["ttraffic.levels", "COPYING", "config.db"]),
    (f"{INST}/doc", glob.glob("doc/*.htm") + glob.glob("doc/*.png")),
    (
        f"{INST}/libglade",
        glob.glob("libglade/*.ui") + ["libglade/carNred64x64.png"],
    ),
    (f"{INST}/music", ["music/README.README", "music/Ranger_Song.ogg"]),
    (f"{INST}/sound_test", ["sound_test/tone.ogg"]),
    # Desktop integration
    ("share/applications", ["pytraffic.desktop"]),
    ("share/icons/hicolor/32x32/apps", ["icons/32x32/pytraffic.png"]),
    ("share/icons/hicolor/48x48/apps", ["icons/48x48/pytraffic.png"]),
    ("share/icons/hicolor/64x64/apps", ["icons/64x64/pytraffic.png"]),
]

# Themes (one bundled + five extras)
for theme_path in sorted(
    glob.glob("themes/*") + glob.glob("extra_themes/*")
):
    if os.path.isdir(theme_path):
        data_files.extend(theme_files(theme_path))

# ---------------------------------------------------------------------------
# setup() – only the dynamic parts; metadata comes from pyproject.toml
# ---------------------------------------------------------------------------

setup(
    ext_modules=ext_modules,
    data_files=data_files,
)
