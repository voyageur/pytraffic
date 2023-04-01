#!/usr/bin/python

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



import os,glob,sys,string,Misc,PropertyBag


np=Misc.normalize_path

config_db=PropertyBag.PropertyBag(configfile=np(Misc.default_config_db))
config_db.load(all=True)

if os.name=='posix':
    from distutils.command.install import install as _install

import shutil
from distutils.core import setup, Extension
from distutils import log
import distutils.util, distutils.dir_util

if os.name=='nt':
    py2exe_present=1
    try:
        import py2exe
    except ImportError:
        py2exe_present=0
        print("No py2exe :-(")
else:
    py2exe_present=0




if os.name=='posix':
    class install(_install):

        def build_and_install_pytraffic_script(self):
            main_command_contents=\
r"""#!/bin/sh
exec python %s/share/%s/Main.py""" %\
                   (os.path.abspath(self.install_base),config_db["install_leaf"])
            pytraffic_build=os.path.join(self.build_base,"pytraffic")
            pytraffic_install=os.path.join(self.install_base,
                                           "bin",
                                           "pytraffic")
            if  self.root:
                pytraffic_install=distutils.util.change_root(self.root,
                                                           pytraffic_install)

            log.info("creating %s" % pytraffic_build)
            main_command_file=open(pytraffic_build,"w")
            main_command_file.write(main_command_contents)
            main_command_file.close()
            distutils.dir_util.mkpath(os.path.dirname(pytraffic_install))
            self.copy_file(pytraffic_build,pytraffic_install)
            os.chmod(pytraffic_install,0o755)

        def get_libdir(self):
            if "LIBDIR" in os.environ:
                return os.environ["LIBDIR"]
            else:
                return os.path.abspath(os.path.join(self.install_base,"lib"))

        def relocate_platform_specific_files(self,strip=0):
            install_dir=os.path.join(self.install_base,
                                     "share",
                                     config_db["install_leaf"])
            if self.root:
                install_dir=distutils.util.change_root(self.root,
                                                           install_dir)
            plat_files=glob.glob(os.path.join(install_dir,"*.so"))
            lib_dir_base=os.path.join(self.get_libdir(),
                                      config_db["install_leaf"])
            if self.root:
                lib_dir=distutils.util.change_root(self.root,
                                                           lib_dir_base)
            else:
                lib_dir=lib_dir_base

            distutils.dir_util.mkpath(lib_dir)
            for f in plat_files:
                self.move_file(f,lib_dir)
                if strip:
                    log.info("stripping %s" % f)
                    os.system("strip -s %s" % f)
# make sure pytraffic knows how to find the libraries.
            config_db_new=PropertyBag.PropertyBag(configfile=\
                                  os.path.join(install_dir,Misc.default_config_db))
            config_db_new.load(all=True)
            config_db_new['add_path']=[ os.path.abspath(lib_dir_base)]
            config_db_new.save()

        def refresh_icon_cache(self):
            if self.root:
                return
            else:
                icon_dir=os.path.join(self.install_base,
                                      "share",
                                      "icons",
                                     "hicolor")
                log.info("updating utime of %s", icon_dir)
                os.utime(icon_dir,None)


        def run(self):
            if os.path.exists(self.install_lib):
                print("The installation directory %s already exists.\n\
Please delete it first." % self.install_lib)
                sys.exit()

            _install.run(self)
            self.relocate_platform_specific_files()
            self.build_and_install_pytraffic_script()
            self.refresh_icon_cache()



cmdclass={}
if os.name=='posix':
    cmdclass={'install' : install}


options={}
options['sdist']={'formats':'gztar'}


if os.name=='nt':
    options['install']={'prefix': "c:\\"+config_db["install_leaf_windows"],
                        'install_lib' :  "c:\\"+config_db["install_leaf_windows"]}
    options['build_ext']={'compiler' : 'mingw32'}
else:
    options['install']={'prefix' : '/usr/local',
                        'install_lib' : '$base/share/'+config_db["install_leaf"],
                       'install_data' : '$base'}
    options['build_ext']={'compiler' : 'unix'}

def add_install_leaf(path):
    if os.name=='nt':
        return path
    else:
        return os.path.join("share",config_db["install_leaf"],path)

ail=add_install_leaf

if py2exe_present:
	options['py2exe']={
        "includes": "pango,atk,gobject",
     }


def main_command():
    if os.name=='posix':
        return []
    else:
        return [(".",["WinMain.pyw"])]

def windows_installer():
    if os.name=='nt':
        return [("inno",['inno/PyTraffic.iss','inno/PyTrafficFull.iss'])]
    else:
        return []

