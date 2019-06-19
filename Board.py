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




import Hint

gtrafficstrips= (
  ( (0, 0), (0, 0) ), 
  ( (0, 2), (0, 0) ), 
  ( (1, 2), (0, 0) ), 
  ( (2, 2), (0, 0) ), 
  ( (3, 2), (0, 0) ), 
  ( (4, 2), (0, 0) ), 
  ( (0, 3), (0, 0) ), 
  ( (1, 3), (0, 0) ), 
  ( (2, 3), (0, 0) ), 
  ( (3, 3), (0, 0) ), 
  ( (0, 2), (2, 2) ), 
  ( (0, 2), (3, 2) ), 
  ( (0, 2), (4, 2) ), 
  ( (1, 2), (3, 2) ), 
  ( (1, 2), (4, 2) ), 
  ( (2, 2), (4, 2) ) 
)


def ttrafficboardtostring(ttrafficboard):
        s=""
        physicalboard={}
        for row in xrange(0,6):
            for column in xrange(0,6):
                physicalboard[(row,column)]='.'
        a=ord('a')
        for car in ttrafficboard:
            row,col,horizontal,length=car
            for i in xrange(0,length):
                if horizontal:
                    if physicalboard[(row,col+i)]=='.':
                        physicalboard[(row,col+i)]=chr(a)
                    else:
                        physicalboard[(row,col+i)]='*'
                else:
                    if physicalboard[(row+i,col)]=='.':
                        physicalboard[(row+i,col)]=chr(a)
                    else:
                        physicalboard[(row+i,col)]='*'
            a=a+1
        for  row in xrange(0,6):
            for column in xrange(0,6):
                s=s+physicalboard[(row,column)]
            s=s+"\n"
        return s


def unpackboard (packedboard):
    r=packedboard[0]
    c=packedboard[1]
    unpackedboard=[]
    for i in xrange(0,6):
	unpackedboard.append(r & 0xF)
	r=r >> 4
    for i in xrange(6,12):
	unpackedboard.append(c & 0xF)
	c=c >> 4
    return unpackedboard


def packboard(unpackedboard):
    r=0
    c=0
    for i in xrange(0,6):
       r=r+(unpackedboard[i]<<(4*i))
       c=c+(unpackedboard[6+i]<<(4*i))
    return (r,c)

def tottrafficboard(unpackedboard):
    originalboard=[]
    for i in xrange(0,12):
        stripnr=unpackedboard[i]
        for j in (0,1):
	    g=  gtrafficstrips[stripnr][j]
	    carpos=g[0]
	    carlength=g[1]
            if carlength:
                if i<=5:
		    originalboard.append([i,carpos,1,carlength])
		else:
		    originalboard.append([carpos,i-6,0,carlength])
    return originalboard

def tounpackedboard(ttrafficboard):
    temp=[]
    for i in xrange(0,6):
        validcarlist=[]
        for c in ttrafficboard:
            row,col,horizontal,length=c
            if horizontal and row==i:
                validcarlist.append((col,length))
        temp.append(validcarlist)
    for i in xrange(6,12):
        validcarlist=[]
        for c in ttrafficboard:
            row,col,horizontal,length=c
            if not(horizontal) and col+6==i:
                validcarlist.append((row,length))
        temp.append(validcarlist)
    unpackedboard=[]
    for j in xrange(0,12):
        validcarlist=temp[j]
        validcarlist.sort()
        for i in xrange(len(validcarlist),2):
            validcarlist.append((0,0))
        validcarlist=tuple(validcarlist)
        for k in xrange(0,len(gtrafficstrips)):
            if gtrafficstrips[k]==validcarlist:
                unpackedboard.append(k)
    if len(unpackedboard)<12:
        raise KeyError
    return unpackedboard
        
def tophysicalboard (ttrafficboard):
    physicalboard={}
    for row in xrange(0,6):
        for column in xrange(0,6):
	    physicalboard[(row,column)]=0

    for car in ttrafficboard:
	row,col,horizontal,length=car
        for i in xrange(0,length):
            if horizontal:
		physicalboard[(row,col+i)]=1
	    else:
		physicalboard[(row+i,col)]=1
    return physicalboard

# __ttrafficboard is always up to date
# other representations of board are
# computed on the fly and chached

