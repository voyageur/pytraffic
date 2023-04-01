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

import Misc
import Affine2D
import os
import glob
import copy
import PropertyBag

np=Misc.normalize_path

def get_id(path):
    name=os.path.split(path)[1]
    base=os.path.splitext(name)[0]
    iid=base[6:]
    return iid

def get_ids(list_of_paths):
    return [get_id(p) for p in list_of_paths]

def get_background_ids(list_of_paths):
    return [os.path.splitext(os.path.split(x)[1])[0] for x in list_of_paths]


class NoSuchTheme(Exception):
    pass

class ThemeEngine:

    def __init__(self):
        self.available_themes=None
        self.default_theme=None
        self.config_db=PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
        self.config_db.load(all=True)


    def default_music_path(self):
        return [np(p) for p in self.config_db["default_music_path"]]

    def theme_has_sound(self):
        return os.path.exists(np(os.path.join(self.getavailable_themes_dict()[self.current_theme],
                                              "sound")))

    def find_sound(self,name,theme=None):
        if not theme:
            theme=self.current_theme
        return np(os.path.join(self.getavailable_themes_dict()[theme],
                                "sound",
                                name+".ogg"))

#    def find_music(self,name):
#        return np(os.path.join(self.default_music_path(),name))

##     def get_available_music(self):
##         music_path=self.default_music_directory()
##         file_list=glob.glob(np(os.path.join(music_path,
##                                             "*")))
##         copyright_list=glob.glob(np(os.path.join(music_path,"*COPYRIGHT*")))
##         readme_list=glob.glob(np(os.path.join(music_path,"*README*")))
##         file_list_=copy.copy(file_list)
##         for m in file_list_:
##             if m in copyright_list:
##                 file_list.remove(m)
##             if m in readme_list:
##                 file_list.remove(m)
##         return file_list

# world to screen transform
    def find_transform(self):
        return np(os.path.join(self.getavailable_themes_dict()[self.current_theme],
                               "transform"))

    def find_background_basepoints(self):
        return np(os.path.join(self.getavailable_themes_dict()[self.current_theme],
                               "background",
                               "basepoints"))

    def find_car_basepoints(self):
        return np(os.path.join(self.getavailable_themes_dict()[self.current_theme],
                               "cars",
                               "basepoints"))

    def __find_car_image(self,name,theme=None):
        if not theme:
            theme=self.current_theme
        return np(os.path.join(self.getavailable_themes_dict()[theme],
                               "cars",
                               name+".png"))

    def get_default_theme(self):
        if self.default_theme:
            return self.default_theme
        default_themes=[os.path.basename(x) for x in self.config_db["themes"]]
        available_themes=self.getavailable_themes()
        for t in default_themes:
            if t in available_themes:
                self.default_theme=t
                return t
        raise Exception("No default theme")


    def find_car_image(self,horizontal,truck,type,theme=None):
        T=['C','T']
        H=['V','H']
        if type=='red':
            return self.__find_car_image('carNred',theme)
        else:
            return self.__find_car_image('car'+H[horizontal]+T[truck]\
                                       +'N'+type,theme)


    def find_background(self,name,theme=None):
        if not theme:
            theme=self.current_theme
        return np(os.path.join(self.getavailable_themes_dict()[theme],
                               "background",
                               name+".png"))

    def load_bag(self,propertybag):
        self.settheme(propertybag['current_theme'])

    def save_bag(self,propertybag):
        propertybag['current_theme']=self.current_theme

    def default_bag(self,propertybag):
        propertybag['current_theme']=self.get_default_theme()

    def settheme(self,theme):
        if theme not in self.getavailable_themes():
            self.current_theme=self.get_default_theme()
        else:
            self.current_theme=theme

    def gettheme(self):
        return self.current_theme

    def getavailable_themes_dict(self):
        if self.available_themes:
            return self.available_themes
        self.available_themes={}
        np=Misc.normalize_path
        for p in self.config_db["theme_search_path"]:
            file_list=glob.glob(np(os.path.join(p,"*")))
            for f in file_list:
                f1=os.path.basename(f)
                self.available_themes[f1]=f
        return self.available_themes

    def getavailable_themes(self):
        return sorted(self.getavailable_themes_dict().keys())

    def gettrucks(self):
        return get_ids(glob.glob(self.__find_car_image("carHTN*")))

    def getcars(self):
        return get_ids(glob.glob(self.__find_car_image("carHCN*")))

    def getbackgrounds(self):
        return  get_background_ids(\
            glob.glob(self.find_background('*')))
