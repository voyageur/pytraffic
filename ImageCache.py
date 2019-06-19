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

import gtk
import Cache

class ImageCache(Cache.Cache):
    def __init__(self):
        Cache.Cache.__init__(self,self.__factory)

    def __factory(self,filename):
        pixbuf=gtk.gdk.pixbuf_new_from_file(filename)
        image=gtk.Image()
        image.set_from_pixbuf(pixbuf)
        return image

    def getimage(self,filename):
        return self.getitem(filename)

class PixmapCache(Cache.Cache):
    def __init__(self):
        Cache.Cache.__init__(self,self.__factory)

    def __factory(self,image):
        return gtk.gdk.Pixbuf.render_pixmap_and_mask(image.get_pixbuf())

    def getpixmaps(self,image):
        return self.getitem(image)
        
