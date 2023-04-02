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

from gi.repository import Gdk,Gtk
import ImageCache
import Affine2D
import math

DUMMY=0
IMAGE=1

class SmartRectangle(Gdk.Rectangle):

    def __init__(self,x=0,y=0,width=0,height=0):
        x=int(x+0.5)
        y=int(y+0.5)
        Gdk.Rectangle.__init__(self,x,y,width,height)

    def translate(self,s,t):
        self.x=self.x+s
        self.y=self.y+t
        return self

    def copy(self):
        return SmartRectangle(self[0],self[1],self[2],self[3])

    def union(self,rectangle):
        r=Gdk.Rectangle.union(self.copy(),rectangle)
        return SmartRectangle(r[0],r[1],r[2],r[3])

    def intersect(self,rectangle):
        r=Gdk.Rectangle.intersect(self.copy(),rectangle)
        return SmartRectangle(r[0],r[1],r[2],r[3])

    def union_translate(self,s,t):
        return self.union(self.copy(),self.translate(s,t))

    def contains(self,x,y):
        return self.x <= x and x < self.x+self.width and \
               self.y <= y and y < self.y+self.height

    def is_empty(self):
        return self.x==0 and self.y==0 and self.width==0 and self.height==0

    def __str__(self):
        return "(%s,%s,%s,%s)" % (self.x,self.y,self.width,self.height)

empty=SmartRectangle(0,0,0,0)

# Some conventions.
# Screen coordinates are always non-negative. Things with strictly negative
# coordinates are ignored. In other words there is no notion of a viewport.
# Bounding boxes are always in screen coordinates.
# Other coordinates are normally world coordinates unless otherwise
# specified.
# Mouse pointers (in events) are screen coordinates.

class CanvasItem:

    def __init__(self):
        global DUMMY
        self.type=DUMMY
        self.bbox=empty.copy()
        self.event_handlers={}
        self.canvas=None
        self.cursor=None

    def _add(self,canvas,x,y,tag):
        self.canvas=canvas
        self.x=x
        self.y=y
        self.tag=tag

    def set_coords(self,x,y):
#       self.basepointx_rel_screen and self.basepointy_rel_screen
#       give the relative position of the base point with respect to the
#       origin of the bounding box in screen coordinates. They should be
#       defined in a subclass. It seems we cannot compute them on the fly
#       using the current basepoint and bounding box since this would
#       accumulate rounding errors.

        if not self.bbox.is_empty():
            bbox_orig=self.bbox.copy()
            x_screen, y_screen=self.canvas.convert_to_screen_coordinates(\
                                              x,y)
            self.bbox=SmartRectangle(x_screen-self.basepointx_rel_screen,
                                     y_screen-self.basepointy_rel_screen,
                                     self.bbox.width,
                                     self.bbox.height)
            clip_rectangle=bbox_orig.union(self.bbox)
        else:
            clip_rectangle=empty
        self.canvas.refresh(clip_rectangle)
        self.canvas.handle_mouse_over()
        self.x=x
        self.y=y


    def move(self,s,t):
        self.set_coords(self.x+s,self.y+t)

    def get_coords(self):
        return (self.x,self.y)

    def draw(self,clip_rectangle):
        pass

# for debugging purposes
    def draw_bbox(self):
        our_gc=Gdk.GC(self.canvas.window)
        our_gc.copy(self.canvas.style.black_gc)
#        our_gc.set_clip_rectangle(self.bbox)
        color_map=self.canvas.window.get_colormap()
        red=Gdk.color_parse("red")
        red=color_map.alloc_color(red)
        blue=Gdk.color_parse("blue")
        blue=color_map.alloc_color(blue)
        our_gc.set_values(line_width=4,
                          foreground=red,
                          background=red)
        self.canvas.window.draw_rectangle(our_gc,
                                                  False,
                                             self.bbox.x,self.bbox.y,
                                             self.bbox.width,self.bbox.height)
        our_gc.set_values(line_width=0,
                          foreground=blue,
                          background=blue)
        x,y=self.canvas.convert_to_screen_coordinates(self.x,self.y)
        x=int(x+0.5)
        y=int(y+0.5)
        self.canvas.window.draw_rectangle(our_gc,
                                          True,
                                          int(x-5),
                                          int(y-5),10,10)


    def get_bbox(self):
        return self.bbox

    def get_type(self):
        return self.type

