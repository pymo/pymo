#!/usr/bin/env python2.7

import sys
sys.path.insert(0, 'buildlib/jinja2.egg')
sys.path.insert(0, 'buildlib')

import re
import tarfile
import os
import shutil
import subprocess
import time
import zipfile

import jinja2
import configure

import plat

# If we have python 2.7, record the path to it.
if sys.version_info.major == 2 and sys.version_info.minor == 7:
    PYTHON = sys.executable
else:
    PYTHON = None

class PatternList(object):
    """
    Used to load in the blacklist and whitelist patterns.
    """
    
    def __init__(self, *args):
        self.patterns = [ ]
    
        for i in args:
            self.load(i)

    def match(self, s):
        """
        Matches the patterns against s. Returns true if they match, False
        otherwise.
        """
        
        slash_s = "/" + s
        
        for p in self.patterns:
            if p.match(s):
                return True
            if p.match(slash_s):
                return  True
            
        return False
    
    
    def load(self, fn):
        
        with open(fn, "r") as f:
            for l in f:
                l = l.strip()
                if not l:
                    continue
                
                if l.startswith("#"):
                    continue
                
                self.patterns.append(self.compile(l))
    
    def compile(self, pattern):
        """
        Compiles a pattern into a regex object.
        """
    
        regexp = ""
    
        while pattern:
            if pattern.startswith("**"):
                regexp += r'.*'
                pattern = pattern[2:]
            elif pattern[0] == "*":
                regexp += r'[^/]*'
                pattern = pattern[1:]
            elif pattern[0] == '[':
                regexp += r'['
                pattern = pattern[1:]
                
                while pattern and pattern[0] != ']':
                    regexp += pattern[0]
                    pattern = pattern[1:]
                    
                pattern = pattern[1:]
                regexp += ']'
                
            else:
                regexp += re.escape(pattern[0])
                pattern = pattern[1:]
                
        regexp += "$"
        
        return re.compile(regexp, re.I)

        

# Used by render.
environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

def render(template, dest, **kwargs):
    """
    Using jinja2, render `template` to the filename `dest`, supplying the keyword
    arguments as template parameters.
    """

    template = environment.get_template(template)
    text = template.render(**kwargs)

    f = file(dest, "wb")
    f.write(text.encode("utf-8"))
    f.close()
    
def compile_dir(dfn):
    """
    Compile *.py in directory `dfn` to *.pyo
    """

    # -OO = strip docstrings
    subprocess.call([PYTHON,'-OO','-m','compileall','-f',dfn])

def make_tar(fn, source_dirs):
    """
    Make a zip file `fn` from the contents of source_dis.
    """

    def include(fn):
        rv = True
        
        if blacklist.match(fn):
            rv = False
            
        if whitelist.match(fn):
            rv = True
            
        return rv

    # zf = zipfile.ZipFile(fn, "w")
    tf = tarfile.open(fn, "w:gz")
    
    added = set()
    
    def add(fn, relfn):
        
        adds = [ ]
        
        while relfn:
            adds.append((fn, relfn))
            fn = os.path.dirname(fn)
            relfn = os.path.dirname(relfn)
            
        adds.reverse()
        
        for fn, relfn in adds:
           
            if relfn not in added:
                added.add(relfn)
                tf.add(fn, relfn, recursive=False)
    
    
    for sd in source_dirs:

        if PYTHON and not RENPY:
            compile_dir(sd)
    
        sd = os.path.abspath(sd)    

        for dir, dirs, files in os.walk(sd): #@ReservedAssignment

            for _fn in dirs:
                fn = os.path.join(dir, _fn)
                relfn = os.path.relpath(fn, sd)
                
                if include(relfn):
                    add(fn, relfn)

            for fn in files:        
                fn = os.path.join(dir, fn)
                relfn = os.path.relpath(fn, sd)

                if include(relfn):
                    add(fn, relfn)

    tf.close()

