import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Misc
import PropertyBag

# Allow a config.db 'add_path' key to inject extra directories (install-time
# override; key is absent in the normal shipped config.db).
try:
    _config_db = PropertyBag.PropertyBag(
        configfile=Misc.normalize_path(Misc.default_config_db))
    _config_db.load(all=True)
    for _p in _config_db.get("add_path", []):
        sys.path.append(_p)
except Exception:
    pass

import Game

if __name__ == '__main__':
    Game.Game()
    Gtk.main()
