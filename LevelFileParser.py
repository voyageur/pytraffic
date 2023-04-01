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

import random
import Misc, Board
np=Misc.normalize_path

def readint(fp):
    # make sure we don't get bitten by endiannes.
    r=fp.read(4)
    return (ord(r[3])<<24)+(ord(r[2])<<16)+(ord(r[1])<<8)+ord(r[0])

class LevelFileParser:
    def __init__(self,file=np("ttraffic.levels")):
        self.file=file
        self.readdirectory()
        
    def readdirectory(self):
        self.directory={}
        self.fp=open(self.file,"rb")
        self.minmovestosolution=readint(self.fp)
        self.mostcomplexsolution=readint(self.fp)
        self.directory[0]=self.minmovestosolution
        self.directory[1]=self.mostcomplexsolution
        self.entriesindirectory=self.mostcomplexsolution\
                                 -self.minmovestosolution+2
        for  i in range(1,self.entriesindirectory+1):
            self.directory[i+1]=readint(self.fp)

    def getboard(self,offset):
        self.fp.seek(offset)
        rows=readint(self.fp)
        columns=readint(self.fp)
        return Board.Board((rows,columns))






