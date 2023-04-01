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

import LevelFileParser
import random

class LevelSelector:
    def __init__(self,solvedlevels=[]):
        self.levelfileparser=LevelFileParser.LevelFileParser()
        self.solvedlevels=solvedlevels
        self.slicedsolvedlevels_cache=None

    def insertinsolvedlevels(self,offset):
        self.slicedsolvedlevels_cache=None
        self.solvedlevels.append(offset)
        self.solvedlevels.sort()

    #sets slicedsolvedlevels to levels >= b and < e
    #should be done with filter!
    
    def  slicesolvedlevels (self,b,e):
        if (self.slicedsolvedlevels_cache!=None)\
           and self.bprev==b and self.eprev==e:
            return self.slicedsolvedlevels_cache
        else:
            slicedsolvedlevels=[]
            for i in self.solvedlevels:
                if (b <= i)  and (i<e):
                    slicedsolvedlevels.append(i)
            self.bprev=b
            self.eprev=e
            self.slicedsolvedlevels_cache=slicedsolvedlevels
            return slicedsolvedlevels

    def offsetsavailable(self,b,e,existing=0):
        slicedsolvedlevels=self.slicesolvedlevels(b,e)
        length=len(slicedsolvedlevels)
        #this is really 8 times the available slots!
        if existing:
            availableslots=e-b
        else:
            availableslots= e-b-8*length
        return availableslots

    def offsetsavailableEx(self,min,max,existing):
        return self.offsetsavailable(self.tooffset(min),
                                     self.tooffset(max),
                                     existing)

    def offsetstotal(self,min,max):
        return (self.tooffset(max)-self.tooffset(min))/8

    def solvedlevelsbetweenbounds(self,min,max):
#should be done with filter!
        b=self.tooffset(min)
        e=self.tooffset(max)
        count=0
        for i in self.solvedlevels:
            if (b <= i)  and (i<e):
                count=count+1
        return count
    
    # finds a random nonsolved level between offsets >=b and <e
    # It is the responsibility of the caller that offsets are left

    def randomoffset(self,b,e,existing):
        slicedsolvedlevels=self.slicesolvedlevels(b,e)
        availableslots=self.offsetsavailable(b,e,existing)
        preoffset=b+8*random.randrange(0,availableslots/8)
        if not existing:
            for i in slicedsolvedlevels:
                if preoffset >= i:
                    preoffset=preoffset+8
        return preoffset

    #eliminates all b<= . <e from solvedlevels

    def resetsolvedlevels(self,b,e):
        self.slicedsolvedlevels_cache=None
        newsolvedlevels=[]
        for i in self.solvedlevels:
            if (i < b) or (i >= e):
                newsolvedlevels.append(i)
        self.solvedlevels=newsolvedlevels

    def resetsolvedlevelsEx(self,minmoves,maxmoves):
        return self.resetsolvedlevels(self.tooffset(minmoves),
                                 self.tooffset(maxmoves))

    def getboard(self,offset):
        return self.levelfileparser.getboard(offset)


    # returns a level >=minmoves <maxmoves
    # return offset in file,
    # it is the resposibility of the caller to make sure
    # levels are available

    
    def tooffset(self,move):
        levelfileparser=self.levelfileparser
        place=move - levelfileparser.minmovestosolution +2
        return levelfileparser.directory[place]
        
    def randomlevel(self,minmoves,maxmoves,existing):
        levelfileparser=self.levelfileparser
        beginoffset=self.tooffset(minmoves)
        endoffset=self.tooffset(maxmoves)
        offset=self.randomoffset(beginoffset,endoffset,existing)
        board=self.getboard(offset)
        for  p in range(minmoves,maxmoves):
            directoryentry=\
                            levelfileparser.directory[p -\
                            levelfileparser.minmovestosolution + 2 + 1]
            if directoryentry > offset:
                bestyoucando=p 
                break
        return (offset,bestyoucando,board)
        
    def save_bag(self,propertybag):
        propertybag['solvedlevels']=self.solvedlevels

    def default_bag(self,propertybag):
        propertybag['solvedlevels']=[]
         
    def load_bag(self,propertybag):
        self.solvedlevels=propertybag['solvedlevels']
# backwards compatibility
# earlier versions inserted zeroes,
# eliminate these
	self.solvedlevels=[x for x in self.solvedlevels if x!=0]

if __name__=='__main__':
    l=LevelSelector()
    print(l.randomlevel(30,40))

