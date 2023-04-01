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

class Timer(GObject.GObject):
    __gsignals__ = {
        'tick' : (GObject.SignalFlags.RUN_FIRST, None,
                      ())
    }
    __gproperties__ = {
        'running' :  (GObject.TYPE_BOOLEAN,
                      'running property',
                      'indicates if the timer has started',
                      0,
                      GObject.PARAM_READWRITE)
        }
    def __init__(self, interval=1000):
        self.__gobject_init__()
        self.__interval=interval
        self.__afterid=None
        self.running=0

    def do_set_property(self,pspec,value):
        if pspec.name=='running':
            self.running=value
            if value:
                self.__start()
            else:
                self.__stop()
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def do_get_property(self,pspec,value):
        if pspec.name=='running':
            return self.running
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def set_running(self,value):
        self.set_property('running',value)

    def get_running(self):
        return self.get_property('running')


    def __start(self):
        if self.__afterid==None:
            self.__afterid=GObject.timeout_add(self.__interval,
                                       self.__commandwrapper)

    def __stop(self):
        if self.__afterid!=None:
            GObject.source_remove(self.__afterid)
            self.__afterid=None

    def __commandwrapper(self):
        self.emit("tick")
        return True

#
#    def __del__(self):
#        print "stopping timer"
#        self.__stop()


GObject.type_register(Timer)


class Idler(GObject.GObject):
    __gsignals__ = {
        'tick' : (GObject.SignalFlags.RUN_FIRST, None,
                      ())
    }
    __gproperties__ = {
        'running' :  (GObject.TYPE_BOOLEAN,
                      'running property',
                      'indicates if the timer has started',
                      0,
                      GObject.PARAM_READWRITE)
        }
    def __init__(self):
        self.__gobject_init__()
        self.__afterid=None
        self.running=0

    def do_set_property(self,pspec,value):
        if pspec.name=='running':
            self.running=value
            if value:
                self.__start()
            else:
                self.__stop()
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def do_get_property(self,pspec,value):
        if pspec.name=='running':
            return self.running
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def set_running(self,value):
        self.set_property('running',value)

    def get_running(self):
        return self.get_property('running')


    def __start(self):
        if self.__afterid==None:
            self.__afterid=GObject.idle_add(self.__commandwrapper)

    def __stop(self):
        if self.__afterid!=None:
            GObject.source_remove(self.__afterid)
            self.__afterid=None

    def __commandwrapper(self):
        self.emit("tick")
        return True

#    Sigh...del method do not work...
#   http://www.daa.com.au/pipermail/pygtk/2003-March/004624.html
#
#
#    def __del__(self):
#        self.__stop()

GObject.type_register(Idler)





if __name__=='__main__':
    def print_something(timer):
        global t
        print(timer)
        print("Hallo")
        t=None
    t=Timer(interval=1000)
#    t.connect("tick",print_something)
#    t.set_property('running',True)
    print(t.__grefcount__)
    del t
    Gtk.main()

