## PyTraffic -- A python simulation of the game Rush Hour invented by
## Nob Yoshigahara and commercialized by Binary Arts Corporation.
##
## Copyright (C) 2001-2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING.
## If not, write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##


import os
import Misc
from gi.repository import Gtk
from gi.repository import GObject
import Chooser

np=Misc.normalize_path

class MusicChooser:

    def __init__(self,theme_engine,music_server):
        settings=Gtk.Settings.get_default()
        self.builder=Gtk.Builder()
        self.builder.add_from_file("libglade/MusicDialog.ui")
        self.dialog=self.builder.get_object("ChooseMusicDialog")
        self.chosen_location=self.builder.get_object("chosen_location")
        self.browse_button=self.builder.get_object("browse_button")
        self.advanced_button=self.builder.get_object("advanced_button")
        self.shuffle_button=self.builder.get_object("shuffle_button")
        self.recursive_button=self.builder.get_object("recursive_button")
        self.use_extensions_button=self.builder.get_object("use_extensions_button")
        self.browse_image=self.builder.get_object("browse_image")
        self.default_image=self.builder.get_object("default_image")
        if not settings.get_property("gtk_button_images"):
            self.browse_image.destroy()
            self.default_image.destroy()
	
        events={"on_browse_button_clicked" : self.browse,
              "on_default_button_clicked": self.default,
              "on_cancel_button_clicked" : self.cancel,
              "on_ok_button_clicked"     : self.ok,
              "on_chosen_location_activate" : self.ok,
              "on_ChooseMusicDialog_delete_event" : self.cancel}
        self.builder.connect_signals(events)
        self.theme_engine=theme_engine
        self.music_server=music_server
        self.create_browser()
        self.myloop=GObject.MainLoop()

    def create_browser(self):
        self.builder.add_from_file("libglade/MusicBrowser.ui")
        events1={"on_music_browser_cancel_button_clicked" :
                 self.music_browser_cancel,
                 "on_music_browser_open_button_clicked" :
                 self.music_browser_open,
                 "on_music_browser_select_button_clicked" :
                 self.music_browser_select,
                 "on_MusicBrowser_delete_event":
                 self.music_browser_cancel,
                 "on_MusicBrowser_close":
                 self.music_browser_cancel,
                 "on_MusicBrowser_response":
                 self.music_browser_response}
        self.builder.connect_signals(events1)
        self.music_browser=self.builder.get_object("MusicBrowser")
		
        
    def run(self):
        self.browse_button.grab_focus()
        self.advanced_button.set_expanded(False)
        self.chosen_location.set_text(\
            os.path.abspath(self.music_server.get_music_path()))
        if self.music_server.get_strategy()==Chooser.RANDOM:
            self.shuffle_button.set_active(1)
        else:
            self.shuffle_button.set_active(0)
        if self.music_server.get_recursive():
            self.recursive_button.set_active(1)
        else:
            self.recursive_button.set_active(0)
        if self.music_server.get_use_extensions():
            self.use_extensions_button.set_active(1)
        else:
            self.use_extensions_button.set_active(0)
        self.dialog.show_all()
        self.myloop.run()

    def browse(self, *args):
        path=os.path.abspath(self.chosen_location.get_text())
        self.music_browser.select_filename(path)
        self.music_browser.run()
        return True

    def default(self, *args):
        self.chosen_location.set_text(\
            os.path.abspath(self.theme_engine.default_music_path()[0]))
        self.use_extensions_button.set_active(True)
        self.music_server.set_use_extensions(True)
        return True
        

    def cancel(self, *args):
        self.dialog.hide()
        self.myloop.quit()
        return True

    def ok(self, *args):
        if self.shuffle_button.get_active():
            self.music_server.set_strategy(Chooser.RANDOM)
        else:
            self.music_server.set_strategy(Chooser.REPEAT)
        if self.recursive_button.get_active():
            self.music_server.set_recursive(True)
        else:
            self.music_server.set_recursive(False)
        if self.use_extensions_button.get_active():
            self.music_server.set_use_extensions(True)
        else:
            self.music_server.set_use_extensions(False)
        path=self.chosen_location.get_text()
        self.music_server.load([path])
        self.cancel()
        return True

    def music_browser_cancel(self,*args):
        self.music_browser.hide()
        return True

    def music_browser_response(self,*args):
        return True
        
    def music_browser_open(self,*args):
        selection=self.music_browser.get_filename()
        if selection and not os.path.isdir(selection):
            self.music_browser_select()
        return True

    def music_browser_select(self,*args):
        selection=self.music_browser.get_filename()
        if selection:
            self.chosen_location.set_text(selection)
            self.music_browser_cancel()
        return True
