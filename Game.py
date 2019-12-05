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

from gi.repository import Gtk
from gi.repository import Pango
import sys,os,string,copy
import time
import PropertyBag
import Hint
import Arena,Board,Misc
import History,BottomBar
import LevelSelector
import ConfigParser
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

np=Misc.normalize_path

class Game:
    def __init__(self):
        self.callbacks_enabled=0
        self.window=Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_icon_from_file(np("libglade/carNred64x64.png"))
        self.window.set_title("PyTraffic")
        self.window.set_resizable(False)
        self.window.connect("delete_event",self.quit)
        self.window.connect("destroy",self.quit)
        vbox=Gtk.VBox(False,0)
        self.window.add(vbox)
        sound_menu=self.construct_sound_menu()
        self.theme_engine=ThemeEngine.ThemeEngine()
        self.create_theme_data()
        theme_menu=self.construct_theme_menu()
        """ TODO these need to be updated to modern framework
        self.menu_items=(
            ("/_File",None,None,0,"<Branch>"),
            ( "/File/_New","<control>N",self.new,0,None),
            ( "/File/S_tatistics","<alt>T",self.show_statistics,0,None),
            ( "/File/_Quit","<alt>Q",self.quit,0,None),
            ("/_Edit",None,None,0,"<Branch>"),
            ("/Edit/_First","<control>B",self.restart,0,None),
            ("/Edit/_Undo","<control>Z",self.undo,0,None),
            ("/Edit/_Redo","<control>R",self.redo,0,None),
            ("/Edit/_End","<control>E",self.gotoend,0,None),
            ("/_Settings",None,None,0,"<Branch>"),
            ("/Settings/_Difficulty",None,None,0,"<Branch>" ),
            ("/Settings/Difficulty/_Trivial",None,self.settype,0,"<RadioItem>"),
            ("/Settings/Difficulty/_Easy",None,self.settype,1,
                                          "/Settings/Difficulty/Trivial"),
            ("/Settings/Difficulty/_Intermediate",None,self.settype,2,
                                          "/Settings/Difficulty/Trivial"),
            ("/Settings/Difficulty/_Advanced",None,self.settype,3,
                                          "/Settings/Difficulty/Trivial"),
            ("/Settings/Difficulty/_Expert",None,self.settype,4,
                                          "/Settings/Difficulty/Trivial"),
            ("/Settings/Dummy",None,None,0,"<Separator>"),
            ("/Settings/_Warnings",None,self.setwarningsmode,0,"<CheckItem>"))\
            + theme_menu +\
            (("/Settings/Dummy",None,None,0,"<Separator>"),
            ("/Settings/_Sound",None,self.setsound,0,"<CheckItem>"),
            ("/Settings/_Music",None,self.setmusic,0,"<CheckItem>"),
             ("/Settings/_Choose Music",None,self.choosemusic,0,None))\
            + sound_menu +\
            (("/_Help",None,None,0,"<Branch>"),
            ("/Help/H_int","<alt>I",self.hint,0,None),
            ("/Help/_Demo","<control>D",self.setdemomode,0,"<CheckItem>"),
            ("/Help/_Show readme",None,self.readme,0,None),
            ("/Help/_About","<control>H",self.about,0,None)
            )
        accel_group=Gtk.AccelGroup()
        self.item_factory=item_factory=Gtk.ItemFactory(Gtk.MenuBar, 
                                                       "<main>", 
                                                       accel_group)
        item_factory.create_items(self.menu_items)
        self.window.add_accel_group(accel_group)
        menubar=item_factory.get_widget("<main>")
        vbox.pack_start(menubar, False, True, 0)
        self.extract_sound_menu_items(item_factory)
        self.extract_theme_menu_items(item_factory)
        self.new_=item_factory.get_widget("/File/New")
        self.restart_=item_factory.get_widget("/Edit/First")
        self.undo_=item_factory.get_widget("/Edit/Undo")
        self.redo_=item_factory.get_widget("/Edit/Redo")
        self.end_=item_factory.get_widget("/Edit/End")
        self.trivial_=item_factory.get_widget("/Settings/Difficulty/Trivial")
        self.easy_=item_factory.get_widget("/Settings/Difficulty/Easy")
        self.intermediate_=item_factory.get_widget(\
                                       "/Settings/Difficulty/Intermediate")
        self.advanced_=item_factory.get_widget("/Settings/Difficulty/Advanced")
        self.expert_=item_factory.get_widget("/Settings/Difficulty/Expert")
        self.animation_=item_factory.get_widget("/Settings/Animation")
        self.warningsmode_=item_factory.get_widget("/Settings/Warnings")
        self.sound_=item_factory.get_widget("/Settings/Sound")
        self.music_=item_factory.get_widget("/Settings/Music")
        self.choose_music_=item_factory.get_widget("/Settings/Choose Music")
#        self.fancy_=item_factory.get_widget("/Settings/Theme/Fancy")
#        self.minimal_=item_factory.get_widget("/Settings/Theme/Minimal")
        self.demo_=item_factory.get_widget("/Help/Demo")
        self.hint_=item_factory.get_widget("/Help/Hint")
        self.readme_=item_factory.get_widget("/Help/Show readme")
        """


        toolbar=Gtk.Toolbar()
        """ TODO these need to be updated too
        self.new_button=toolbar.insert_stock(Gtk.STOCK_NEW,
                                             "New level",
                                             "",
                                             self.new,
                                             None,
                                             -1)
        self.restart_button=toolbar.insert_stock(Gtk.STOCK_GOTO_FIRST,
                                                 "Restart level",
                                                 "",
                                                 self.restart,
                                                 None,
                                                 -1)
        self.undo_button=toolbar.insert_stock(Gtk.STOCK_UNDO,
                                              "Undo last move",
                                              "",
                                              self.undo,
                                              None,
                                              -1)
        self.redo_button=toolbar.insert_stock(Gtk.STOCK_REDO,
                                              "Redo last move",
                                              "",
                                              self.redo,
                                              None,
                                              -1)
        self.end_button=toolbar.insert_stock(Gtk.STOCK_GOTO_LAST,
                                             "Goto end of history",
                                             "",
                                             self.gotoend,
                                             None,   
                                             -1)
        self.hint_button=toolbar.insert_stock(Gtk.STOCK_HELP,
                                              "Ask for hint",
                                              "",
                                              self.hint,
                                              None,
                                              -1)
        """
        vbox.pack_start(toolbar,False,False,0)

        statusbar=BottomBar.BottomBar(False,0)
        self.type_label=statusbar.add(" Intermediate ")
        self.finished=statusbar.add(" Unsolved ")
        self.hints=statusbar.add(" Hint : 100 ")
        self.moves=statusbar.add(" 0/100 ")
        self.time_label=statusbar.empty
        self.time_label.set_text("")
        self.time_label.set_anchor('e')
        vbox.pack_end(statusbar,False,False,0)

        self.sound_server=SoundServer.SoundServer(self.theme_engine)
        self.music_server=MusicServer.MusicServer(self.sound_server)
        self.music_server.connect("notify::status",self.music_status_change)
        self.music_server.connect("no_files_loaded",self.no_files_loaded)
        self.step=0.01
        self.al=0.5
        self.music_server.connect("progress",self.music_progress)
        self.music_chooser=MusicChooser.MusicChooser(self.theme_engine,
                                                     self.music_server)
        self.statisticsdialog=Statistics.StatisticsDialog(self.window)
        self.artwork=ArtWork.ArtWork(self)
        self.gamestate=GameState.GameState()
        self.propertybag=PropertyBag.PropertyBag(
                configfile=np(Misc.default_configfile),
		comment="This is a generated file!")

        self.arena=Arena.Arena(self)
        vbox.pack_start(self.arena,False,False)
        self.arena.connect("button_press_event",self.stop_demo)
        self.window.connect("key_release_event",self.stop_demo_key)
        self.on=1
        self.clock()
        self.timer=Timer.Timer(interval=1000)
        self.timer.connect("tick",self.clock)
        self.timer.set_running(1)
        self.demo_timer=Timer.Timer(interval=1500)
        self.demo_timer.connect("tick",self.demo_step)
        self.builder=Gtk.Builder()
        self.builder.add_from_file("libglade/AboutDialog.glade")
        self.about_dialog=self.builder.get_object("AboutDialog")
        config_db=PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
        config_db.load(all=True)
        self.about_dialog.set_version("%s-%s" % (config_db["version"],
                                                 config_db["release"]))
        events={"on_AboutDialog_response": self.about_dialog_close,
		"on_AboutDialog_close": self.about_dialog_close,
		"on_AboutDialog_delete_event": self.about_dialog_close
	}	
        self.builder.connect_signals(events)
        self.callbacks_enabled=1
        self.newgame()
        self.window.show_all()
        # Hack to take focus away from "new" button?
        # What is the correct method?
        self.new_button.set_sensitive(False)
        self.new_button.set_sensitive(True)


    def music_status_change(self,*args):
        if self.music_server.get_status()==MusicServer.BUSY:
            self.time_label.set_anchor()
            self.time_label.set_text("finding music")
        else:
            self.clock()

    def music_progress(self,*args):
        if self.al>=1.0 or self.al<=0.0:
            self.step=-self.step
        self.al+=self.step
        Gtk.Misc.set_alignment(self.time_label.label,self.al,1.0)
       
            
    def stop_demo_key(self,widget,event,*args):
        if not(event.get_state() & Gdk.ModifierType.MODIFIER_MASK) and \
               event.keyval & 255==27:  # compare with ESC
            self.demomode=0
            self.updateGUI()

    def stop_demo(self,widget,event,*args):
        self.demomode=0
        self.updateGUI()

    def create_theme_data(self):
        self.theme_data=[]
        for theme in self.theme_engine.getavailable_themes():
            self.theme_data.append({'id':theme,
                                    'menu_label':theme,
                                    'action':None,
                                    'menu_item':None})
    def construct_theme_menu(self):
        prefix="/Settings/Theme"
        theme_menu=[(prefix,None,None,0,"<Branch>")]
        action=0
        first_menu_path=""
        menu_path=""
        for data in self.theme_data:
            data['action']=action
            if action==0:
                first_menu_path=prefix+"/%(menu_label)s" % data
                menu_path="<RadioItem>"
            else:
                menu_path=first_menu_path
            theme_menu.append(
                      (prefix+"/%(menu_label)s" % data,
                        None,
                        self.settheme,
                        action,
                        menu_path)
                      )
            action=action+1
        return tuple(theme_menu)


    def extract_theme_menu_items(self,item_factory):
        prefix="/Settings/Theme"
        for data in self.theme_data:
            data['menu_item']=item_factory.get_widget(\
                                   prefix+"/%(menu_label)s" % data)

    def construct_sound_menu(self):
        prefix="/Settings/Sound output"
        sound_menu=[]
        first_menu_path=""
        menu_path=""
        if os.name!='nt':
            sound_menu=[(prefix,None,None,0,"<Branch>")]
            action=0
            for data in SoundData.sound_data:
                data['action']=action
                if action==0:
                    first_menu_path=prefix+"/%(menu_label)s" % data
                    menu_path="<RadioItem>"
                else:
                    menu_path=first_menu_path
                sound_menu.append(
                       (prefix+"/%(menu_label)s" % data,
                        None,
                        self.setsoundoutput,
                        action,
                        menu_path)
                      )
                action=action+1
            sound_menu.append((prefix+"/Dummy",
                               None,
                               None,
                               0,
                               "<Separator>")
                              )
            sound_menu.append((prefix+"/What is this about?",
                               None,
                               self.showsounddoc,
                               0,
                               None)
                              )
        return tuple(sound_menu)


    def extract_sound_menu_items(self,item_factory):
        prefix="/Settings/Sound output"
        if os.name!='nt':
            for data in SoundData.sound_data:
                data['menu_item']=item_factory.get_widget(\
                         prefix+"/%(menu_label)s" % data)
            self.soundabout_=item_factory.get_widget(\
                         prefix+"/What is this about?")


    def readme(self,*args):
        ShowHTML.showhtml("doc/readme.htm")

    def showsounddoc(self,*args):
        ShowHTML.showhtml("doc/sound.htm")

    def demo_step(self,timer):
        if self.gamestate.redcarout():
            self.new()
        else:
            self.hint()
            if self.gamestate.redcarout():
                self.doredcarout()
		

    def enable_easteregg(self,*args):
        print("Enabling easter egg")
        self.gamestate.easteregg=1

    def show_statistics(self,*args):
        if self.callbacks_enabled:
            self.statisticsdialog.show()
            self.updateGUI()

    def setwarningsmode(self,action,menu):
        if self.callbacks_enabled:
            if menu.get_active()==True:
                self.expertmode=0
            else:
                self.expertmode=1

    def setsound(self,action,menu):
        if self.callbacks_enabled:
            if menu.get_active()==True:
                self.sound_server.enable_sound()
            else:
                self.sound_server.disable_sound()

    def setsoundoutput(self,soundoutput,menu):
        if self.callbacks_enabled:
            if os.name!='nt':
                for data in SoundData.sound_data:
                    if data['action']==soundoutput:
