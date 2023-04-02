
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


import sys,glob,random,os
import ImageCache
import SoundCache
import Misc
import copy
import Chooser
import Affine2D


np=Misc.normalize_path


class ArtWork:
    def __init__(self,root):
        self.image_cache=ImageCache.ImageCache()
        self.theme_engine=root.theme_engine
        self.sound_server=root.sound_server
        self.sound_cache=SoundCache.SoundCache(self.sound_server)

    def load_bag(self,propertybag):
        self.saved_list=propertybag['saved_list']
        self.saved_background=propertybag['background']
        self.theme_change()

    def save_bag(self,propertybag):
        propertybag['saved_list']=self.new_saved_list
        propertybag['background']=self.last_background

    def default_bag(self,propertybag):
        propertybag['saved_list']=[]
        propertybag['background']=''

    def theme_change(self):
        if self.sound_server.sound_works() and \
           self.theme_engine.theme_has_sound():
            self.applause_clip=self.sound_cache.getsound(\
                            self.theme_engine.find_sound("applause"))
            self.engine_clip=self.sound_cache.getsound(\
                             self.theme_engine.find_sound("engine"))
            self.horn_clip=self.sound_cache.getsound(\
                             self.theme_engine.find_sound("horn"))
        self.truck_chooser=Chooser.Chooser(self.theme_engine.gettrucks(),
                                           "Resetting trucks")
        self.car_chooser=Chooser.Chooser(self.theme_engine.getcars(),
                                         "Resetting cars")
        self.bg_chooser=Chooser.Chooser(self.theme_engine.getbackgrounds(),
                                        "Resetting background")
        basepoints_path=self.theme_engine.find_background_basepoints()
        if os.path.exists(basepoints_path):
            f=open(basepoints_path,"r")
            self.background_basepoints=eval(f.read())
            f.close()
        else:
            self.background_basepoints=None
        basepoints_path=self.theme_engine.find_car_basepoints()
        if os.path.exists(basepoints_path):
            f=open(basepoints_path,"r")
            self.car_basepoints=eval(f.read())
            f.close
        else:
            self.car_basepoints=None

    def gettransform(self):
        transform_path=self.theme_engine.find_transform()
        if os.path.exists(transform_path):
            f=open(transform_path,"r")
            transform=eval(f.read())
            f.close()
        else:
            transform=Affine2D.identity_affine
        return transform

    def getbackground(self):
        if self.saved_background!='':
            self.last_background=self.saved_background
            self.saved_background=''
        else:
            self.last_background=self.bg_chooser.get()
        try:
            image=self.image_cache.getimage(
                     self.theme_engine.find_background(self.last_background))
        except:
            print("Background image in save file does not exist")
            print("Using place holder")
            self.last_background=self.bg_chooser.get()
            image=self.image_cache.getimage(
                        self.theme_engine.find_background(self.last_background))
        if not self.background_basepoints:
            return (image,(0,0))
        else:
            return (image,self.background_basepoints[self.last_background+".png"])


    def reset(self):
        self.truck_chooser.reset()
        self.car_chooser.reset()
        self.new_saved_list=[]


    def getapplause(self):
        if self.sound_server.sound_works() and \
           self.theme_engine.theme_has_sound():
            return self.applause_clip
        else:
            return None

    def getartwork(self,horizontal=1,truck=0):
        H={0:'V', 1:'H'}
        T={0:'C', 1:'T'}
        S={'normal':'N', 'ghost':'G'}
        if self.saved_list!=[]:
            color=self.saved_list[0]
            del self.saved_list[0]
        else:
            if truck:
                color=self.truck_chooser.get()
            else:
                color=self.car_chooser.get()
        self.new_saved_list=self.new_saved_list+[color]

        artwork={}
        filename=self.theme_engine.find_car_image(horizontal,
                                                  truck,
                                                  str(color))
        try:
            if not self.car_basepoints:
                artwork['normal']=(self.image_cache.getimage(filename),(0,0))
            else:
                artwork['normal']=(self.image_cache.getimage(filename),
                            self.car_basepoints[\
                                   os.path.basename(filename)])
        except:
            print("Using place holder for %s" % filename)
            filename=self.theme_engine.find_car_image(horizontal,
                                                         truck,
                                                         '0')
            if not self.car_basepoints:
                artwork['normal']=(self.image_cache.getimage(filename),(0,0))
            else:
                artwork['normal']=(self.image_cache.getimage(filename),
                            self.car_basepoints[\
                                    os.path.basename(filename)])


        if self.sound_server.sound_works() and \
           self.theme_engine.theme_has_sound():
           try:
               filename_horn=self.theme_engine.find_sound(\
                              'car'+T[truck]+'horn'+str(color))
               artwork['horn']=self.sound_cache.getsound(filename_horn)
           except:
               artwork['horn']=self.horn_clip
           try:
               filename_engine=self.theme_engine.find_sound(\
                          'car'+T[truck]+'engine'+str(color))
               artwork['engine']=self.sound_cache.getsound(filename_engine)
           except:
               artwork['engine']=self.engine_clip
        else:
            artwork['horn']=None
            artwork['engine']=None


        return artwork



    def getRedCar(self):
        artwork={}
        try:
            filename=self.theme_engine.find_car_image(0,0,'red')
            if not self.car_basepoints:
                artwork['normal']=(self.image_cache.getimage(filename),(0,0))
            else:
                artwork['normal']=(self.image_cache.getimage(filename),
                            self.car_basepoints[\
                                   os.path.basename(filename)])
        except:
            print("Using a place holder for %s." % filename)
            filename=self.theme_engine.find_car_image(horizontal=1,
                                                         truck=0,
                                                         type='0')
            if not self.car_basepoints:
                artwork[s]=(self.image_cache.getimage(filename),(0,0))
            else:
                artwork[s]=(self.image_cache.getimage(filename),
                            self.car_basepoints[\
                                   os.path.basename(filename)])


        if self.sound_server.sound_works() and \
           self.theme_engine.theme_has_sound():
           try:
               filename_horn=self.theme_engine.find_sound('carhornred')
               artwork['horn']=self.sound_cache.getsound(filename_horn)
           except:
               artwork['horn']=self.horn_clip
           try:
               filename_engine=self.theme_engine.find_sound('carenginered')
               artwork['engine']=self.sound_cache.getsound(filename_engine)
           except:
               artwork['engine']=self.engine_clip
        else:
            artwork['horn']=None
            artwork['engine']=None


        return artwork
