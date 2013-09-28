.. _changelog:

Changelog
=========

Pygame Subset for Android 0.9.6
-------------------------------

This release patches Python to work with .apk files distributed
through the Amazon App Store, which are subtly different from
standard apk files.

This release fixes support for pre-2.3 Android devices.


Pygame Subset for Android 0.9.5
-------------------------------

PGS4A now supports Expansion APKs when used in conjunction with the
Google Play store. This increases the maximum package size from
50 MB to 2 GB. (Sideloaders or users of other app stores should
continue to produce a monolithic package.)

PGS4A is now based on a slightly modified python-for-android, which in
turn was originally based on PGS4A. 

PGS4A now uses and requires Android 2.2 and OpenGL ES 2.

`PyJNIus <https://github.com/kivy/pyjnius>`_ is included, allowing
access to more Android functionality. (PyJNIus integration with
PGS4A has not been tested.)

The webbrowser module can now open URLs using the Android intents system.

Increased the range of keycodes we support to include all keycodes in
Android 13.

The installsdk command now fixes permissions of the android script before
running it. Hopefully, this will make PGS4A work better on OSX X. OS X is
still not a supported development platform.

The configure command now lets you choose to include python files in your
apk package. Doing so may be necessary when upgrading a package originally
made with PGS4A 0.9.3 or earlier.

The android.mixer module is now documented properly, and android.mixer.periodic
now works.

Pygame Subset for Android 0.9.4
-------------------------------

This release changes the development process to a packaging centric
one. Instead of copying files to the device's storage, as in previous
versions of PGS4A, this release focuses on making it far easier to
create a release-worthy package.

To enable this, the old build.py tool has been replaced with a new
android.py tool. The new tool has the following functions:

* Installing and configuring an Android development environment with the
  correct versions of various software packages and signing keys.
* Allowing the user to interactively configure various build parameters.
* Mananging the process of building and installing an android package.
* Displaying log output.

These changes were motivated by difficulties accessing the sdcard in
some devices, and a general feeling that it was too hard to go from
simple code to a market-ready package.

New to this release is support for accessing assets in a package, using the
:func:`android.assets.list` and :func:`android.assets.open` functions. The
new split package layout makes it possible to includes assets as part
of the packaging process.


Pygame Subset for Android 0.9.3
-------------------------------

Important: An application must call :func:`android.init` before it can receive
input events. This prevents a crash on input.

PGS4A now uses Python 2.7.1.

The :func:`android.get_dpi` function retrieves the display DPI.

The :func:`android.show_keyboard` and :func:`android.hide_keyboard` functions
show and hide the on-screen keyboard. For now, the application is responsible
for mapping android keys to pygame keys, and then to unicode.

The following modules have been added by default: urllib2, io, uuid,
json. The following encodings have been added: idna, base64, hex.

The sqlite and PIL libraries are available, and can be enabled with the
--with-sqlite3 and --with-PIL options.


Pygame Subset for Android 0.9.2
-------------------------------

The packaging tool now include PGS4A as part of the packages it
builds. While this makes the packages somewhat larger, doing this
prevents the end user from having to download a second package to run a
game, and allows multiple PGS4A games to run simultaneously. It also
ensures that changes to PGS4A will not break games on user devices.

The packaging tool has been rewritten, and now takes more options. It
allows permissions (allowing vibration and internet access) to be
supplied on a per-application basis. It also allows the presplash
screen to be specified on a per-application basis.

Windows support has been added to the packaging tool.

The new :func:`android.vibrate` function allows an application to
request that the device vibrate for some period of time.

The new :func:`android.accelerometer_enable` and `android.accelerometer_reading`
functions allow reading the device's accelerometer.

Pygame Subset for Android 0.9.1
-------------------------------

Initial market release.