# should be overridden
# note the use of screen coordinates
    def contains(self,x_screen,y_screen):
        return False

    def connect(self,event_type,function):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type]=[function]
        else:
            self.event_handlers[event_type].append(function)

    def handle_event(self,event_type,event):
        if event_type=="enter_notify_event":
            self.canvas.window.set_cursor(self.cursor)
        elif  event_type=="leave_notify_event":
            self.canvas.window.set_cursor(None)

        if event_type not in self.event_handlers:
            return False
        else:
            handled=False
            for handler in self.event_handlers[event_type]:
                handled=handler(self,event)
                if handled==True:
                    break
            return handled

    def set_cursor(self,cursor):
        self.cursor=cursor
        if self.canvas and self.canvas.window:
            if self==self.canvas.get_under_mouse():
                self.canvas.window.set_cursor(cursor)

#    def __str__(self):
#         return str(self.bbox)

# Specifies an image on screen.  No coordinate transform is
# applied to it (I know no good way of transforming images in
# in gtk). Hence the specified image should be pregenerated.
# Note that generally coordinates are still world coordinates.

class ScreenImageItem(CanvasItem):

    pixmap_cache=ImageCache.PixmapCache()

# base point is specified in screen coordinates!
# image is a screen image.

    def __init__(self,image,basepointx=0,basepointy=0):
        global IMAGE
        CanvasItem.__init__(self)
        self.type=IMAGE
        self.image=image
        pixbuf=image.get_pixbuf()
        self.bbox.width=pixbuf.get_width()
        self.bbox.height=pixbuf.get_height()
        self.pixmap,self.mask=ScreenImageItem.pixmap_cache.getpixmaps(image)
        self.basepointx=basepointx
        self.basepointy=basepointy
        self.basepointx_rel_screen=basepointx
        self.basepointy_rel_screen=basepointy
        self.pixels=pixbuf.get_pixels()
        self.row_stride = pixbuf.get_rowstride()

# (x_screen,y_screen) are specified in screen coordinates!

    def getRGBA(self,x_screen,y_screen):
        return (ord(self.pixels[(self.row_stride*y_screen+x_screen*4)]),
                ord(self.pixels[(self.row_stride*y_screen+x_screen*4)+1]),
                ord(self.pixels[(self.row_stride*y_screen+x_screen*4)+2]),
                ord(self.pixels[(self.row_stride*y_screen+x_screen*4)+3]))


# (x,y) is specified in world coordinates!

    def _add(self,canvas,x,y,tag):
        self.canvas=canvas
        self.x=x
        self.y=y
        x_screen,y_screen=self.canvas.convert_to_screen_coordinates(x,y)
        x_screen=int(x_screen+0.5)
        y_screen=int(y_screen+0.5)
        self.bbox.x=x_screen-self.basepointx
        self.bbox.y=y_screen-self.basepointy



    def draw(self,clip_rectangle):

        dr=self.bbox.intersect(clip_rectangle)
        if dr.is_empty():
            return
        im_origx=dr.x-self.bbox.x
        im_origy=dr.y-self.bbox.y
        our_gc=Gdk.GC(self.canvas.window)
        our_gc.copy(self.canvas.gc)
        our_gc.set_clip_origin(self.bbox.x,self.bbox.y)
        if self.mask!=None:
            our_gc.set_clip_mask(self.mask)
        self.canvas.window.draw_drawable(our_gc,self.pixmap,
                                             im_origx,im_origy,
                                             dr.x,dr.y,dr.width,dr.height)
#        self.draw_bbox()

# here we use screen coordinates.
    def contains(self,x_screen,y_screen):
# sanity check!
        x_screen,y_screen=int(x_screen+0.5),int(y_screen+0.5)
        x_screen,y_screen=x_screen-self.bbox.x,y_screen-self.bbox.y
        if x_screen>=0 and x_screen<self.bbox.width and \
           y_screen>=0 and y_screen<self.bbox.height:
           A=self.getRGBA(x_screen,y_screen)[3]
           if A!=0:
               return True
        return False



