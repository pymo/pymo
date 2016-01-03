#! /bin/env python
# This file runs successfully with Python 2.7.11, pygame-1.9.1, py2exe-0.6.9, and pymedia-1.2.2
from distutils.core import setup
import py2exe, sys, os
import shutil

def copy_to_dir(filelist, dst, base_path):
    for filename in filelist:
        shutil.copy2(os.path.join(base_path,filename), dst)

#hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

sys.argv.append('py2exe')
src_dir='./'
dist_dir ='dist/'
if os.path.isdir(dist_dir): #Erase previous destination dir
    shutil.rmtree(dist_dir)
#copy_to_dir(['main.py','e32.py','key_codes.py','pymedia_mixer.py'], '.',src_dir)
setup(windows=['main.py'], options={
          "py2exe": {
              "excludes": ["OpenGL.GL", "Numeric", "copyreg", "itertools.imap", "numpy", "pkg_resources", "queue", "winreg", "pygame.SRCALPHA", "pygame.sdlmain_osx"],
              }
          }
      )
copy_to_dir(['button.png','default.ttf','globalconfig.txt','keypad1.png','button_s.png','dialog.png','icon_mask.png','keypad2.png','slider.png','checkbox.png','keypad3.png','stringres.txt','config.png'],dist_dir,src_dir)
shutil.copytree(os.path.join(src_dir,'MO1_test'),os.path.join(dist_dir,'MO1_test'))
os.rename(os.path.join(dist_dir,'main.exe'), os.path.join(dist_dir,'pymo.exe'))
if os.path.isdir('build'): #Clean up build dir
    shutil.rmtree('build')
 
