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


import copy, LevelSelector, Board, History, Hint
import PropertyBag,Misc

np=Misc.normalize_path

class GameState:
    def __init__(self):
        self.levelselector=LevelSelector.LevelSelector()
        self.history=History.History()
# this one is special, it is only saved, not loaded
        config_db=PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
        config_db.load(all=True)
        self.ptversion=config_db["version"]
        self.statistics={}
        self.statistics['Trivial']={}
        self.statistics['Easy']={}
        self.statistics['Intermediate']={}
        self.statistics['Advanced']={}
        self.statistics['Expert']={}
        for type in ('Trivial','Easy'):
            self.statistics[type]['Solved']=0
        for type in ('Intermediate','Advanced','Expert'):
            movebounds=self.movebounds(type)
            self.statistics[type]['Solved']=0
            self.statistics[type]['Total']=self.levelselector.offsetstotal(
                movebounds[0],movebounds[1])

    def movebounds(self,type):
        if type=='Trivial':
            b=2
            e=8
        elif type=='Easy':
            b=8
            e=21
        elif type=='Intermediate':
            b=21 
            e=31
        elif type=='Advanced':
            b=31 
            e=41
        elif type=='Expert':
            b=41 
            e=52
        return (b,e)

    def domove(self,index,row,col):
        origrow,origcol,h,l=self.board.getttrafficboard()[index]
        if (origrow!=row) or (origcol!=col):
            self.history.addtohistory(index,origrow,origcol,row,col)
            self.board.domove(index,row,col)
            self.endboard=self.board
            
    def insertinsolvedlevels(self):
	if not self.dontinsert:
        	self.levelselector.insertinsolvedlevels(self.offset)

    def offsetsavailable(self,type,existing=0):
        if type=='Trivial' or type=='Easy':
            return 1
        else:
            min,max=self.movebounds(type)
            return self.levelselector.offsetsavailableEx(min,max,existing)
    
    def resetsolvedlevels(self,type):
        min,max=self.movebounds(type)
        self.statistics[type]['Solved']=0
        return self.levelselector.resetsolvedlevelsEx(min,max)

    def randomlevel(self,type,existing):
        b,e=self.movebounds(type)
        if type=='Trivial' or type=='Easy':
            l=Hint.findlevel(b,e)
            return (0,l[0],Board.Board((l[1],l[2])))
        else:
            return self.levelselector.randomlevel(b,e,existing)

    def new(self,existing=0):
        # it is the responsibility of the caller to make sure games are
        # available
        if existing:
            self.dontinsert=1
        else:
            self.dontinsert=0
        randomlevel=self.randomlevel(self.type,existing)
        self.hint=0
        self.history.reset()
        self.offset,self.bestyoucando,self.originalboard=randomlevel
        if self.offset==0:
            self.dontinsert=1
        self.youvewon=0
        self.board=copy.deepcopy(self.originalboard)
        self.endboard=copy.deepcopy(self.originalboard)

    def findbestmove(self):
        return self.board.findbestmove()

    def play_area(self,index):
        return self.board.play_area(index)

    def redcarout(self):
        return self.board.redcarout()

    def testlegality(self,index,row,col):
        return self.board.testlegality(index,row,col)

    def getttrafficboard(self):
        return self.board.getttrafficboard()

    def restart(self):
        if self.history.endofhistory():
            self.endboard=copy.deepcopy(self.board)
        self.history.beginningofhistory()
        self.board.update(self.originalboard)

    def gotoend(self):
        self.history.gotoendofhistory()
        self.board.update(self.endboard)
        
    def nextmove(self):
        return self.history.nextmove()

    def lastmove(self):
        return self.history.lastmove()
    
    def redo(self):
        index,origrow,origcol,row,col=self.nextmove()
        self.history.forwardinhistory()
        self.board.domove(index,row,col)

    def undo(self):
        index,origrow,origcol,row,col=self.lastmove()
        if self.history.endofhistory():
            self.endboard=copy.deepcopy(self.board)
        self.history.backinhistory()
        self.board.domove(index,origrow,origcol)

    def startofhistory(self):
        return self.history.startofhistory()

    def endofhistory(self):
        return self.history.endofhistory()

    def nrofmovestaken(self):
        return self.history.nrofmovestaken()

    def won(self):
        self.youvewon=1
        self.solvedinnrofmoves=self.nrofmovestaken()
        if not self.dontinsert:
            self.statistics[self.type]['Solved']=\
                      self.statistics[self.type]['Solved']+1
            self.insertinsolvedlevels()

    def solvedlevelsbetweenbounds(self,min,max):
        return self.levelselector.solvedlevelsbetweenbounds(min,max)

    def save_bag(self,propertybag):
        self.history.save_bag(propertybag)
        self.originalboard.save_bag(propertybag,key='originalboard')
        self.levelselector.save_bag(propertybag)
        propertybag['offset']=self.offset
        propertybag['youvewon']=self.youvewon
        propertybag['type']=self.type
        propertybag['bestyoucando']=self.bestyoucando
        propertybag['hint']=self.hint
        propertybag['ptversion']=self.ptversion
        propertybag['solvedinnrofmoves']=self.solvedinnrofmoves
        propertybag['dontinsert']=self.dontinsert
	propertybag['easteregg']=self.easteregg

    def default_bag(self,propertybag):
        self.history.default_bag(propertybag)
        self.levelselector.default_bag(propertybag)
        propertybag['dontinsert']=0
        propertybag['hint']=0
        propertybag['offset']=0
        propertybag['originalboard']=None
        propertybag['bestyoucando']=0
        propertybag['youvewon']=0
        propertybag['type']="Intermediate"
        propertybag['solvedinnrofmoves']=0
        propertybag['ptversion']=self.ptversion
	propertybag['easteregg']=1
        
    def load_bag(self,propertybag):
        self.history.load_bag(propertybag)
        self.levelselector.load_bag(propertybag)
        self.originalboard=Board.Board()
        self.originalboard.load_bag(propertybag,key='originalboard')
        self.offset=propertybag['offset']
        self.youvewon=propertybag['youvewon']
        self.bestyoucando=propertybag['bestyoucando']
        self.hint=propertybag['hint']
        self.type=propertybag['type']
        self.solvedinnrofmoves=propertybag['solvedinnrofmoves']
        self.dontinsert=propertybag['dontinsert']
	self.easteregg=propertybag['easteregg']
# feeble attempt at backwards compatibility for earlier versions of the
# save file
        if self.offset!=0:
            self.originalboard=self.levelselector.getboard(self.offset)
        elif propertybag['originalboard']==None:
# this may crash things if the user has modified the save file,
# but then all bets are off anyway
             self.new()

        self.statistics['Intermediate']['Solved']=\
             self.solvedlevelsbetweenbounds(
                    self.movebounds('Intermediate')[0],
                    self.movebounds('Intermediate')[1])
        self.statistics['Advanced']['Solved']=\
             self.solvedlevelsbetweenbounds(
                    self.movebounds('Advanced')[0],
                    self.movebounds('Advanced')[1])
        self.statistics['Expert']['Solved']=\
             self.solvedlevelsbetweenbounds(
                    self.movebounds('Expert')[0],
                    self.movebounds('Expert')[1])

        self.endboard=copy.deepcopy(self.originalboard)
        self.board=copy.deepcopy(self.originalboard)
        moveindex=0
        for move in self.history.history:
            index,origrow,origcol,row,col=move
            self.endboard.domove(index,row,col)
            if moveindex<self.history.historyindex:
                self.board.domove(index,row,col)
            moveindex=moveindex+1
            
        