# This contains a lot of overlap with the constructor.
# Originally the common code was refactored but then it was
# hard to read.
    def set_image(self,image,basepointx=None,basepointy=None):
        if basepointx==None:
            basepointx=self.basepointx
        if basepointy==None:
            basepointy=self.basepointy
        self.image=image
        pixbuf=image.get_pixbuf()
        old_bbox=self.bbox.copy()
        self.bbox.width=pixbuf.get_width()
        self.bbox.height=pixbuf.get_height()
        self.bbox.x=old_bbox.x+self.basepointx-basepointx
        self.bbox.x=old_bbox.x+self.basepointx-basepointx
        self.pixmap,self.mask=ScreenImageItem.pixmap_cache.getpixmaps(image)
        basepointx=self.basepointx
        basepointy=self.basepointy
        self.pixels=pixbuf.get_pixels()
        self.row_stride = pixbuf.get_rowstride()
        if self.canvas!=None:
            self.canvas.refresh(self.bbox.union(old_bbox))


class FakeEvent:
    pass


class Canvas(Gtk.DrawingArea):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.set_double_buffered(False)
        gtk.DrawingArea.connect(self,"draw",
                                     self.expose_event)
        gtk.DrawingArea.connect(self,"configure-event",
                                     self.configure_event)
        gtk.DrawingArea.connect(self,"motion-notify-event",
                                     self.motion_notify_event)
        gtk.DrawingArea.connect(self,"button-press-event",
                                     self.button_press_event)
        gtk.DrawingArea.connect(self,"button-release-event",
                                     self.button_release_event)
        gtk.DrawingArea.connect(self,"enter-notify-event",
                                     self.enter_notify_event)
        gtk.DrawingArea.connect(self,"leave-notify-event",
                                     self.leave_notify_event)
        self.set_events(Gdk.EventMask.EXPOSURE_MASK
                            | Gdk.EventMask.LEAVE_NOTIFY_MASK
                            | Gdk.EventMask.ENTER_NOTIFY_MASK
                            | Gdk.EventMask.BUTTON_PRESS_MASK
                            | Gdk.EventMask.BUTTON_RELEASE_MASK
                            | Gdk.EventMask.POINTER_MOTION_MASK
                            | Gdk.EventMask.POINTER_MOTION_HINT_MASK)

        self.objects=[]
        self.gc=None
        self.selection=None
        self.under_mouse=None
        self.size_set=0
        self._pointer_cache=None
        self.event_handlers={}
        self.mb=SmartRectangle(0,0,0,0)
        self.set_world_to_screen_transform(Affine2D.identity_affine)

    def refresh(self,clip_rectangle):
        if self.window:
            self.window.invalidate_rect(clip_rectangle,False)

# Note the nature of the "set_size_request".
# As stated above we ignore things with negative coordinates.
    def add(self,x,y,object,tag=None):
        object._add(self,x,y,tag)
        self.objects.append(object)
        if self.size_set==0:
            mb=self.mb=self.mb.union(object.get_bbox())
            Gtk.DrawingArea.set_size_request(self,mb.x+mb.width,mb.y+mb.height)
        self.handle_mouse_over()

        self.refresh(object.get_bbox())

# This makes the size of the canvas as small as possible, in such a way
# that the bounding boxes of all objects are visible. Note that
# we ignore things with negative coordinates.

    def pack(self):
        self.mb=mb=SmartRectangle(0,0,0,0)
        for object in self.objects:
            mb=self.mb=self.mb.union(object.get_bbox())
        Gtk.DrawingArea.set_size_request(self,mb.x+mb.width,mb.y+mb.height)
        self.size_set=0

    def remove(self,object):
        clip_rectangle=object.get_bbox()
        self.objects.remove(object)
        if object==self.selection:
            self.selection=None
        self.handle_mouse_over()
        self.refresh(clip_rectangle)

    def lift(self,object):
        clip_rectangle=object.get_bbox()
        self.objects.remove(object)
        self.objects.append(object)
        self.handle_mouse_over()
        self.refresh(clip_rectangle)

    def get_gc(self):
        return self.gc

    def set_size_request(self,w,h):
        self.size_set=1
        Gtk.DrawingArea.set_size_request(self,w,h)

    def configure_event(self, widget, event):
        x, y, self.width, self.height = self.get_allocation()
        self.gc=self.window.new_gc()
        self.default_clip_rectangle=SmartRectangle(0,0,self.width,self.height)
        self.draw_objects()
        return True

    def draw_objects(self,clip_rectangle=None):
        if not self.gc:
            return
        if not clip_rectangle:
            clip_rectangle=self.default_clip_rectangle
        self.window.begin_paint_rect(clip_rectangle)
        self.window.draw_rectangle(self.get_style().white_gc,
                          True, clip_rectangle.x, clip_rectangle.y,
                                   clip_rectangle.width, clip_rectangle.height)
        for object in self.objects:

            object.draw(clip_rectangle)
        self.window.end_paint()

