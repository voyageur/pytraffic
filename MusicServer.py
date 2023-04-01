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
from gi.repository import GObject
import Timer,Chooser
import Misc
import PropertyBag

FREE=0
BUSY=1

np=Misc.normalize_path

class MusicServer(GObject.GObject):
    __gsignals__ = {
        'progress' : (GObject.SignalFlags.RUN_FIRST, None,
                      ()),
        'no_files_loaded' : (GObject.SignalFlags.RUN_FIRST, None,
                      ()),
    }
    __gproperties__ = {
        'playing' :  (GObject.TYPE_BOOLEAN,
                      'playing property',
                      'indicates if the music is playing',
                      0,
                      GObject.PARAM_READWRITE),
        'status' :  (GObject.TYPE_INT,
                      'status property',
                      'indicates if the server is loading or not',
                     0,
                     1,
                      FREE,
                      GObject.PARAM_READABLE),
        'strategy' :  (GObject.TYPE_INT,
                      'strategy property',
                      'indicates whether music selection should be shuffled or not',
                     0,
                     1,
                      Chooser.REPEAT,
                      GObject.PARAM_READWRITE),
        'recursive' :  (GObject.TYPE_BOOLEAN,
                      'recursive property',
                      'indicates if the music selection should be considered recursive',
                      0,
                      GObject.PARAM_READWRITE),
        'use-extensions' :  (GObject.TYPE_BOOLEAN,
                      'use_extension property',
                      'whether to cache supported/unsupported extensions',
                      1,
                      GObject.PARAM_READWRITE),
        }

    def set_playing(self,value):
        self.set_property('playing',value)

    def get_playing(self):
        return self.get_property('playing')

    def set_strategy(self,value):
        self.set_property('strategy',value)

    def get_strategy(self):
        return self.get_property('strategy')

    def set_recursive(self,value):
        self.set_property('recursive',value)

    def get_recursive(self):
        return self.get_property('recursive')

    def set_use_extensions(self,value):
        self.set_property('use_extensions',value)

    def get_use_extensions(self):
        return self.get_property('use_extensions')

    def __set_status(self,value):
        if value!=self.__status:
            self.__status=value
            self.notify("status")

    def get_status(self):
        return self.get_property('status')

    
    def __init__(self,sound_server):
        super().__init__()
        self.__playing=0
        self.__status=FREE
        self.__strategy=Chooser.REPEAT
        self.__recursive=False
        self.__use_extensions=True
        self.__idler=Timer.Idler()
        self.__idler.connect("tick",self.__make_some_progress)
        self.__music_watcher=Timer.Timer(interval=1000)
        self.__music_watcher.connect("tick",self.__check_music)
        self.__sound_server=sound_server
        config_db=PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
        config_db.load(all=True)
        self.__default_music_path=list(map(np,config_db["default_music_path"]))
        self.__music_path=self.__default_music_path
        self.__old_music_path=self.__default_music_path
        self.__default_available_music=\
                           Chooser.Chooser(list(map(np,config_db["default_playlist"])))
        self.__available_music=self.__default_available_music

        
    def __check_music(self,*args):
            if not self.__sound_server.mixer.music.get_busy() \
                   and self.get_status()==FREE:
# To be safe we limit our tries to 10.
                checks=0
                while(1):
                    music_file=self.__available_music.get()
                    try:
                        self.__sound_server.mixer.music.load(music_file)
                        self.__sound_server.mixer.music.play()
#                        print "Playing %s " % music_file
                        break
                    except:
#                        print "%s has an unsupported format" % music_file
                        pass
                    checks+=1
                    if checks>10:
# We should never get here but it is possible if the user installs
# many files which seem supported but are not.
# We go back to the default setting here. We should emit a signal
# accordingly.
                            print("Can't find suitable music... Reverting to default.")
                            self.__music_path=\
                                          self.__default_music_path
                            self.__available_music=\
                                          self.__default_available_music
                            break


    def do_set_property(self,pspec,value):
        if pspec.name=='playing':
            if self.__sound_server.sound_works():
                self.__playing=value
                if value:
                    self.__music_watcher.set_running(1)
                else:
                    self.__music_watcher.set_running(0)
                    self.__sound_server.mixer.music.stop()
        elif pspec.name=='strategy':
            self.__strategy=value
            self.__available_music.set_strategy(value)
        elif pspec.name=='recursive':
            self.__recursive=value
        elif pspec.name=='use-extensions':
            self.__use_extensions=value
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def do_get_property(self,pspec):
        if pspec.name=='playing':
            return self.__playing
        elif pspec.name=='status':
            return self.__status
        elif pspec.name=='strategy':
            return self.__strategy
        elif pspec.name=='recursive':
            return self.__recursive
        elif pspec.name=='use-extensions':
            return self.__use_extensions
        else:
            raise AttributeError('unknown property %s' % pspec.name)

# temporary hack
    def get_music_path(self):
        return self.__music_path[0]

    def reset(self):
        if self.get_playing():
            self.set_playing(0)
            self.set_playing(1)


    def load(self,music_path):
        if self.__sound_server.sound_works():
            if type(music_path)!=type([]):
                raise Exception("Music path is not a list")
	    if self.get_status()!=BUSY:
	        self.__old_music_path=self.__music_path
            self.__music_path=music_path
            self.__set_status(BUSY)
            if self.get_recursive():
                self.__file_list_generator=\
                        Misc.walk(music_path,recursion_depth=None)
            else:
                self.__file_list_generator=\
                        Misc.walk(music_path,1)
            self.__partial_list=[]
            self.__idler.set_running(1)

    def __make_some_progress(self,*args):
        try:
            file_name=next(self.__file_list_generator)
            self.emit("progress")
            if self.__sound_server.is_supported(file_name,self.get_use_extensions()):
                self.__partial_list.append(file_name)
            else:
                pass
        except StopIteration:
            self.__set_status(FREE)
            self.__idler.set_running(0)
            if self.__partial_list==[]:
                self.emit("no_files_loaded")
                self.__music_path=self.__old_music_path
            else:
                self.__available_music=Chooser.Chooser(self.__partial_list)
                self.__available_music.set_strategy(self.get_strategy())
                self.reset()

    def default_bag(self,propertybag):
        propertybag['music_playing']=1
        propertybag['music_path']=self.__sound_server.theme_engine.\
                                   default_music_path()
        propertybag['music_strategy']=Chooser.REPEAT
        propertybag['music_recursive']=False
        propertybag['music_use_extensions']=True

    def load_bag(self,propertybag):
        self.set_recursive(propertybag['music_recursive'])
        self.set_use_extensions(propertybag['music_use_extensions'])
        self.set_strategy(propertybag['music_strategy'])
        self.load(propertybag['music_path'])
        self.set_playing(propertybag['music_playing'])
        

    def save_bag(self,propertybag):
        propertybag['music_playing']=self.get_playing()
	if self.get_status()==BUSY:
		propertybag['music_path']=self.__old_music_path
	else:
		propertybag['music_path']=self.__music_path
        propertybag['music_strategy']=self.get_strategy()
        propertybag['music_recursive']=self.get_recursive()
        propertybag['music_use_extensions']=self.get_use_extensions()
     
        

GObject.type_register(MusicServer)
