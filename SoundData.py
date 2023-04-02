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

import os

sound_data=[]

# We assume that on Windows everything "just works" :-)

if os.name=='nt':
    sound_data=None
else:
    sound_data=[
    {
    'id' : 'Default',
    'env' : None,
    'menu_label' : 'Default',
    'action' : None,
    'menu_item' : None
    },
    {
    'id' : 'OSS',
    'env' : 'oss',
    'menu_label' : 'OSS',
    'action' : None,
    'menu_item' : None
    },
    {
    'id' : 'Alsa',
    'env' : 'alsa',
    'menu_label' : 'Alsa',
    'action' : None,
    'menu_item' : None
    },
    {
    'id' : 'Artsd',
    'env' : 'artsc',
    'menu_label' : 'Artsd',
    'action' : None,
    'menu_item' : None
    },
    {
    'id' : 'Esd',
    'env' : 'esd',
    'menu_label' : 'Esd',
    'action' : None,
    'menu_item' : None
    }
    ]


def do_os_stuff(output):
    if output and output!='Default' and os.name=='posix':
        for data in sound_data:
            if data['id']==output:
                os.environ['SDL_AUDIODRIVER']=data['env']
