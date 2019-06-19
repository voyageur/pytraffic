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
import pango

class SmartLabel(gtk.EventBox):
    def __init__(self,text=""):
        gtk.EventBox.__init__(self)
        self.label=gtk.Label(text)
        self.add(self.label)
        style=self.label.rc_get_style()
        self.default_bg=style.bg[gtk.STATE_NORMAL]
        self.font_desc=style.font_desc
        self.font_metrics=\
             self.label.get_pango_context().get_metrics(self.font_desc)
        self.approximate_char_width=\
             self.font_metrics.get_approximate_char_width()

    def modify_bg(self,color):
        gtk.EventBox.modify_bg(self,gtk.STATE_NORMAL,color)

    def reset_bg(self):
        gtk.EventBox.modify_bg(self,gtk.STATE_NORMAL,self.default_bg)

    def set_char_width(self,n):
        self.set_size_request(n*self.approximate_char_width/pango.SCALE,-1)
    
    def set_anchor(self,s=''):
        if s=='e':
            gtk.Misc.set_alignment(self.label,1.0,1.0)
        elif s=='w':
            gtk.Misc.set_alignment(self.label,0.0,1.0)
        else:
            gtk.Misc.set_alignment(self.label,0.5,1.0)

    def set_text(self,text):
        self.label.set_text(text)

    def set_sensitive(self,gtk_boolean):
        self.label.set_sensitive(gtk_boolean)


