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
import SmartLabel


class BottomBarItem(SmartLabel.SmartLabel):
    def __init__(self,text=""):
        SmartLabel.SmartLabel.__init__(self,text)
        self.frame=Gtk.Frame()
        self.frame.add(self)
        
    def show(self):
        SmartLabel.show(self)
        self.frame.show()

class BottomBar(Gtk.HBox):
    def __init__(self,homogeneous=False,spacing=0):
        GObject.GObject.__init__(self,homogeneous,spacing)
        self.empty=BottomBarItem()
#        self.empty=Gtk.ProgressBar()
        self.pack_end(self.empty.frame,True,True,0)
#        self.pack_end(self.empty,True,True,0)

    def add(self,text=""):
        l=BottomBarItem(text)
        self.pack_start(l.frame,True,True,0)
        return l


