"""
pytraffic_launcher – console-script entry point installed by pip.

When the game is run via the ``pytraffic`` command after installation,
Python resolves data files relative to this module's location.  We set
the working directory to the installed share tree so that ``config.db``,
``ttraffic.levels``, themes, and libglade UI files are all found by the
same relative-path logic already present in the game modules.
"""

import os
import sys


def main() -> None:
    # Locate the installed data directory next to this launcher module.
    # After "pip install ." the layout is:
    #   <prefix>/lib/pythonX.Y/site-packages/pytraffic_launcher.py
    #   <prefix>/share/pytraffic/                 ← data root
    launcher_dir = os.path.dirname(os.path.abspath(__file__))

    # Walk up from site-packages to <prefix>, then down to share/pytraffic.
    # site-packages is typically <prefix>/lib/pythonX.Y/site-packages
    prefix = os.path.normpath(os.path.join(launcher_dir, "..", "..", ".."))
    data_dir = os.path.join(prefix, "share", "pytraffic")

    if os.path.isdir(data_dir):
        os.chdir(data_dir)
        # Make sure site-packages (where the modules live) is on sys.path
        if launcher_dir not in sys.path:
            sys.path.insert(0, launcher_dir)
    else:
        # Fallback: running from a checkout (e.g. after pip install -e .)
        src_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(src_dir)

    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("Gdk", "3.0")
    from gi.repository import Gtk
    import Game
    Game.Game()
    Gtk.main()
