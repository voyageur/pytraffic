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

    

def askokcancel(message,window=None,disable=0):
    if not disable:
        dialog=Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                 flags=Gtk.DialogFlags.MODAL|\
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                 buttons=Gtk.ButtonsType.OK_CANCEL,
                                 message_format=message)
        if window:
            dialog.set_transient_for(window)
        response_id=dialog.run()
        dialog.destroy()
        if response_id==Gtk.ResponseType.OK:
            return 1
        else:
            return 0
    else:
        return 1

def askyesno(message,window=None,disable=0):
    if not disable:
        dialog=Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                 flags=Gtk.DialogFlags.MODAL|\
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                 buttons=Gtk.ButtonsType.YES_NO,
                                 message_format=message)
        if window:
            dialog.set_transient_for(window)
        dialog.set_modal(True)
        response_id=dialog.run()
        dialog.destroy()
        if response_id==Gtk.ResponseType.YES:
            return 1
        else:
            return 0
    else:
        return 1

def showinfo(message,window=None,disable=0):
    if not disable:
        dialog=Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                 flags=Gtk.DialogFlags.MODAL|\
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                 buttons=Gtk.ButtonsType.OK,
                                 message_format=message)
        if window:
            dialog.set_transient_for(window)
        dialog.run()
        dialog.destroy()

def showwarning(message,window=None,disable=0):
    if not disable:
        dialog=Gtk.MessageDialog(type=Gtk.MessageType.WARNING,
                                 flags=Gtk.DialogFlags.MODAL|\
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                 buttons=Gtk.ButtonsType.OK,
                                 message_format=message)
        if window:
            dialog.set_transient_for(window)
        dialog.run()
        dialog.destroy()
