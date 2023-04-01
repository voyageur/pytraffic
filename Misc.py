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

import os,sys,string,shutil

#Taken from the pysol source.

def gethomedir():
    default_home = os.curdir
    if os.name == "nt": default_home = "c:\\"
    home = os.environ.get("HOME", "").strip()
    if not home or not os.path.isdir(home):
        if os.name == "nt":
            home = os.environ.get("HOMEDRIVE", "")\
                   + os.environ.get("HOMEPATH","")
    if not home or not os.path.isdir(home):
        home = default_home
    return os.path.abspath(home)

exec_dir=os.path.split(sys.argv[0])[0]
sys.path.insert(0,exec_dir)

def normalize_path(path):
    return os.path.join(os.getcwd(),path)

default_configfile=os.path.join(gethomedir(),r".pytraffic")
backup_configfile=os.path.join(gethomedir(),r".pytraffic_save")
default_config_db="config.db"

def save_configfile():
    try:
        shutil.copyfile(default_configfile,backup_configfile)
    except:
        print("Renaming configfile failed.")
    
cellheight=50
cellwidth=50
borderwidth=10
gridwidth=2
extraroomonright=cellwidth
bordercolor=0

boardheight=6*cellheight
boardwidth=6*cellwidth
jamheight=boardheight+2*borderwidth
jamwidth=boardwidth+2*borderwidth
totaljamwidth=jamwidth+extraroomonright
jamoriginx=borderwidth
jamoriginy=borderwidth

# returns the nearest gridpoint  for a given point x,y in canvas coordinates
# the returned point maybe outside board

def nearestgridpoint (x, y):
    roundy=round((y-jamoriginy+0.0)/cellheight)*cellheight+jamoriginy
    roundx=round ((x-jamoriginx+0.0)/cellwidth)*cellwidth+jamoriginx
    return (roundx,roundy)

#converts x,y coordinates on grid to row col pairs

def torowcol (x, y,rounding=1):
    rowfrac=(y-jamoriginy+0.0)/cellheight
    columnfrac=(x-jamoriginx+0.0)/cellwidth
    if rounding:
        row=round(rowfrac)
        column=round(columnfrac)
    else:
        row=int(rowfrac)
        column=int(columnfrac)
    
    return (row,column)

#converts row, col pair to grid coordinates

def togridpoint (row,col):
    x=col*cellwidth +jamoriginx
    y=row*cellwidth +jamoriginx
    return (x,y)

# works on cygwin 2.3 and 2.4

def isCygwin():
	return string.find(string.lower(sys.version),'cyg')!=-1	


def walk(file_list,recursion_depth=None):
    for f in file_list:
#	print f
        if not os.path.exists(f):
            continue
        elif os.path.isfile(f):
            yield f
        elif os.path.isdir(f) and not os.path.islink(f) and \
            (recursion_depth==None or recursion_depth>0):
            l=None
            try:
                l=os.listdir(f)
            except:
                pass
            if l:
                l=[os.path.join(f,x) for x in l]
                if recursion_depth:
                    recursion_depth=recursion_depth-1
                for ff in walk(l,recursion_depth):
                    yield ff
            else:
                yield f
        else:
            yield f


#g=walk(['.'])
#
#while(1):
#    print g.next()