# Selection of radio items seems to generate two events (pygtk 2.4).
# One for the selected one and one for the new one.
                        if self.sound_server.getsoundoutput()!=data['id']:
                            self.sound_server.setsoundoutput(data['id'])
                            CondMessageBox.showwarning(
                                message="This change will only take effect after you restart PyTraffic.",
                                window=self.window)
                    

    def setmusic(self,*args):
        if self.callbacks_enabled:
            if self.music_.get_active()==True:
                self.music_server.set_playing(1)
            else:
                self.music_server.set_playing(0)

    def no_files_loaded(self,*arg):
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

    def choosemusic(self,*args):
        self.music_chooser.run()

    def settheme(self,theme,menu):
        if self.callbacks_enabled:
            for data in self.theme_data:
                if data['action']==theme:
# Selection of radio items seems to generate two events (pygtk 2.4).
# One for the selected one and one for the new one.
                    if data['id']!=self.theme_engine.gettheme():
                        self.theme_engine.settheme(data['id'])
                        self.artwork.theme_change()
                        self.arena.setupboard()
            self.updateGUI()

    def setdemomode(self,action,menu):
        if self.callbacks_enabled:
            if menu.get_active()==True:
                self.demomode=1
            else:
                self.demomode=0
            self.updateGUI()

    def clock(self,*args):
        if self.music_server.get_status()==MusicServer.FREE:
            self.time_label.set_anchor('e')
            if self.on:
                format="%H:%M"
            else:
                format="%H:%M"
            self.on=not(self.on)
            strtime=time.strftime(format,time.localtime(time.time()))
            self.time_label.set_text(strtime)

    def about_dialog_close(self,*args):
        self.about_dialog.hide()
        return True

    def about(self,*args):
       	self.about_dialog.show()
        return True
 
    def new(self,action=None,menu=None):
            if self.demomode:
                self.gamestate.new(existing=1)
                self.arena.setupboard()
                self.updateGUI()
                return
            reply=0
            if not(self.gamestate.youvewon):
                reply=CondMessageBox.askyesno(
                    message="Do you want to abandon the current level?",
                    window=self.window,
                    disable=self.expertmode or self.demomode)
            if self.gamestate.youvewon or reply:
                availableslots=self.gamestate.offsetsavailable(\
                                         self.gamestate.type)
                existing=0
                if not(availableslots):
                    resetpermission=CondMessageBox.askyesno(
                          message="No more unsolved levels of the requested \
type! Do you want to reset these levels?",
                          window=self.window,
                          disable=0)
                    if resetpermission:
                        self.gamestate.resetsolvedlevels(self.gamestate.type)
                    else:
                        existing=1
                self.gamestate.new(existing)
                self.arena.setupboard()
                self.updateGUI()
        
    def newgame(self):
        something_bad_happened=0
        try:
            self.default_all()
            self.propertybag.load()
            self.load_all()
        except Exception as e:
            something_bad_happened=1
            last_error=str(e)
            print ("Exception in newgame",last_error)
        except Error as e:
            something_bad_happened=1
            last_error=str(e)
            print ("Error in newgame", last_error)
        if something_bad_happened:
            Misc.save_configfile()
            self.default_all()
            self.load_all()
            CondMessageBox.showwarning(
                   message="""There was a fatal error in the savefile: %s.
It will be replaced by an empty one.
I have tried to save a copy as: %s.
The error was: %s. """ % (Misc.default_configfile,Misc.backup_configfile,last_error),
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

    def hint(self,*args):
        self.arena.setanimation(True)
        confirmation=0
        if not(self.gamestate.youvewon) and not(self.gamestate.dontinsert):
            confirmation=CondMessageBox.askokcancel(
                    message="If you use a hint now the level can no longer be recorded as solved!",
                    window=self.window,
                    disable=self.expertmode or self.demomode)
        else:
            confirmation=1
        if confirmation:
            if not(self.gamestate.youvewon):
                self.gamestate.dontinsert=1
                self.gamestate.hint=self.gamestate.hint+1
            index,row,col=self.gamestate.findbestmove()
            self.arena.domove(index,row,col)
            self.arena.carlist[index].move(row,col)
            if self.gamestate.redcarout():
                self.doredcarout()
        self.arena.setanimation(False)

    def doredcarout(self):
        if not(self.gamestate.youvewon or self.demomode):
            self.sound_server.play(self.artwork.getapplause())
            if self.gamestate.hint==0 and \
                    self.gamestate.bestyoucando-1==self.gamestate.nrofmovestaken():
                CondMessageBox.showinfo(
			 message="Congratulations...you found the shortest possible solution to this level!",
			 window=self.window,
			 disable=self.expertmode)
            elif self.gamestate.hint==0:
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

    def settype(self,type,menu):
      if self.callbacks_enabled:
        type_dict={0: "Trivial", 1: "Easy", 2: "Intermediate", 3: "Advanced",
                   4: "Expert"}
        type=type_dict[type]
# Selection of radio items seems to generate two events (pygtk 2.4).
# One for the selected one and one for the new one.
        if type!=self.gamestate.type:
            if self.demomode:
                    self.gamestate.type=type
                    self.gamestate.new(existing=1)
                    self.arena.setupboard()
                    self.updateGUI()
                    return
            reply=0
            if  not(self.gamestate.youvewon):
                reply=CondMessageBox.askyesno(
                       message="Do you want to abandon the current level?",
                       window=self.window,
                       disable=self.expertmode or self.demomode)
            if reply or self.gamestate.youvewon:
                availableslots=self.gamestate.offsetsavailable(type)
                existing=0
                if not(availableslots):
                    resetpermission=CondMessageBox.askyesno(
                             message="No more unsolved levels of the requested type! Do you want to reset these levels?",
                             window=self.window,
                             disable=0)
                    if resetpermission:
                        self.gamestate.resetsolvedlevels(type)
                    else:
                        existing=1
                self.gamestate.type=type
                self.gamestate.new(existing)
                self.arena.setupboard()
        self.updateGUI()

    def restart(self,*args):
        self.arena.restart()

    def gotoend(self,*args):
        self.arena.gotoend()

    def redo(self,*args):
        if not self.gamestate.endofhistory():
                self.arena.redo()

    def undo(self,*args):
        if not self.gamestate.startofhistory():
            self.arena.undo()

#    def location(self):
#        return "+%s+%s" % self.window.get_position()

    def updateGUI(self):
        self.callbacks_enabled=0
        if self.expertmode:
            self.warningsmode_.set_active(False)
        else:
            self.warningsmode_.set_active(True)
        for data in self.theme_data:
            if data['id']==self.theme_engine.gettheme():
                data['menu_item'].set_active(True)
        self.moves.set_text("%d/%d" % (self.gamestate.nrofmovestaken(),
                                  self.gamestate.bestyoucando-1))
        type_dict={"Trivial" : self.trivial_, "Easy": self.easy_ ,
                   "Intermediate": self.intermediate_,
                   "Advanced" : self.advanced_,
                   "Expert": self.expert_}
        type_dict[self.gamestate.type].set_active(True)
        self.type_label.set_text(self.gamestate.type)
        if not self.gamestate.youvewon:
            self.finished.set_text("Unsolved")
            self.finished.modify_bg(Gdk.color_parse("red"))
        elif self.gamestate.hint:
            self.finished.set_text("Solved: %d" % \
                            self.gamestate.solvedinnrofmoves)
            self.finished.modify_bg(Gdk.color_parse("Orange"))
        else:
            self.finished.set_text("Solved: %d" % \
                            self.gamestate.solvedinnrofmoves)
            self.finished.modify_bg(Gdk.color_parse("Green"))
        self.statisticsdialog.update_statistics(self.gamestate.statistics)
        if os.name!='nt':
            for data in SoundData.sound_data:
                if data['id']==self.sound_server.getsoundoutput():
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

#        if self.sound_server.has_music():  
#            self.music_.set_sensitive(True)
#	else:
#            self.sound_.set_active(False)
#	    self.music_.set_sensitive(False)

        if not self.sound_server.sound_works():
            self.sound_.set_sensitive(False)
            self.music_.set_sensitive(False)
            self.choose_music_.set_sensitive(False)
        if not ShowHTML.can_display_html():
            self.readme_.set_sensitive(False)
            if os.name!='nt':
                self.soundabout_.set_sensitive(False)
        if self.demomode:
            self.demo_.set_active(True)
            self.hint_button.set_sensitive(False)
            self.hint_.set_sensitive(False)
#                self.arena.set_sensitive(False)
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
            self.hints.set_text("Demo"),
            self.hints.modify_bg(Gdk.color_parse("yellow"))
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
                #                self.arena.set_sensitive(False)
                 self.arena.disable()
            else:
                #                self.arena.set_sensitive(True)
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
                self.hints.modify_bg(Gdk.color_parse("Orange"))
            else:
                self.hints.reset_bg()
            self.demo_timer.set_running(0)
        self.arena.update_cursors()
        self.callbacks_enabled=1

    def quit(self,*args):
        self.save_all()
        Gtk.main_quit()
        # there is a problem with using sys.exit() if the program has
        # been suspended while the music is playing.
        # is this safe?
        os._exit(0)


    def save_all(self):
        self.artwork.save_bag(self.propertybag)
        self.theme_engine.save_bag(self.propertybag)
        self.gamestate.save_bag(self.propertybag)
        self.statisticsdialog.save_bag(self.propertybag)
        self.sound_server.save_bag(self.propertybag)
        self.music_server.save_bag(self.propertybag)
        self.arena.save_bag(self.propertybag)
        self.propertybag['expertmode']=self.expertmode
#        self.propertybag['location']=self.location()
        self.propertybag.save()

    def default_all(self):
        self.theme_engine.default_bag(self.propertybag)
        self.sound_server.default_bag(self.propertybag)
        self.music_server.default_bag(self.propertybag)
        self.artwork.default_bag(self.propertybag)
        self.gamestate.default_bag(self.propertybag)
        self.statisticsdialog.default_bag(self.propertybag)
        self.arena.default_bag(self.propertybag)
#        self.propertybag['location']=None
        self.propertybag['expertmode']=0
        self.propertybag['demomode']=0

    def load_all(self):
        self.callbacks_enabled=0
        self.theme_engine.load_bag(self.propertybag)
        self.sound_server.load_bag(self.propertybag)
        self.music_server.load_bag(self.propertybag)
        self.artwork.load_bag(self.propertybag)
        self.gamestate.load_bag(self.propertybag)
        self.arena.load_bag(self.propertybag)
        self.arena.setupboard()
#        if self.propertybag['location']!=None:
#            self.window.parse_geometry(self.propertybag['location'])
        self.expertmode=self.propertybag['expertmode']
        self.statisticsdialog.load_bag(self.propertybag)
        self.demomode=0
        self.callbacks_enabled=1
        self.updateGUI()

if __name__=='__main__':
    Game()
    Gtk.main()