def make_tree(src, dest):
    
    def ignore(dir, files):
        
        rv = [ ]
        
        for basename in files:
            fn = os.path.join(dir, basename)
            relfn = os.path.relpath(fn, src)
            
            ignore = False
        
            if blacklist.match(relfn):
                ignore = True
            if whitelist.match(relfn):
                ignore = False
                
            if ignore:
                rv.append(basename)

        return rv
        
    shutil.copytree(src, dest, ignore=ignore)

def join_and_check(base, sub):
    """
    If base/sub is a directory, returns the joined path. Otherwise, return None.
    """
    
    rv = os.path.join(base, sub)
    if os.path.exists(rv):
        return rv
    
    return None


def edit_file(fn, pattern, line):
    """
    Replaces lines in `fn` that begin with `pattern` with `line`. `line`
    should not end with a newline - we add it.
    """

    lines = [ ]
    
    with open(fn, "r") as f:
        for l in f:
            
            if re.match(pattern, l):
                l = line + "\n"
                
            lines.append(l)
            
    with open(fn, "w") as f:
        f.write(''.join(lines))
    
def zip_directory(zf, dirname):
    """
    Zips up the directory with `dirname`. `zf` is the file to place the
    contents of the directory into.
    """
    
    for dirname, dirs, files in os.walk(dirname):
        for fn in files:
            fn = os.path.join(dirname, fn)
            zf.write(fn)
    
            
    
