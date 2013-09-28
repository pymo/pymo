=================
Developer's Guide
=================

|PGS4A| is a variant of RAPT, the Ren'Py Android Packaging Tool. To build it:

1. Use git to clone the RAPT source code from:

    git://github.com/renpy/rapt.git

2. Run ``git submodule init`` inside the rapt directory to download
   our branch of python-for-android.

3. Download the Android SDK, and place it in rapt/android-sdk. Ensure that the
   Android 2.2 SDK is downloaded.

4. Download the Android NDK revison 8c, and place it in rapt/android-ndk-r8c.

5. Change into the rapt directory, and run ./build_pgs4a.sh. This should build
   |PGS4A| automatically, and place the result in dist/pgs4a.

We recommend installing ccache to speed up subsequent builds.
