import extra_path
import os
import sys
os.environ['LANG']='C'
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
import Game
Game.Game()
Gtk.main()