def build(iface, directory, commands):

    # Are we doing a Ren'Py build?

    global RENPY
    RENPY = os.path.exists("renpy")

    if not os.path.isdir(directory):
        iface.fail("{} is not a directory.".format(directory))

    if RENPY and not os.path.isdir(os.path.join(directory, "game")):
        iface.fail("{} does not contain a Ren'Py game.".format(directory))

    
    config = configure.Configuration(directory)
    if config.package is None:
        iface.fail("Run configure before attempting to build the app.")


    global blacklist
    global whitelist
    
    blacklist = PatternList("blacklist.txt")
    whitelist = PatternList("whitelist.txt")
        
    if RENPY:
        manifest_extra = None        
        default_icon = "templates/renpy-icon.png"
        default_icon_fg = "templates/pygame-icon-foreground.png"
        default_icon_bg = "templates/pygame-icon-background.png"
        default_presplash = "templates/renpy-presplash.jpg"

        public_dir = None
        private_dir = None
        assets_dir = directory
    
    else:
        manifest_extra = ""
        default_icon = "templates/pygame-icon.png"
        default_icon_fg = "templates/pygame-icon-foreground.png"
        default_icon_bg = "templates/pygame-icon-background.png"
        default_presplash = "templates/pygame-presplash.jpg"
        
        if config.layout == "internal":
            private_dir = directory
            public_dir = None
            assets_dir = None
        elif config.layout == "external":
            private_dir = None
            public_dir = directory
            assets_dir = None
        elif config.layout == "split":
            private_dir = join_and_check(directory, "internal")
            public_dir = join_and_check(directory, "external")
            assets_dir = join_and_check(directory, "assets")
        
    versioned_name = config.name.replace(" ", "").replace("'", "") + "-" + config.version

    # Annoying fixups.
    config.name = config.name.replace("'", "\\'")
    config.icon_name = config.icon_name.replace("'", "\\'")
    
    # Figure out versions of the private and public data.
    private_version = str(time.time())

    if public_dir:
        public_version = private_version
    else:
        public_version = None
            
    # Render the various templates into control files.
    render(
        "AndroidManifest.tmpl.xml",
        "AndroidManifest.xml", 
        config = config,
        manifest_extra = manifest_extra,
        )

    render(
        "strings.xml",
        "res/values/strings.xml",
        public_version = public_version,
        private_version = private_version,
        config = config)

    try:
        os.unlink("build.xml")
    except:
        pass
        
    iface.info("Updating source code.")
    
    #edit_file("src/org/renpy/android/DownloaderActivity.java", r'import .*\.R;', 'import {}.R;'.format(config.package)) #edit!
    
    iface.info("Updating build files.")
        
    # Update the project to a recent version.
    subprocess.call([plat.android, "update", "project", "-p", '.', '-t', 'android-28', '-n', versioned_name,
        # "--library", "android-sdk/extras/google/play_licensing/library",
        #"--library", "android-sdk/extras/google/play_apk_expansion/downloader_library",        
        ])



    iface.info("Creating assets directory.")

    if os.path.isdir("assets"):
        shutil.rmtree("assets")
    
    if assets_dir is not None:
        make_tree(assets_dir, "assets")
    else:
        os.mkdir("assets")

    # Copy in the Ren'Py common assets.
    if os.path.exists("renpy/common"):

        if os.path.isdir("assets/common"):
            shutil.rmtree("assets/common")
        
        make_tree("renpy/common", "assets/common")

        # Ren'Py uses a lot of names that don't work as assets. Auto-rename
        # them.
        for dirpath, dirnames, filenames in os.walk("assets", topdown=False):
            
            for fn in filenames + dirnames:
                if fn[0] == ".":
                    continue
                
                old = os.path.join(dirpath, fn)
                new = os.path.join(dirpath, "x-" + fn)
                
                os.rename(old, new)


    if config.expansion:
        iface.info("Creating expansion file.")
        expansion_file = "main.{}.{}.obb".format(config.numeric_version, config.package)

        zf = zipfile.ZipFile(expansion_file, "w", zipfile.ZIP_STORED)
        zip_directory(zf, "assets")
        zf.close()

        # Delete and re-make the assets directory.
        shutil.rmtree("assets")
        os.mkdir("assets")
        
        # Write the file size into DownloaderActivity.
        file_size = os.path.getsize(expansion_file)
        
        edit_file("src/org/renpy/android/DownloaderActivity.java", 
            r'    private int fileVersion =', 
            '    private int fileVersion = {};'.format(config.numeric_version))

        edit_file("src/org/renpy/android/DownloaderActivity.java", 
            r'    private int fileSize =', 
            '    private int fileSize = {};'.format(file_size))
        
    else:
        expansion_file = None

    iface.info("Packaging internal data.")

    private_dirs = [ 'private' ]

    if private_dir is not None:
        private_dirs.append(private_dir)
        
    if os.path.exists("engine-private"):
        private_dirs.append("engine-private")

    make_tar("assets/private.mp3", private_dirs)
    
    if public_dir is not None:
        iface.info("Packaging external data.")
        make_tar("assets/public.mp3", [ public_dir ])

    # Copy over the icon and presplash files.
    shutil.copy(join_and_check(directory, "android-icon.png") or default_icon, "res/mipmap/ic_launcher.png")
    shutil.copy(join_and_check(directory, "android-icon-foreground.png") or default_icon_fg, "res/drawable/ic_foreground_trimmed.png")
    shutil.copy(join_and_check(directory, "android-icon-background.png") or default_icon_bg, "res/drawable/ic_background.png")
    shutil.copy(join_and_check(directory, "android-presplash.jpg") or default_presplash, "res/drawable/presplash.jpg")

    # Build.
    iface.info("I'm using Ant to build the package.")

    # Clean is required 
    try:   
        subprocess.check_call([plat.ant, "clean"] +  commands)
        iface.success("It looks like the build succeeded.")
    except:
        iface.fail("The build seems to have failed.")


    if (expansion_file is not None) and ("install" in commands):
        iface.info("Uploading expansion file.")
        
        dest = "/mnt/sdcard/{}".format(expansion_file)

        subprocess.check_call([ plat.adb, "push", expansion_file, dest ])
        
        iface.success("Uploaded the expansion file.")

    if expansion_file is not None:
        os.rename(expansion_file, "bin/" + expansion_file)

    if ("install" in commands):
        iface.info("Launching app.")
        launch_activity = "PythonActivity"
        subprocess.check_call([
            plat.adb, "shell",
            "am", "start",
            "-W",
            "-a", "android.intent.action.MAIN",
            "{}/org.renpy.android.{}".format(config.package, launch_activity),
            ])
        
