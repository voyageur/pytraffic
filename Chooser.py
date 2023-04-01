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

import copy
import random

RANDOM=0
REPEAT=1


class Chooser:

    def __init__(self,list,refresh_message=None, strategy=RANDOM):
        if not( strategy in (RANDOM,REPEAT)):
            raise Exception("Unsupported strategy")
        self.__list=list
        self.__is_empty=0
        if list==[]:
            self.__is_empty=1
        self.__work_list=copy.copy(list)
        self.__refresh_message=refresh_message
        self.__dirty=0
        self.__strategy=strategy

    def set_strategy(self,strategy):
        self.__strategy=strategy

    def get_strategy(self):
        return self.__strategy

    def is_empty(self):
        return self.__is_empty

    def get(self):
        if self.__is_empty:
            raise Exception("Cannot choose from empy list")
        if self.__strategy==RANDOM:
            selection=random.choice(self.__work_list)
        else:
            selection=self.__work_list[0]
        self.__work_list.remove(selection)
        self.__dirty=1
        if self.__work_list==[]:
            self.reset()
        return selection

    def reset(self):
        if self.__dirty:
            self.__work_list=copy.copy(self.__list)
            self.__dirty=0

    def __str__(self):
        return str(self.__list)