# (x_screen,y_screen) are screen coordinates
    def find_object(self,x_screen,y_screen):
        count=len(self.objects)
        for i in range(0,count):
            object=self.objects[count-1-i]
            if object.contains(x_screen,y_screen):
                return object
        return None

    def expose_event(self, widget,event):
        x , y, width, height = event.area
        self.draw_objects(clip_rectangle=event.area)
        return False


    def connect(self,event_type,function):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type]=[function]
        else:
            self.event_handlers[event_type].append(function)

    def handle_event(self,event_type,event):
        if event_type not in self.event_handlers:
            return False
        else:
            handled=False
            for handler in self.event_handlers[event_type]:
                handled=handler(self,event)
                if handled==True:
                    break
            return handled

    def button_press_event(self, widget,event):
        object=self.find_object(event.x,event.y)
        if not object:
            handled=False
        else:
            if event.type==Gdk.EventType.BUTTON_PRESS:
                self.selection=object
# this does not handle double clicks entirely correctly
# too difficult to change!
            handled=object.handle_event("button_press_event",event)
        if handled==False:
            return self.handle_event("button_press_event",event)
        return True

    def button_release_event(self, widget,event):
        if not self.selection:
            handled=False
        else:
            handled=self.selection.handle_event("button_release_event",event)
            self.selection=None
        if handled==False:
            return self.handle_event("button_release_event",event)
        return True



    def motion_notify_event(self, widget,event):
        ex,ey,es=event.window.get_pointer()
        self._pointer_cache=(ex,ey)
        e=FakeEvent()
        e.type=Gdk.MOTION_NOTIFY
        e.x=float(ex)
        e.y=float(ey)
        e.state=es
        self.handle_mouse_over()
        if not self.selection:
            handled=False
        else:
            handled=self.selection.handle_event("motion_notify_event",e)
        if handled==False:
            return self.handle_event("motion_notify_event",e)

        return True

    def enter_notify_event(self,widget,event):
        self._pointer_cache=(event.x,event.y)
        handled=self.handle_mouse_over()
        if handled==False:
            return self.handle_event("enter_notify_event",event)
        return True

    def leave_notify_event(self,widget,event):
        self._pointer_cache=(event.x,event.y)
        handled=self.handle_mouse_over()
        self._pointer_cache=None
        if handled==False:
            return self.handle_event("leave_notify_event",event)
        return True

    def handle_mouse_over(self):
        if not self._pointer_cache:
            return
        else:
            x,y=self._pointer_cache
        object=self.find_object(x,y)
        e=FakeEvent()
        e.x=x
        e.y=y
        handled_leave=False
        handled_enter=False
        if object!=self.under_mouse:
            if self.under_mouse:
                e.type=Gdk.LEAVE_NOTIFY
                handled_leave=self.under_mouse.handle_event(\
                    "leave_notify_event",e)
            if object:
                e.type=Gdk.ENTER_NOTIFY
                handled_enter=object.handle_event(\
                    "enter_notify_event",e)
            self.under_mouse=object
            return handled_leave or handled_enter
        return False

    def get_under_mouse(self):
        return self.under_mouse

    def set_world_to_screen_transform(self,transform):
        self.world_to_screen=transform
        self.screen_to_world=Affine2D.inverse_affine(transform)

    def convert_to_screen_coordinates(self,x,y):
        return Affine2D.multiply_affine_vector(self.world_to_screen,(x,y))

    def convert_to_world_coordinates(self,x_screen,y_screen):
        return Affine2D.multiply_affine_vector(self.screen_to_world,
                                               (x_screen,y_screen))

#    def convert_vector_to_screen_coordinates(self,x,y):
#        return Affine2D.multiply_matrix_vector(self.world_to_screen[0:4],
#                                                   (x,y))



import Timer

