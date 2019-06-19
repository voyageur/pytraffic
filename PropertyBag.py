
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

import UserDict
import ConfigParser
import os

class PropertyBag(UserDict.UserDict):
    def __init__(self, configfile="", title="Main",comment=None):
        UserDict.UserDict.__init__(self)
        self.__title=title
        self.__configfile=configfile
	self.__comment=comment

    def setconfigfile(self,configfile):
        self.__configfile=configfile
            
    def save(self):
        fp=open(self.__configfile,"w")
	if self.__comment!=None:
		fp.write(";; %s\n" % self.__comment)
        fp.write("[%s]\n" % self.__title)
        for (key,item) in self.items():
            fp.write("%s=%s\n" % (key,repr(item)))
        fp.close()

    def load(self,all=False):
        c=ConfigParser.ConfigParser()
        if not os.access(self.__configfile,os.F_OK):
            return
        c.read(self.__configfile)
        for key in c.options(self.__title):
            if key!='__name__'  and (all or self.has_key(key)):
                item=eval(c.get(self.__title,key))
                self[key]=item
        
            