class Board:
    def __init__(self,a=[]):
        self.init()
        if type(a)==type([]):
            self.__ttrafficboard=a
        elif type(a)==type(()):
            self.__unpackedboard=unpackboard(a)
            self.__ttrafficboard=tottrafficboard(self.__unpackedboard)

    def init(self):
        self.__ttrafficboard=None
        self.__packedboard=None
        self.__physicalboard=None
        self.__unpackedboard=None

    def getttrafficboard(self):
        return self.__ttrafficboard

    def getphysicalboard(self,cache=1):
        newphysicalboard=self.__physicalboard
        if newphysicalboard==None:
            newphysicalboard=tophysicalboard(self.__ttrafficboard)
            if cache:
                self.__physicalboard=newphysicalboard
        return newphysicalboard

    def getunpackedboard(self,cache=1):
        newunpackedboard=self.__unpackedboard
        if newunpackedboard==None:
            newunpackedboard=tounpackedboard(self.__ttrafficboard)
            if cache:
                self.__unpackedboard=newunpackedboard
        return newunpackedboard

    def getpackedboard(self,cache=1):
        newpackedboard=self.__packedboard
        if newpackedboard==None:
            newunpackedboard=self.getunpackedboard(cache)
            newpackedboard=packboard(newunpackedboard)
            if cache:
                self.__packedboard=newpackedboard
        return newpackedboard

    def findbestmove(self):
        t0=self.__ttrafficboard
        t1=Board(Hint.bestmove(self.getpackedboard())).getttrafficboard()
        for i in t1:
            if not(i in t0):
                row=i[0]
                col=i[1]
        for i in t0:
            if not(i in t1):
                index=t0.index(i)
        return [index,row,col]
        
    #new board must have same size as old board

    def update(self,newboard):
        newboard=newboard.getttrafficboard()
        if len(newboard)!=len(self.__ttrafficboard):
            raise KeyError
        savedttrafficboard=self.__ttrafficboard
        self.init()
        self.__ttrafficboard=savedttrafficboard
        for i in xrange(0,len(newboard)):
            self.__ttrafficboard[i]=newboard[i]
        
    def domove(self,index,row,column):
        oldrow,oldcolumn,horizontal,length=self.__ttrafficboard[index]
        savedttrafficboard=self.__ttrafficboard
        self.init()
        self.__ttrafficboard=savedttrafficboard
        self.__ttrafficboard[index]=[row,column,horizontal,length]

    def play_area(self,index):
	    physicalboard=self.getphysicalboard(cache=0)
# cache=0 is necessary since we will be changing physicalboard
	    row,column,horizontal,length=self.__ttrafficboard[index]
	    if(horizontal):
		    toprow=row
		    bottomrow=row
	            #remove current car
		    for i in xrange(0,length):
			    physicalboard[(row,column+i)]=0
		    #find left bound
		    leftcolumn=column
		    found=0
		    while not(found):
			    if leftcolumn==-1:
				    found=1
			    elif physicalboard[(row,leftcolumn)]==1:
				    found=1
			    else:
				    leftcolumn=leftcolumn-1
		    #we've overshot by one
		    leftcolumn=leftcolumn+1
		    #find rightbound
		    rightcolumn=column
		    found=0
		    while not(found):
			    if rightcolumn+length-1==6:
				    found=1
			    elif physicalboard[(row,rightcolumn+length-1)]==1:
				    found=1
			    else:
				    rightcolumn=rightcolumn+1
		    #we've overshot by one
		    rightcolumn=rightcolumn-1
	    else:
		    leftcolumn=column
		    rightcolumn=column
	            #remove current car
		    for i in xrange(0,length):
			    physicalboard[(row+i,column)]=0
		    #find top bound
		    toprow=row
		    found=0
		    while not(found):
			    if toprow==-1:
				    found=1
			    elif physicalboard[(toprow,column)]==1:
				    found=1
			    else:
				    toprow=toprow-1
		    #we've overshot by one
		    toprow=toprow+1
		    #find bottombound
		    bottomrow=row
		    found=0
		    while not(found):
			    if bottomrow+length-1==6:
				    found=1
			    elif physicalboard[(bottomrow+length-1,column)]==1:
				    found=1
			    else:
				    bottomrow=bottomrow+1
		    #we've overshot by one
		    bottomrow=bottomrow-1

	    return (toprow,bottomrow,leftcolumn,rightcolumn)

    def redcarout(self):
        return ([2,4,1,2] in self.__ttrafficboard)

    def testlegality(self,index,row,column):
        legal=1
        car=self.__ttrafficboard[index]
        carrow,carcolumn,horizontal,length=car
        if  (row>=6) or (row<0) or (column<0) or (column>=6):
            legal=0
        elif horizontal and ((column +length) > 6):
            legal=0
        elif not(horizontal) and ((row +length) > 6):
            legal=0
        elif horizontal and (carrow!=row):
            legal=0
        elif not(horizontal) and (carcolumn!=column):
            legal=0
        elif horizontal and (column >= carcolumn):
            for  i in xrange(carcolumn,column):
                if self.getphysicalboard()[(row,i+length)]==1:
                    legal=0
        elif horizontal and (column <= carcolumn):
            for i in xrange(column,carcolumn):
                if self.getphysicalboard()[(row,i)]==1:
                    legal=0
        elif not(horizontal) and (row >= carrow):
            for i in xrange(carrow,row):
                if self.getphysicalboard()[(i+length,column)]==1:
                    legal=0
        elif  not(horizontal) and (row <= carrow):
            for i in xrange(row,carrow):
                if self.getphysicalboard()[(i,column)]==1:
                    legal=0
	return legal

    def save_bag(self,propertybag,key='board'):
        propertybag[key]=self.__ttrafficboard
        
    def load_bag(self,propertybag,key='board'):
        self.init()
        self.__ttrafficboard=propertybag[key]


class TestBoard(Board):
    def __init__(self):
        Board.__init__(self,[[0,0,0,2],[0,2,1,2],[0,4,1,2],[1,1,1,3],
	    [1,5,0,2],[2,0,1,2],[2,2,0,2],[2,3,0,2],
	    [3,4,1,2],[4,1,1,3],[4,4,0,2],[4,5,0,2],
	    [5,1,1,3]])

class SimpleTestBoard(Board):
    def __init__(self):
        Board.__init__(self,[[2,0,1,2]])
        




if __name__=='__main__':
    t=TestBoard()
    print ttrafficboardtostring(t.getttrafficboard())
    for i in xrange(0,13):
	    print t.play_area(i)
    