class SimpleTestApp:
    def __init__(self):
        window=Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("PyTraffic")
        window.set_resizable(False)
        window.connect("delete_event",self.quit)
        window.connect("destroy",self.quit)
        self.canvas=Canvas()
        worldtoscreen=Affine2D.multiply_affine(\
            Affine2D.translation_affine((320/math.sqrt(2),0)),
            Affine2D.rotation_affine(math.pi/4))
        self.canvas.set_world_to_screen_transform(worldtoscreen)
        image=Gtk.Image()
        image.set_from_file("background_rotated.png")
        bpx,bpy=Utils.default_basepoint(image,
                                        worldtoscreen[0:4],
                                        SmartRectangle(0,0,370,320))
        image_object=ScreenImageItem(image,bpx,bpy)
        print(image_object.row_stride)
        print(len(image_object.pixels))
        self.canvas.add(0,0,image_object)
        image_car2=Gtk.Image()
        image_car2.set_from_file("car_rotated.png")
        bpx,bpy=Utils.default_basepoint(image_car2,
                                        worldtoscreen[0:4],
                                        SmartRectangle(0,0,150,50))
        self.image_object_car2=ScreenImageItem(image_car2,bpx,bpy)
        self.canvas.add(10,10,self.image_object_car2)
        print(self.canvas.find_object(100,40))
        print(self.canvas.find_object(200,200))
        self.image_object_car2.set_cursor(Gdk.Cursor.new(\
                                         Gdk.SB_H_DOUBLE_ARROW))
        window.add(self.canvas)
        window.show_all()

    def quit(self,*args):
        Gtk.main_quit()


class TestApp:
    def __init__(self):
        window=Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("PyTraffic")
        window.set_resizable(False)
        window.connect("delete_event",self.quit)
        window.connect("destroy",self.quit)
        self.canvas=Canvas()
        f=open("themes/DeLuxe3D/transform")
        worldtoscreen=eval(f.read())
        f.close()
        image=Gtk.Image()
        image.set_from_file("themes/DeLuxe3D/background/background.png")
        f=open("themes/DeLuxe3D/background/basepoints","r")
        bpx,bpy=eval(f.read())['background.png']
        f.close()
        self.canvas.set_world_to_screen_transform(worldtoscreen)
        image_object=ScreenImageItem(image,bpx,bpy)
        self.canvas.add(0,0,image_object)
        image_car2=Gtk.Image()
        image_car2.set_from_file("themes/DeLuxe3D/cars/carHTN3.png")
        f=open("themes/DeLuxe3D/cars/basepoints","r")
        basepoints=eval(f.read())
        bpx,bpy=basepoints['carHTN3.png']
        f.close()
        self.image_object_car2=ScreenImageItem(image_car2,bpx,bpy)
        self.image_object_car2.set_cursor(Gdk.Cursor.new(\
                                         Gdk.SB_H_DOUBLE_ARROW))
        image_car=Gtk.Image()
        image_car.set_from_file("themes/DeLuxe3D/cars/carNred.png")
        bpx,bpy=basepoints['carNred.png']
        self.image_object_car=ScreenImageItem(image_car,bpx,bpy)
        self.image_object_car2.connect("button_press_event",self.startdrag)
        self.image_object_car2.connect("motion_notify_event",self.drag)
        self.image_object_car2.connect("button_release_event",self.enddrag)
        self.canvas.add(210,10,self.image_object_car)
        self.canvas.add(110,210,self.image_object_car2)
        self.x=0
        self.y=0
        self.dx=3
        self.dy=6
        self.x1=200
        self.y1=100
        self.dx1=6
        self.dy1=3
        window.add(self.canvas)
        timer=Timer.Timer(interval=10)
        timer.connect("tick",self.move_image)
        timer.set_running(1)
        window.show_all()

    def startdrag(self,widget,event):
        self.xorg, self.yorg=\
                 self.canvas.convert_to_world_coordinates(event.x,event.y)
        return True

    def drag(self,widget,event):
        x,y=self.canvas.convert_to_world_coordinates(event.x,event.y)
        widget.move(x-self.xorg,y-self.yorg)
        self.xorg=x
        self.yorg=y
        return True

    def enddrag(self,widget,event):
        print("Well done!")
        return True

    def move_image(self,*args):
        pass
        self.x=self.x+self.dx
        self.y=self.y+self.dy
        if self.x > 270 or self.x < 0: self.dx=-self.dx
        if self.y > 270 or self.y < 0: self.dy=-self.dy
        self.image_object_car.set_coords(self.x,self.y)
        self.x1=self.x1+self.dx1
        self.y1=self.y1+self.dy1
        if self.x1 > 220 or self.x1 < 0: self.dx1=-self.dx1
        if self.y1 > 270 or self.y1 < 0: self.dy1=-self.dy1
        self.image_object_car2.set_coords(self.x1,self.y1)

    def quit(self,*args):
        Gtk.main_quit()


if __name__=='__main__':
    a=TestApp()
    Gtk.main()
