import extra_path
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Game

if __name__ == '__main__':
    Game.Game()
    Gtk.main()
