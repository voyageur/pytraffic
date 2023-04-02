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




import sys
import Misc
import copy
import CondMessageBox
import GameState
import Canvas
from gi.repository import GObject
from gi.repository import Gtk

import Board


class Car:
    def __init__(self,arena,row=0,col=0,horizontal=1,truck=0,red=0,id=0):
        self.horizontal=horizontal
        self.truck=truck
        self.arena=arena
        self.id=id
        self.row=row
        self.col=col
        if not(red):
            self.artwork=arena.artwork.getartwork(horizontal,truck)
        else:
            self.artwork=arena.artwork.getRedCar()
        x,y=Misc.togridpoint(row,col)
        image,basepoint=self.artwork['normal']
        bpx,bpy=basepoint
        self.im=Canvas.ScreenImageItem(image,bpx,bpy)
        arena.add(x,y,self.im)
        bpx,bpy=basepoint
        self.init_drag_and_drop()
        self.im.connect("button_press_event",self.do_popup)
        self.enable()

    def disable(self):
        self.disabled=1

    def enable(self):
        self.disabled=0

    def do_popup(self,widget,event,*args):
        if event.button!=3:
            return False
        if self.arena.gamestate.easteregg:
            self.arena.popup.popup(None,
                                   None,
                                   None,
                                   event.button,
                                   event.get_time())
        return True

    def init_drag_and_drop(self):
        self.im.connect("button_press_event",self.startdrag)
        self.im.connect("motion_notify_event",self.drag)
        self.im.connect("button_release_event",self.enddrag)
        self.dragging=0

    def update_cursor(self):
        toprow,bottomrow,leftcolumn,rightcolumn=\
                          self.arena.gamestate.play_area(self.id)
        if ((toprow!=bottomrow) or (leftcolumn!=rightcolumn)) \
                             and not(self.disabled):
            if self.horizontal:
#                self.im.set_cursor(Gdk.Cursor.new(Gdk.SB_H_DOUBLE_ARROW))
                self.im.set_cursor(Gdk.Cursor.new(Gdk.HAND2))
            else:
#                self.im.set_cursor(Gdk.Cursor.new(Gdk.SB_V_DOUBLE_ARROW))
                self.im.set_cursor(Gdk.Cursor.new(Gdk.HAND2))
        else:
            self.im.set_cursor(None)


    def destroy(self):
        self.arena.remove(self.im)

    def move(self,row,col):
        if self.arena.animation:
            self.animated_move(row,col)
        else:
            self.standard_move(row,col)

    def standard_move(self,row,col):
        x,y=Misc.togridpoint(row,col)
        self.im.set_coords(x,y)
        self.row=row
        self.col=col

# Written by Jesse Weinstein

    def move_a_bit_inner(self,cnt, dest, other, axis):
        mu=5
        delay_ms=10
        if cnt>dest and cnt-mu>=dest:
            cnt=cnt-mu
        elif cnt<dest and cnt+mu<=dest:
            cnt=cnt+mu
        else:
            cnt=dest
        if axis==0:
            self.im.set_coords(other, cnt)
        else:
            self.im.set_coords(cnt, other)
        if cnt!=dest:
            GObject.timeout_add(
                delay_ms, lambda f= self.move_a_bit_inner,
                cnt=cnt,
                dest=dest,
                other=other,
                axis=axis:f(cnt, dest, other, axis))

        return False

#    """Annimate the movement of a Car from one square to another.
#    All written by Jesse Weinstein."""

    def animated_move(self, row, col):
        ox, oy=Misc.togridpoint(self.row, self.col)
        x,y=Misc.togridpoint(row,col)
        if x==ox:
            self.move_a_bit_inner(oy, y, x, 0)
        else:
            self.move_a_bit_inner(ox, x, y, 1)
        self.row=row
        self.col=col

    def startdrag(self,window,e):
        if e.button!=1 or \
           e.type!=Gdk.EventType.BUTTON_PRESS or \
           self.disabled:
            return False
        toprow,bottomrow,leftcolumn,rightcolumn=\
                          self.arena.gamestate.play_area(self.id)
        if (toprow!=bottomrow) or (leftcolumn!=rightcolumn):
            self.arena.sound_server.play(self.artwork['engine'])
            self.dragging=1
            self.arena.lift(self.im)
            self.ddobject=self.im
            self.upperleftx,self.upperlefty=Misc.togridpoint(toprow,
                                                             leftcolumn)
            self.lowerrightx,self.lowerrighty=Misc.togridpoint(bottomrow,
                                                               rightcolumn)
            self.xorg,self.yorg=\
                        self.arena.convert_to_world_coordinates(e.x,e.y)
        else:
            self.arena.sound_server.play(self.artwork['horn'])

        return True

    def drag(self,window,e):
        ex,ey=self.arena.convert_to_world_coordinates(e.x,e.y)
        if self.dragging:
            coords=self.ddobject.get_coords()
            upperleftx,upperlefty=coords
            if self.horizontal:
                newupperleftx=ex-self.xorg+upperleftx
                if newupperleftx> self.lowerrightx:
                    newupperleftx=self.lowerrightx
                elif newupperleftx< self.upperleftx:
                    newupperleftx=self.upperleftx
                self.ddobject.move(newupperleftx-upperleftx,0)
                self.xorg=self.xorg+newupperleftx-upperleftx
            else:
                newupperlefty=ey-self.yorg+upperlefty
                if newupperlefty> self.lowerrighty:
                    newupperlefty=self.lowerrighty
                elif newupperlefty< self.upperlefty:
                    newupperlefty=self.upperlefty
                self.ddobject.move(0,newupperlefty-upperlefty)
                self.yorg=self.yorg+newupperlefty-upperlefty
        return True

    def enddrag(self,window,e):
        if self.dragging:
            self.dragging=0
            coords=self.ddobject.get_coords()
            upperleftx,upperlefty=coords
            row,col=Misc.torowcol(upperleftx,upperlefty)
            self.move(row,col)
            self.arena.domove(self.id,row,col)
            if self.arena.gamestate.redcarout():
                self.arena.doredcarout()
        return True



