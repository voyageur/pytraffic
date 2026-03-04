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

from gi.repository import Gtk, Gdk, Pango
import sys, os, copy
import time
import PropertyBag
import Hint
import Arena, Board, Misc
import History, BottomBar
import LevelSelector
import Timer
import GameState
import CondMessageBox
import Statistics
import ArtWork
import ShowHTML
import SoundServer
import MusicServer
import ThemeEngine
import Canvas
import SoundData
import traceback
import MusicChooser
import SmartLabel

np = Misc.normalize_path

class Game:
    def __init__(self):
        self.callbacks_enabled = 0
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_icon_from_file(np("libglade/carNred64x64.png"))
        self.window.set_title("PyTraffic")
        self.window.set_resizable(False)
        self.window.connect("delete_event", self.quit)
        self.window.connect("destroy", self.quit)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.add(vbox)

        self.theme_engine = ThemeEngine.ThemeEngine()
        self.create_theme_data()

        # --- Build menu bar using Gtk.MenuBar ---
        menubar = self._build_menubar()
        vbox.pack_start(menubar, False, True, 0)

        # --- Build toolbar using Gtk.Toolbar ---
        toolbar = self._build_toolbar()
        vbox.pack_start(toolbar, False, False, 0)

        statusbar = BottomBar.BottomBar(False, 0)
        self.type_label = statusbar.add(" Intermediate ")
        self.finished = statusbar.add(" Unsolved ")
        self.hints = statusbar.add(" Hint : 100 ")
        self.moves = statusbar.add(" 0/100 ")
        self.time_label = statusbar.empty
        self.time_label.set_text("")
        self.time_label.set_anchor('e')
        vbox.pack_end(statusbar, False, False, 0)

        self.sound_server = SoundServer.SoundServer(self.theme_engine)
        self.music_server = MusicServer.MusicServer(self.sound_server)
        self.music_server.connect("notify::status", self.music_status_change)
        self.music_server.connect("no_files_loaded", self.no_files_loaded)
        self.step = 0.01
        self.al = 0.5
        self.music_server.connect("progress", self.music_progress)
        self.music_chooser = MusicChooser.MusicChooser(self.theme_engine,
                                                     self.music_server)
        self.statisticsdialog = Statistics.StatisticsDialog(self.window)
        self.artwork = ArtWork.ArtWork(self)
        self.gamestate = GameState.GameState()
        self.propertybag = PropertyBag.PropertyBag(
                configfile=np(Misc.default_configfile),
                comment="This is a generated file!")

        self.arena = Arena.Arena(self)
        vbox.pack_start(self.arena, False, False, 0)
        self.arena.connect("button_press_event", self.stop_demo)
        self.window.connect("key_release_event", self.stop_demo_key)
        self.on = 1
        self.clock()
        self.timer = Timer.Timer(interval=1000)
        self.timer.connect("tick", self.clock)
        self.timer.set_running(1)
        self.demo_timer = Timer.Timer(interval=1500)
        self.demo_timer.connect("tick", self.demo_step)

        # About dialog via GtkBuilder
        self.builder = Gtk.Builder()
        self.builder.add_from_file("libglade/AboutDialog.ui")
        self.about_dialog = self.builder.get_object("AboutDialog")
        config_db = PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
        config_db.load(all=True)
        self.about_dialog.set_version("%s-%s" % (config_db["version"],
                                                 config_db["release"]))
        events = {"on_AboutDialog_response": self.about_dialog_close,
                  "on_AboutDialog_close": self.about_dialog_close,
                  "on_AboutDialog_delete_event": self.about_dialog_close
                  }
        self.builder.connect_signals(events)
        self.callbacks_enabled = 1
        self.newgame()
        self.window.show_all()

    def _build_menubar(self):
        """Build Gtk.MenuBar replacing the old gtk.ItemFactory."""
        accel_group = Gtk.AccelGroup()
        self.window.add_accel_group(accel_group)
        menubar = Gtk.MenuBar()

        # --- File menu ---
        file_menu = Gtk.Menu()
        file_item = Gtk.MenuItem(label="_File")
        file_item.set_use_underline(True)
        file_item.set_submenu(file_menu)

        self.new_ = Gtk.MenuItem(label="_New")
        self.new_.set_use_underline(True)
        self.new_.connect("activate", self.new)
        self.new_.add_accelerator("activate", accel_group,
                                  Gdk.KEY_n, Gdk.ModifierType.CONTROL_MASK,
                                  Gtk.AccelFlags.VISIBLE)
        file_menu.append(self.new_)

        stats_item = Gtk.MenuItem(label="S_tatistics")
        stats_item.set_use_underline(True)
        stats_item.connect("activate", self.show_statistics)
        stats_item.add_accelerator("activate", accel_group,
                                   Gdk.KEY_t, Gdk.ModifierType.MOD1_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        file_menu.append(stats_item)

        quit_item = Gtk.MenuItem(label="_Quit")
        quit_item.set_use_underline(True)
        quit_item.connect("activate", self.quit)
        quit_item.add_accelerator("activate", accel_group,
                                  Gdk.KEY_q, Gdk.ModifierType.MOD1_MASK,
                                  Gtk.AccelFlags.VISIBLE)
        file_menu.append(quit_item)
        menubar.append(file_item)

        # --- Edit menu ---
        edit_menu = Gtk.Menu()
        edit_item = Gtk.MenuItem(label="_Edit")
        edit_item.set_use_underline(True)
        edit_item.set_submenu(edit_menu)

        self.restart_ = Gtk.MenuItem(label="_First")
        self.restart_.set_use_underline(True)
        self.restart_.connect("activate", self.restart)
        self.restart_.add_accelerator("activate", accel_group,
                                      Gdk.KEY_b, Gdk.ModifierType.CONTROL_MASK,
                                      Gtk.AccelFlags.VISIBLE)
        edit_menu.append(self.restart_)

        self.undo_ = Gtk.MenuItem(label="_Undo")
        self.undo_.set_use_underline(True)
        self.undo_.connect("activate", self.undo)
        self.undo_.add_accelerator("activate", accel_group,
                                   Gdk.KEY_z, Gdk.ModifierType.CONTROL_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        edit_menu.append(self.undo_)

        self.redo_ = Gtk.MenuItem(label="_Redo")
        self.redo_.set_use_underline(True)
        self.redo_.connect("activate", self.redo)
        self.redo_.add_accelerator("activate", accel_group,
                                   Gdk.KEY_r, Gdk.ModifierType.CONTROL_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        edit_menu.append(self.redo_)

        self.end_ = Gtk.MenuItem(label="_End")
        self.end_.set_use_underline(True)
        self.end_.connect("activate", self.gotoend)
        self.end_.add_accelerator("activate", accel_group,
                                  Gdk.KEY_e, Gdk.ModifierType.CONTROL_MASK,
                                  Gtk.AccelFlags.VISIBLE)
        edit_menu.append(self.end_)
        menubar.append(edit_item)

        # --- Settings menu ---
        settings_menu = Gtk.Menu()
        settings_item = Gtk.MenuItem(label="_Settings")
        settings_item.set_use_underline(True)
        settings_item.set_submenu(settings_menu)

        # Difficulty submenu
        diff_menu = Gtk.Menu()
        diff_item = Gtk.MenuItem(label="_Difficulty")
        diff_item.set_use_underline(True)
        diff_item.set_submenu(diff_menu)

        self.trivial_ = Gtk.RadioMenuItem(label="_Trivial")
        self.trivial_.set_use_underline(True)
        self.trivial_.connect("toggled", self.settype, 0)
        diff_menu.append(self.trivial_)

        self.easy_ = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(
            self.trivial_, "_Easy")
        self.easy_.connect("toggled", self.settype, 1)
        diff_menu.append(self.easy_)

        self.intermediate_ = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(
            self.trivial_, "_Intermediate")
        self.intermediate_.connect("toggled", self.settype, 2)
        diff_menu.append(self.intermediate_)

        self.advanced_ = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(
            self.trivial_, "_Advanced")
        self.advanced_.connect("toggled", self.settype, 3)
        diff_menu.append(self.advanced_)

        self.expert_ = Gtk.RadioMenuItem.new_with_mnemonic_from_widget(
            self.trivial_, "_Expert")
        self.expert_.connect("toggled", self.settype, 4)
        diff_menu.append(self.expert_)

        settings_menu.append(diff_item)
        settings_menu.append(Gtk.SeparatorMenuItem())

        self.warningsmode_ = Gtk.CheckMenuItem(label="_Warnings")
        self.warningsmode_.set_use_underline(True)
        self.warningsmode_.connect("toggled", self.setwarningsmode)
        settings_menu.append(self.warningsmode_)

        settings_menu.append(Gtk.SeparatorMenuItem())

        # Theme submenu
        theme_menu_item = Gtk.MenuItem(label="_Theme")
        theme_menu_item.set_use_underline(True)
        theme_menu = Gtk.Menu()
        theme_menu_item.set_submenu(theme_menu)
        first_theme_item = None
        for data in self.theme_data:
            if first_theme_item is None:
                item = Gtk.RadioMenuItem(label=data['menu_label'])
                first_theme_item = item
            else:
                item = Gtk.RadioMenuItem.new_from_widget(first_theme_item)
                item.set_label(data['menu_label'])
            item.connect("toggled", self.settheme, data['action'])
            data['menu_item'] = item
            theme_menu.append(item)
        settings_menu.append(theme_menu_item)

        settings_menu.append(Gtk.SeparatorMenuItem())

        self.sound_ = Gtk.CheckMenuItem(label="_Sound")
        self.sound_.set_use_underline(True)
        self.sound_.connect("toggled", self.setsound)
        settings_menu.append(self.sound_)

        self.music_ = Gtk.CheckMenuItem(label="_Music")
        self.music_.set_use_underline(True)
        self.music_.connect("toggled", self.setmusic)
        settings_menu.append(self.music_)

        self.choose_music_ = Gtk.MenuItem(label="_Choose Music")
        self.choose_music_.set_use_underline(True)
        self.choose_music_.connect("activate", self.choosemusic)
        settings_menu.append(self.choose_music_)

        # Sound output submenu (Unix only)
        if os.name != 'nt':
            sound_output_item = Gtk.MenuItem(label="Sound _output")
            sound_output_item.set_use_underline(True)
            sound_output_menu = Gtk.Menu()
            sound_output_item.set_submenu(sound_output_menu)
            first_sound_item = None
            for data in SoundData.sound_data:
                if first_sound_item is None:
                    item = Gtk.RadioMenuItem(label=data['menu_label'])
                    first_sound_item = item
                else:
                    item = Gtk.RadioMenuItem.new_from_widget(first_sound_item)
                    item.set_label(data['menu_label'])
                item.connect("toggled", self.setsoundoutput, data['action'])
                data['menu_item'] = item
                sound_output_menu.append(item)
            sound_output_menu.append(Gtk.SeparatorMenuItem())
            self.soundabout_ = Gtk.MenuItem(label="What is this about?")
            self.soundabout_.connect("activate", self.showsounddoc)
            sound_output_menu.append(self.soundabout_)
            settings_menu.append(sound_output_item)

        menubar.append(settings_item)

        # --- Help menu ---
        help_menu = Gtk.Menu()
        help_item = Gtk.MenuItem(label="_Help")
        help_item.set_use_underline(True)
        help_item.set_submenu(help_menu)

        self.hint_ = Gtk.MenuItem(label="H_int")
        self.hint_.set_use_underline(True)
        self.hint_.connect("activate", self.hint)
        self.hint_.add_accelerator("activate", accel_group,
                                   Gdk.KEY_i, Gdk.ModifierType.MOD1_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        help_menu.append(self.hint_)

        self.demo_ = Gtk.CheckMenuItem(label="_Demo")
        self.demo_.set_use_underline(True)
        self.demo_.connect("toggled", self.setdemomode)
        self.demo_.add_accelerator("activate", accel_group,
                                   Gdk.KEY_d, Gdk.ModifierType.CONTROL_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        help_menu.append(self.demo_)

        self.readme_ = Gtk.MenuItem(label="_Show readme")
        self.readme_.set_use_underline(True)
        self.readme_.connect("activate", self.readme)
        help_menu.append(self.readme_)

        about_item = Gtk.MenuItem(label="_About")
        about_item.set_use_underline(True)
        about_item.connect("activate", self.about)
        about_item.add_accelerator("activate", accel_group,
                                   Gdk.KEY_h, Gdk.ModifierType.CONTROL_MASK,
                                   Gtk.AccelFlags.VISIBLE)
        help_menu.append(about_item)
        menubar.append(help_item)

        return menubar

    def _build_toolbar(self):
        """Build Gtk.Toolbar replacing deprecated insert_stock."""
        toolbar = Gtk.Toolbar()

        self.new_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        self.new_button.set_tooltip_text("New level")
        self.new_button.connect("clicked", self.new)
        toolbar.insert(self.new_button, -1)

        self.restart_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GOTO_FIRST)
        self.restart_button.set_tooltip_text("Restart level")
        self.restart_button.connect("clicked", self.restart)
        toolbar.insert(self.restart_button, -1)

        self.undo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        self.undo_button.set_tooltip_text("Undo last move")
        self.undo_button.connect("clicked", self.undo)
        toolbar.insert(self.undo_button, -1)

        self.redo_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REDO)
        self.redo_button.set_tooltip_text("Redo last move")
        self.redo_button.connect("clicked", self.redo)
        toolbar.insert(self.redo_button, -1)

        self.end_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GOTO_LAST)
        self.end_button.set_tooltip_text("Goto end of history")
        self.end_button.connect("clicked", self.gotoend)
        toolbar.insert(self.end_button, -1)

        self.hint_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_HELP)
        self.hint_button.set_tooltip_text("Ask for hint")
        self.hint_button.connect("clicked", self.hint)
        toolbar.insert(self.hint_button, -1)

        return toolbar

    def music_status_change(self, *args):
        if self.music_server.get_status() == MusicServer.BUSY:
            self.time_label.set_anchor()
            self.time_label.set_text("finding music")
        else:
            self.clock()

    def music_progress(self, *args):
        if self.al >= 1.0 or self.al <= 0.0:
            self.step = -self.step
        self.al += self.step
        self.time_label.label.set_halign(
            Gtk.Align.START if self.al < 0.5 else Gtk.Align.END)

    def stop_demo_key(self, widget, event, *args):
        if not(event.get_state() & Gdk.ModifierType.MODIFIER_MASK) and \
               event.keyval & 255 == 27:  # compare with ESC
            self.demomode = 0
            self.updateGUI()

    def stop_demo(self, widget, event, *args):
        self.demomode = 0
        self.updateGUI()

    def create_theme_data(self):
        self.theme_data = []
        for theme in self.theme_engine.getavailable_themes():
            self.theme_data.append({'id': theme,
                                    'menu_label': theme,
                                    'action': len(self.theme_data),
                                    'menu_item': None})

    def readme(self, *args):
        ShowHTML.showhtml("doc/readme.htm")

    def showsounddoc(self, *args):
        ShowHTML.showhtml("doc/sound.htm")

    def demo_step(self, timer):
        if self.gamestate.redcarout():
            self.new()
        else:
            self.hint()
            if self.gamestate.redcarout():
                self.doredcarout()


    def enable_easteregg(self, *args):
        print("Enabling easter egg")
        self.gamestate.easteregg = 1

    def show_statistics(self, *args):
        if self.callbacks_enabled:
            self.statisticsdialog.show()
            self.updateGUI()

    def setwarningsmode(self, menu, *args):
        if self.callbacks_enabled:
            if menu.get_active() == True:
                self.expertmode = 0
            else:
                self.expertmode = 1

    def setsound(self, menu, *args):
        if self.callbacks_enabled:
            if menu.get_active() == True:
                self.sound_server.enable_sound()
            else:
                self.sound_server.disable_sound()

    def setsoundoutput(self, menu, soundoutput, *args):
        if self.callbacks_enabled:
            if os.name != 'nt' and menu.get_active():
                for data in SoundData.sound_data:
                    if data['action'] == soundoutput:
                        if self.sound_server.getsoundoutput() != data['id']:
                            self.sound_server.setsoundoutput(data['id'])
                            CondMessageBox.showwarning(
                                message="This change will only take effect after you restart PyTraffic.",
                                window=self.window)

    def setmusic(self, *args):
        if self.callbacks_enabled:
            if self.music_.get_active() == True:
                self.music_server.set_playing(1)
            else:
                self.music_server.set_playing(0)

    def no_files_loaded(self, *arg):
        CondMessageBox.showwarning(
               message="""\
You have selected no playable music.
Reverting to previous selection.

Note: wav, ogg and mod are usually
supported. Because of license issues
it is often not possible to play mp3
files.
""",
               window=self.window)

    def choosemusic(self, *args):
        self.music_chooser.run()

    def settheme(self, menu, theme_action, *args):
        if self.callbacks_enabled and menu.get_active():
            for data in self.theme_data:
                if data['action'] == theme_action:
                    if data['id'] != self.theme_engine.gettheme():
                        self.theme_engine.settheme(data['id'])
                        self.artwork.theme_change()
                        self.arena.setupboard()
            self.updateGUI()

    def setdemomode(self, menu, *args):
        if self.callbacks_enabled:
            if menu.get_active() == True:
                self.demomode = 1
            else:
                self.demomode = 0
            self.updateGUI()

    def clock(self, *args):
        if self.music_server.get_status() == MusicServer.FREE:
            self.time_label.set_anchor('e')
            if self.on:
                format = "%H:%M"
            else:
                format = "%H:%M"
            self.on = not(self.on)
            strtime = time.strftime(format, time.localtime(time.time()))
            self.time_label.set_text(strtime)

    def about_dialog_close(self, *args):
        self.about_dialog.hide()
        return True

    def about(self, *args):
        self.about_dialog.show()
        return True

    def new(self, action=None, menu=None):
        if self.demomode:
            self.gamestate.new(existing=1)
            self.arena.setupboard()
            self.updateGUI()
            return
        reply = 0
        if not(self.gamestate.youvewon):
            reply = CondMessageBox.askyesno(
                message="Do you want to abandon the current level?",
                window=self.window,
                disable=self.expertmode or self.demomode)
        if self.gamestate.youvewon or reply:
            availableslots = self.gamestate.offsetsavailable(
                                         self.gamestate.type)
            existing = 0
            if not(availableslots):
                resetpermission = CondMessageBox.askyesno(
                      message="No more unsolved levels of the requested \
type! Do you want to reset these levels?",
                      window=self.window,
                      disable=0)
                if resetpermission:
                    self.gamestate.resetsolvedlevels(self.gamestate.type)
                else:
                    existing = 1
            self.gamestate.new(existing)
            self.arena.setupboard()
            self.updateGUI()

    def newgame(self):
        something_bad_happened = 0
        last_error = ""
        try:
            self.default_all()
            self.propertybag.load()
            self.load_all()
        except Exception as e:
            something_bad_happened = 1
            last_error = str(e)
            print("Exception in newgame", last_error)
        if something_bad_happened:
            Misc.save_configfile()
            self.default_all()
            self.load_all()
            CondMessageBox.showwarning(
                   message="""There was a fatal error in the savefile: %s.
It will be replaced by an empty one.
I have tried to save a copy as: %s.
The error was: %s. """ % (Misc.default_configfile, Misc.backup_configfile, last_error),
                   window=self.window)

        if (not self.sound_server.sound_works()) and self.sound_server.sound_has_worked():
            CondMessageBox.showwarning(
                message="""There was an error while initializing the sound. Please consult the readme file (via the Help menu)
The error was: """+self.sound_server.last_error(),
                window=self.window)
        if not Hint.hint_enabled:
            CondMessageBox.showwarning(
                message="""There was an error while initializing the help and demo features. Please consult the readme file (via the Help menu).
The error was: """+Hint.last_error(),
                window=self.window)
        if not ShowHTML.can_display_html():
            CondMessageBox.showwarning(
                message="""I don't seem to know how to display html on your system.
PyTraffic reported: """+ShowHTML.last_error(),
                window=self.window)

    def hint(self, *args):
        self.arena.setanimation(True)
        confirmation = 0
        if not(self.gamestate.youvewon) and not(self.gamestate.dontinsert):
            confirmation = CondMessageBox.askokcancel(
                    message="If you use a hint now the level can no longer be recorded as solved!",
                    window=self.window,
                    disable=self.expertmode or self.demomode)
        else:
            confirmation = 1
        if confirmation:
            if not(self.gamestate.youvewon):
                self.gamestate.dontinsert = 1
                self.gamestate.hint = self.gamestate.hint+1
            index, row, col = self.gamestate.findbestmove()
            self.arena.domove(index, row, col)
            self.arena.carlist[index].move(row, col)
            if self.gamestate.redcarout():
                self.doredcarout()
        self.arena.setanimation(False)

    def doredcarout(self):
        if not(self.gamestate.youvewon or self.demomode):
            self.sound_server.play(self.artwork.getapplause())
            if self.gamestate.hint == 0 and \
                    self.gamestate.bestyoucando-1 == self.gamestate.nrofmovestaken():
                CondMessageBox.showinfo(
                         message="Congratulations...you found the shortest possible solution to this level!",
                         window=self.window,
                         disable=self.expertmode)
            elif self.gamestate.hint == 0:
                CondMessageBox.showinfo(
                         message="Congratulations...you solved this level!",
                         window=self.window,
                         disable=self.expertmode)
            else:
                CondMessageBox.showinfo(
                       message="You solved this level...now next time try to do it all by yourself:-)",
                       window=self.window,
                       disable=self.expertmode)
            self.gamestate.won()
        elif self.demomode:
            self.gamestate.won()
        self.save_all()
        self.updateGUI()

    def settype(self, menu, type_id, *args):
        if self.callbacks_enabled and menu.get_active():
            type_dict = {0: "Trivial", 1: "Easy", 2: "Intermediate", 3: "Advanced",
                         4: "Expert"}
            type = type_dict[type_id]
            # Selection of radio items generates two events.
            # One for the deselected one and one for the newly selected one.
            if type != self.gamestate.type:
                if self.demomode:
                    self.gamestate.type = type
                    self.gamestate.new(existing=1)
                    self.arena.setupboard()
                    self.updateGUI()
                    return
                reply = 0
                if not(self.gamestate.youvewon):
                    reply = CondMessageBox.askyesno(
                           message="Do you want to abandon the current level?",
                           window=self.window,
                           disable=self.expertmode or self.demomode)
                if reply or self.gamestate.youvewon:
                    availableslots = self.gamestate.offsetsavailable(type)
                    existing = 0
                    if not(availableslots):
                        resetpermission = CondMessageBox.askyesno(
                                 message="No more unsolved levels of the requested type! Do you want to reset these levels?",
                                 window=self.window,
                                 disable=0)
                        if resetpermission:
                            self.gamestate.resetsolvedlevels(type)
                        else:
                            existing = 1
                    self.gamestate.type = type
                    self.gamestate.new(existing)
                    self.arena.setupboard()
            self.updateGUI()

    def restart(self, *args):
        self.arena.restart()

    def gotoend(self, *args):
        self.arena.gotoend()

    def redo(self, *args):
        if not self.gamestate.endofhistory():
            self.arena.redo()

    def undo(self, *args):
        if not self.gamestate.startofhistory():
            self.arena.undo()

    def updateGUI(self):
        self.callbacks_enabled = 0
        if self.expertmode:
            self.warningsmode_.set_active(False)
        else:
            self.warningsmode_.set_active(True)
        for data in self.theme_data:
            if data['id'] == self.theme_engine.gettheme():
                data['menu_item'].set_active(True)
        self.moves.set_text("%d/%d" % (self.gamestate.nrofmovestaken(),
                                  self.gamestate.bestyoucando-1))
        type_dict = {"Trivial" : self.trivial_, "Easy": self.easy_,
                     "Intermediate": self.intermediate_,
                     "Advanced" : self.advanced_,
                     "Expert": self.expert_}
        type_dict[self.gamestate.type].set_active(True)
        self.type_label.set_text(self.gamestate.type)
        if not self.gamestate.youvewon:
            self.finished.set_text("Unsolved")
            rgba = Gdk.RGBA()
            rgba.parse("red")
            self.finished.modify_bg(rgba)
        elif self.gamestate.hint:
            self.finished.set_text("Solved: %d" % \
                            self.gamestate.solvedinnrofmoves)
            rgba = Gdk.RGBA()
            rgba.parse("orange")
            self.finished.modify_bg(rgba)
        else:
            self.finished.set_text("Solved: %d" % \
                            self.gamestate.solvedinnrofmoves)
            rgba = Gdk.RGBA()
            rgba.parse("green")
            self.finished.modify_bg(rgba)
        self.statisticsdialog.update_statistics(self.gamestate.statistics)
        if os.name != 'nt':
            for data in SoundData.sound_data:
                if data['id'] == self.sound_server.getsoundoutput():
                    data['menu_item'].set_active(True)
        if self.sound_server.sound_enabled():
            self.sound_.set_active(True)
        else:
            self.sound_.set_active(False)
        if self.music_server.get_playing():
            self.music_.set_active(True)
        else:
            self.music_.set_active(False)

        if self.theme_engine.theme_has_sound():
            self.sound_.set_sensitive(True)
        else:
            self.sound_.set_sensitive(False)
            self.sound_.set_active(False)

        if not self.sound_server.sound_works():
            self.sound_.set_sensitive(False)
            self.music_.set_sensitive(False)
            self.choose_music_.set_sensitive(False)
        if not ShowHTML.can_display_html():
            self.readme_.set_sensitive(False)
            if os.name != 'nt':
                self.soundabout_.set_sensitive(False)
        if self.demomode:
            self.demo_.set_active(True)
            self.hint_button.set_sensitive(False)
            self.hint_.set_sensitive(False)
            self.arena.disable()
            self.undo_button.set_sensitive(False)
            self.undo_.set_sensitive(False)
            self.restart_button.set_sensitive(False)
            self.restart_.set_sensitive(False)
            self.redo_button.set_sensitive(False)
            self.redo_.set_sensitive(False)
            self.end_button.set_sensitive(False)
            self.end_.set_sensitive(False)
            self.new_button.set_sensitive(False)
            self.new_.set_sensitive(False)
            self.hints.set_text("Demo")
            rgba = Gdk.RGBA()
            rgba.parse("yellow")
            self.hints.modify_bg(rgba)
            self.demo_timer.set_running(1)
        else:
            if not(Hint.hint_enabled):
                self.demo_.set_sensitive(False)
                self.trivial_.set_sensitive(False)
                self.easy_.set_sensitive(False)
            else:
                self.demo_.set_active(False)
            self.new_.set_sensitive(True)
            self.new_button.set_sensitive(True)
            if self.gamestate.redcarout():
                self.arena.disable()
            else:
                self.arena.enable()
            if not(Hint.hint_enabled) or self.gamestate.redcarout():
                self.hint_button.set_sensitive(False)
                self.hint_.set_sensitive(False)
            else:
                self.hint_button.set_sensitive(True)
                self.hint_.set_sensitive(True)
            if self.gamestate.startofhistory():
                self.undo_button.set_sensitive(False)
                self.undo_.set_sensitive(False)
                self.restart_button.set_sensitive(False)
                self.restart_.set_sensitive(False)
            else:
                self.restart_button.set_sensitive(True)
                self.restart_.set_sensitive(True)
                self.undo_button.set_sensitive(True)
                self.undo_.set_sensitive(True)
            if self.gamestate.endofhistory():
                self.redo_button.set_sensitive(False)
                self.redo_.set_sensitive(False)
                self.end_button.set_sensitive(False)
                self.end_.set_sensitive(False)
            else:
                self.redo_button.set_sensitive(True)
                self.redo_.set_sensitive(True)
                self.end_button.set_sensitive(True)
                self.end_.set_sensitive(True)
            self.hints.set_text("Hint: %d" % self.gamestate.hint)
            if self.gamestate.hint:
                rgba = Gdk.RGBA()
                rgba.parse("orange")
                self.hints.modify_bg(rgba)
            else:
                self.hints.reset_bg()
            self.demo_timer.set_running(0)
        self.arena.update_cursors()
        self.callbacks_enabled = 1

    def quit(self, *args):
        self.save_all()
        Gtk.main_quit()
        # there is a problem with using sys.exit() if the program has
        # been suspended while the music is playing.
        os._exit(0)


    def save_all(self):
        self.artwork.save_bag(self.propertybag)
        self.theme_engine.save_bag(self.propertybag)
        self.gamestate.save_bag(self.propertybag)
        self.statisticsdialog.save_bag(self.propertybag)
        self.sound_server.save_bag(self.propertybag)
        self.music_server.save_bag(self.propertybag)
        self.arena.save_bag(self.propertybag)
        self.propertybag['expertmode'] = self.expertmode
        self.propertybag.save()

    def default_all(self):
        self.theme_engine.default_bag(self.propertybag)
        self.sound_server.default_bag(self.propertybag)
        self.music_server.default_bag(self.propertybag)
        self.artwork.default_bag(self.propertybag)
        self.gamestate.default_bag(self.propertybag)
        self.statisticsdialog.default_bag(self.propertybag)
        self.arena.default_bag(self.propertybag)
        self.propertybag['expertmode'] = 0
        self.propertybag['demomode'] = 0

    def load_all(self):
        self.callbacks_enabled = 0
        self.theme_engine.load_bag(self.propertybag)
        self.sound_server.load_bag(self.propertybag)
        self.music_server.load_bag(self.propertybag)
        self.artwork.load_bag(self.propertybag)
        self.gamestate.load_bag(self.propertybag)
        self.arena.load_bag(self.propertybag)
        self.arena.setupboard()
        self.expertmode = self.propertybag['expertmode']
        self.statisticsdialog.load_bag(self.propertybag)
        self.demomode = 0
        self.callbacks_enabled = 1
        self.updateGUI()

if __name__ == '__main__':
    Game()
    Gtk.main()