def icons():
    if os.name=='nt':
        return [('icons',['icons/carNred.ico',
                     'icons/carNred16x16.ico',
                     'icons/carNred32x32.ico'])]
    else:
        return [("share/icons/hicolor/32x32/apps",["icons/32x32/pytraffic.png"]),
                ("share/icons/hicolor/48x48/apps",["icons/48x48/pytraffic.png"]),
                ("share/icons/hicolor/64x64/apps",["icons/64x64/pytraffic.png"])]

def desktop_file():
    if os.name=='nt':
        return []
    else:
        return [(ail("."),["pytraffic.desktop"])]

def theme_files():
    result=[]
    for t in config_db["themes"]:
        files=[(ail('%s' % t), glob.glob('%s/transform' % t)),
               (ail('%s/cars' % t), glob.glob('%s/cars/*.png' % t)),
               (ail('%s/cars' % t), glob.glob('%s/cars/basepoints' % t)),
               (ail('%s/background' % t), glob.glob('%s/background/*.png' % t)),
               (ail('%s/background' % t), glob.glob('%s/background/basepoints' % t))
               ]
        if glob.glob('%s/sound/*.ogg' % t):
            files+=[(ail('%s/sound' % t), glob.glob('%s/sound/*.ogg' % t))]
        result+=files
    return result

def music_files():
    result=[]
    for t in config_db["default_playlist"]:
        t=os.path.splitext(os.path.basename(t))[0]
        files=[(ail('music'), glob.glob('music/*%s*' % t))]
        result+=files
    return result

py_modules=['Affine2D',
                  'Arena',
                  'ArtWork',
                  'BottomBar',
                  'Board',
                  'Cache',
                  'Canvas',
                  'Chooser',
                  'CondMessageBox',
                  'Game',
                  'GameState',
                  'Hint',
                  'History',
                  'ImageCache',
                  'LevelFileParser',
                  'LevelSelector',
                  'Misc',
                  'MusicChooser',
                  'MusicServer',
                  'PropertyBag',
                  'ShowHTML',
                  'SmartLabel',
                  'SoundCache',
                  'SoundData',
                  'SoundServer',
                  'ThemeEngine',
                  'Timer',
                  'Statistics',
                  'Main',
                  'sdl_mixer',
                  'music',
                  'extra_path']

ext_modules=[Extension("_hint",["src/hint/asci.c",
                                       "src/hint/debug.c",
                                       "src/hint/hint.c",
                                       "src/hint/masterfile.c",
                                       "src/hint/base.c",
                                       "src/hint/extract.c",
                                       "src/hint/gtraffic.c",
                                       "src/hint/hint_wrap.c",
                                       "src/hint/precompute.c",
                                       ]),
             Extension("_sdl_mixer",
                             ["src/sdl_mixer/sdl_mixer_wrap.c"],
                             libraries=["SDL","SDL_mixer"]
                            )]

data_files=[(ail("."),['ttraffic.levels','COPYING','config.db']),
            (ail('doc'),glob.glob('doc/*.htm')+glob.glob('doc/*.png')),
            (ail('libglade'),glob.glob('libglade/*.glade')+\
                              ['libglade/carNred64x64.png']),
            (ail('music'),['music/README.README']),
            (ail('sound_test'),['sound_test/tone.ogg']),
            ('share/applications',['pytraffic.desktop']),]\
            +theme_files()\
            +music_files()\
            +main_command()\
            +windows_installer()\
            +icons()\
            +desktop_file()


long_description="""\
PyTraffic is a Python version of the board game Rush Hour
created by Binary Arts Coporation. The goal is to remove the red
car out of the grid through the slot on the right. To do this you have to
slide the other cars out of the way.

PyTraffic comes with about 19.000 puzzles ranging from intermediate to
expert.
"""

setup_kw={'cmdclass' : cmdclass,
          'options': options,
          'name' : "pytraffic",
          'version' : config_db["version"],
          'description' : "A Python simulation of the Game Rush Hour.",
          'author' : "Michel Van den Bergh",
          'author_email' : "michel.vandenbergh@uhasselt.be",
          'url' : "http://alpha.uhasselt.be/Research/Algebra",
          'long_description' : long_description,
          'py_modules' : py_modules,
          'ext_modules' : ext_modules,
          'data_files' :data_files,
          'license' : 'GPL'
          }

if py2exe_present:
    setup_kw['windows']=[{"script" : "WinMain.pyw",
                          "icon_resources":[(1,"icons/carNred.ico")]}]

setup(**setup_kw)











