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
np = Misc.normalize_path

def readint(fp):
    # make sure we don't get bitten by endianness.
    # In Python 3, reading bytes returns bytes; indexing bytes gives int directly.
    r = fp.read(4)
    return (r[3] << 24) + (r[2] << 16) + (r[1] << 8) + r[0]

class LevelFileParser:
    def __init__(self, file=np("ttraffic.levels")):
        self.file = file
        self.readdirectory()

    def readdirectory(self):
        self.directory = {}
        with open(self.file, "rb") as fp:
            self.minmovestosolution = readint(fp)
            self.mostcomplexsolution = readint(fp)
            self.directory[0] = self.minmovestosolution
            self.directory[1] = self.mostcomplexsolution
            self.entriesindirectory = self.mostcomplexsolution \
                                     - self.minmovestosolution + 2
            for i in range(1, self.entriesindirectory+1):
                self.directory[i+1] = readint(fp)

    def getboard(self, offset):
        with open(self.file, "rb") as fp:
            fp.seek(offset)
            rows = readint(fp)
            columns = readint(fp)
        return Board.Board((rows, columns))