class Arena(Canvas.Canvas):
    np=Misc.normalize_path
    def __init__(self,game):
        Canvas.Canvas.__init__(self)
        self.game=game
        self.gamestate=game.gamestate
        self.sound_server=game.sound_server
        self.updateGUI=game.updateGUI
        self.save_all=game.save_all
        self.doredcarout=game.doredcarout
        self.artwork=game.artwork
        self.carlist=[]
        self.background=None
        self.popup=Gtk.Menu()
        self.popup_item=Gtk.MenuItem("Order this car")
        self.popup.append(self.popup_item)
        self.popup_item.show()
        self.popup_item.connect("activate",self.order)
        self.setanimation(0)

    def update_cursors(self):
        for car in self.carlist:
            car.update_cursor()

    def disable(self):
        for car in self.carlist:
            car.disable()

    def enable(self):
        for car in self.carlist:
            car.enable()

    def order(self,*args):
        self.gamestate.easteregg=0
        CondMessageBox.showinfo(message="""This feature is being worked on. Please check in later. ;-)""",
                                window=self.game.window)

    def domove(self,index,row,col):
        self.gamestate.domove(index,row,col)
        self.updateGUI()

    def setupboard (self):
        self.artwork.reset()
        self.set_world_to_screen_transform(self.artwork.gettransform())
        if self.background!=None:
            self.remove(self.background_id)
        self.background,self.background_basepoint=self.artwork.getbackground()
        bpx,bpy=self.background_basepoint
        self.background_id=Canvas.ScreenImageItem(self.background,bpx,bpy)
        self.add(0,0,self.background_id)
        self.destroycars()
        self.carlist=[]
        board=self.gamestate.getttrafficboard()
        index=0
        for car in board:
            r,c,h,l=car
            if l==2:
                t=0
            else:
                t=1
            if r == 2 and h:
                c=Car(self,row=r,col=c,red=1,id=index)
            else:
                c=Car(self,row=r,col=c,horizontal=h,truck=t,id=index)
            index=index+1
            self.carlist.append(c)
        self.pack()

    def destroycars(self):
        for c in self.carlist:
            c.destroy()

    def setupboard_soft(self):
        otboard=self.gamestate.getttrafficboard()
        for c in self.carlist:
            row,col,horizontal,length=otboard[c.id]
            c.move(row,col)


    def restart(self):
        self.setanimation(True)
        self.gamestate.restart()
        self.setupboard_soft()
        self.setanimation(False)
        self.updateGUI()

    def gotoend(self):
        self.setanimation(True)
        self.gamestate.gotoend()
        self.setupboard_soft()
        self.setanimation(False)
        self.updateGUI()

    def redo(self):
        self.setanimation(True)
        index,origrow,origcol,row,col=self.gamestate.nextmove()
        self.carlist[index].move(row,col)
        self.gamestate.redo()
        self.setanimation(False)
        self.updateGUI()

    def undo(self):
        self.setanimation(True)
        index,origrow,origcol,row,col=self.gamestate.lastmove()
        self.carlist[index].move(origrow,origcol)
        self.gamestate.undo()
        self.setanimation(False)
        self.updateGUI()


    def setanimation(self,animation):
        self.animation=animation

    def getanimation(self):
        return self.animation


    def default_bag(self,propertybag):
        pass

    def load_bag(self,propertybag):
        pass

    def save_bag(self,propertybag):
        pass
