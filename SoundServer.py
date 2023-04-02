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
import ThemeEngine
import SoundData
import Chooser
import Timer
import glob,copy
import stat

np=Misc.normalize_path


# SoundServer is a singleton object!


class SoundServer:

    def __init__(self,theme_engine):
        self.__sound_output_explicitly_set=0
        self.theme_engine=theme_engine

    def last_error(self):
        return self.__last_error

    def sound_works(self):
        return self.__sound_works

    def enable_sound(self):
        if self.__sound_works:
            self.__sound_enabled=1

    def disable_sound(self):
        self.__sound_enabled=0

    def sound_enabled(self):
        return self.__sound_enabled


    def play(self,sound):
        if self.__sound_works and self.__sound_enabled and sound!=None:
            sound.play()

    def init_supported(self):
        self.__supported_dict={}
        self.__supported_dict['']=False
        self.__supported_dict['.readme']=False
        self.__supported_dict['.copyright']=False
        for file in glob.glob(np('sound_test/*')):
            extension=os.path.splitext(file)[1].lower()
            try:
                dummy_test=self.mixer.Sound(np(file))
                self.__supported_dict[extension]=True
            except:
                self.__supported_dict[extension]=False

    def is_supported(self,filename,use_extensions=1):
        if not os.path.exists(np(filename)):
            return False
        mode=os.stat(filename)[stat.ST_MODE]
        if not stat.S_ISREG(mode):
            return False
        extension=os.path.splitext(filename)[1].lower()
        if use_extensions and self.__supported_dict.get(extension)==True:
            return True
        elif use_extensions and self.__supported_dict.get(extension)==False:
            return False
        else:
#            print "Doing real work with %s" % filename
            try:
                self.mixer.music.load(np(filename))
                if use_extensions:
                    self.__supported_dict[extension]=True
                return True
            except:
                if use_extensions:
                    self.__supported_dict[extension]=False
                return False



    def sound_has_worked(self):
        return self.__sound_has_worked

    def setsoundoutput(self,output):
        self.__output=output
        self.__sound_output_explicitly_set=1

    def getsoundoutput(self):
        return self.__output

    def default_bag(self,propertybag):
        propertybag['sound_has_worked']=1
        propertybag['sound_output']='Default'
        propertybag['sound_enabled']=1

    def load_bag(self,propertybag):
        self.__output=output=propertybag['sound_output']
        self.__chooser=None
        SoundData.do_os_stuff(output)
        self.__sound_works=0
        self.__sound_enabled=0
        try:
            import sdl_mixer as mixer
            self.mixer=mixer
            self.mixer.init(frequency=44100)
            self.init_supported()
            if self.is_supported(np('sound_test/tone.ogg')):
                self.__sound_works=1
        except Exception as e:
            self.__last_error=str(e)


        self.__sound_has_worked=propertybag['sound_has_worked']
        if self.__sound_has_worked and self.__sound_works:
            if propertybag['sound_enabled']:
                self.enable_sound()
        elif self.__sound_works:
            self.enable_sound()



    def save_bag(self,propertybag):
        propertybag['sound_enabled']=self.__sound_enabled
        if not self.__sound_output_explicitly_set:
            propertybag['sound_has_worked']=self.__sound_works
        else:
            propertybag['sound_has_worked']=1 # force dialog box after restart
            propertybag['sound_enabled']=1  # enable sound

        propertybag['sound_output']=self.__output
