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


class History:
    def __init__(self):
        self.reset()

    def addtohistory(self,index,origrow,origcol,newrow,newcol):
        self.history[self.historyindex:self.historyindex]\
                  =[(index,origrow,origcol,newrow,newcol)]
        del self.history[self.historyindex+1:]
        self.historyindex=self.historyindex +1
        self.maxhistory=self.historyindex

    def backinhistory(self):
        self.historyindex=self.historyindex-1
        return self.history(self.historyindex)

    def forwardinhistory(self):
        self.historyindex=self.historyindex+1
        return self.history(self.historyindex)

    def beginningofhistory(self):
        self.historyindex=0

    def forwardinhistory(self):
        self.historyindex=self.historyindex+1

    def backinhistory(self):
        self.historyindex=self.historyindex-1

    def nextmove(self):
        return self.history[self.historyindex]

    def lastmove(self):
        return self.history[self.historyindex-1]

    def startofhistory(self):
        return self.historyindex==0

    def endofhistory(self):
        return self.historyindex==self.maxhistory

    def gotoendofhistory(self):
        self.historyindex=self.maxhistory

    def reset(self):
        self.history=[]
        self.historyindex=0
        self.maxhistory=0

    def nrofmovestaken(self):
        return self.historyindex

    def save_bag(self,propertybag):
        propertybag['historyindex']=self.historyindex
        propertybag['history']=self.history

    def default_bag(self,propertybag):
        propertybag['history']=[]
        propertybag['historyindex']=0

    def load_bag(self,propertybag):
        self.history=propertybag['history']
        self.historyindex=propertybag['historyindex']
        self.maxhistory=len(self.history)
