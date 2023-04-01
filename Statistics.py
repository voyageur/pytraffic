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
import sys

np=Misc.normalize_path

class StatisticsDialog:
    def __init__(self,parent=None):
        self.builder=Gtk.Builder()
        self.builder.add_from_file("libglade/StatisticsWindow.ui")
        self.window=self.builder.get_object("StatisticsWindow")
        self.window.set_destroy_with_parent(True)
        # transient does not work well on nt
        if parent and os.name!='nt':
            self.set_transient_for(parent)
        self.intermediate_solved=self.builder.get_object("intermediate_solved")
        self.intermediate_total=self.builder.get_object("intermediate_total")
        self.advanced_solved=self.builder.get_object("advanced_solved")
        self.advanced_total=self.builder.get_object("advanced_total")
        self.expert_solved=self.builder.get_object("expert_solved")
        self.expert_total=self.builder.get_object("expert_total")
        events={"on_StatisticsWindow_delete_event" : self.hide}
        self.builder.connect_signals(events)

    def show(self):
        self.window.show_all()
        self._visible=1

    def hide(self,*args):
        self.window.hide_all()
# at one point this seemed necessary...don't remember why...
#        self.window.unrealize()
        self._visible=0
        return True

    def save_bag(self,propertybag):
        propertybag['statistics']=self._visible

    def default_bag(self,propertybag):
        propertybag['statistics']=0

    def load_bag(self,propertybag):
        self.visible=propertybag['statistics']
        if self.visible:
            self.show()
        else:
            self.hide()

    def update_statistics(self,statistics):
        self.intermediate_solved.set_text(
            str(statistics['Intermediate']['Solved']))
        self.intermediate_total.set_text(
            str(statistics['Intermediate']['Total']))

        self.advanced_solved.set_text(
            str(statistics['Advanced']['Solved']))
        self.advanced_total.set_text(
            str(statistics['Advanced']['Total']))

        self.expert_solved.set_text(
            str(statistics['Expert']['Solved']))
        self.expert_total.set_text(str(statistics['Expert']['Total']))
