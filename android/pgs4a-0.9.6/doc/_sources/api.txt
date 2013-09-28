===
API
===

android
--------

.. module:: android

The android module contains android-specific functionality. Right now, this
includes lifecycle management, key mapping, and vibrator functions.

.. function:: check_pause()

   This should be called on a regular basis to check to see if Android
   expects the game to pause. If it return true, the game should
   call :func:`android.wait_for_resume()`, after persisting its state
   as necessary.

.. function:: wait_for_resume()

   This function should be called after :func:`android.check_pause()`
   returns true. It does not return until Android has resumed from
   the pause. While in this function, Android may kill a game
   without further notice.

.. function:: map_key(keycode, keysym)

   This maps between an android keycode and a python keysym. The android
   keycodes are available as constants in the android module.

.. function:: vibrate(s)

   Causes the phone to vibrate for `s` seconds. This requires that your
   application have the VIBRATE permission.

.. function:: accelerometer_enable(enable)

   Enables (if `enable` is true) or disables the device's accelerometer.

.. function:: accelerometer_reading()

   Returns an (x, y, z) tuple of floats that gives the accelerometer
   reading, in meters per second squared. See `this page
   <http://developer.android.com/reference/android/hardware/SensorEvent.html>`_
   for a description of the coordinate system. The accelerometer must
   be enabled before this function is called. If the tuple contains
   three zero values, the accelerometer is not enabled, not available,
   defective, has not returned a reading, or the device is in
   free-fall.

.. function:: get_dpi()

   Returns the screen density in dots per inch.

.. function:: show_keyboard()

   Shows the soft keyboard.

.. function:: hide_keyboard()

   Hides the soft keyboard.

android.assets
--------------
   
.. module:: android.assets

The android.assets object lets you access assets stored inside the apk
file. These assets do not need to be unpacked to internal or external
storage, reducing initial startup time.

.. function:: list()

    Return a list containing all of the assets in the package.

.. function:: open(name)

    Returns a read-only file-like object that can access an asset.

   
android.mixer
-------------
   
.. module:: android.mixer

The android.mixer module contains a subset of the functionality in found
in the `pygame.mixer <http://www.pygame.org/docs/ref/mixer.html>`_ module. It's
intended to be imported as an alternative to pygame.mixer, using code like: ::

   try:
       import pygame.mixer as mixer
   except ImportError:
       import android.mixer as mixer

The android.mixer module is a wrapper around the Android MediaPlayer
class. This allows it to take advantage of any hardware acceleration
present, and also eliminates the need to ship codecs as part of an
application.
       
It has several differences from the pygame mixer:

* The init and pre_init methods work, but are ignored - Android chooses
  appropriate settign automatically.

* Only filenames and true file objects can be used - file-like objects
  will probably not work.
  
* Fadeout does not work - it causes a stop to occur.

* Looping is all or nothing, there's no way to choose the number of
  loops that occur. For looping to work, the
  :func:`android.mixer.periodic` function should be called on a
  regular basis.

* Volume control is ignored.

* End events are not implemented.

* The mixer.music object is a class (with static methods on it),
  rather than a module. Calling methods like :func:`mixer.music.play`
  should work.

The android.mixer module hasn't been tested much, and so bugs may be
present.

pygame
------

The following pygame modules are present. Not all functionality is
supported on Android. ::

    pygame
    pygame.base
    pygame.bufferproxy
    pygame.colordict
    pygame.color
    pygame.compat
    pygame.constants
    pygame.cursors
    pygame.display
    pygame.draw
    pygame.event
    pygame.fastevent
    pygame.font
    pygame.gfxdraw
    pygame.imageext
    pygame.image
    pygame.joystick
    pygame.key
    pygame.locals
    pygame.mask
    pygame.mouse
    pygame.overlay
    pygame.rect
    pygame.rwobject
    pygame.sprite
    pygame.surface
    pygame.surflock
    pygame.sysfont
    pygame.time
    pygame.transform
    pygame.version

Python
------

The following Python modules are present. Not all functionality is
supported on Android. ::

    _abcoll
    abc
    aliases
    array
    ast
    atexit
    base64
    bisect
    binascii
    calendar
    cmath
    codecs
    collections
    compileall
    contextlib
    copy
    copy_reg
    cStringIO
    cPickle
    datetime
    difflib
    dis
    dummy_threading
    dummy_thread
    encodings
    encodings.raw_unicode_escape
    encodings.utf_8
    encodings.zlib_codec
    errno
    fcntl
    fnmatch
    functools
    __future__
    genericpath
    getopt
    glob
    gzip
    hashlib
    heapq
    httplib
    inspect
    itertools
    keyword
    linecache
    math
    md5
    mimetools
    opcode
    optparse
    os
    operator
    parser
    pickle
    platform
    posix
    posixpath
    pprint
    py_compile
    pwd
    Queue
    random
    repr
    re
    rfc822
    select
    sets
    shlex
    shutil
    site
    socket
    sre_compile
    sre_constants
    sre_parse
    ssl
    stat
    StringIO
    string
    struct
    subprocess
    symbol
    symtable
    strop
    tarfile
    tempfile
    textwrap
    _threading_local
    threading
    time
    tokenize
    token
    traceback
    types
    urllib
    urllib2
    urlparse
    UserDict
    warnings
    weakref
    webbrowser
    zipfile
    zipimport
    zlib

