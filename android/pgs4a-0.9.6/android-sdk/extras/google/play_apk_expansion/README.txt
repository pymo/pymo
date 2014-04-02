Client library for the Google Market APK Expansion files.

Changelog
---------

Version 3
* Directory structure corrected in distribution. No code changes.

Version 2
* Patch file now gets downloaded.
* Honeycomb devices now supported with ICS-like notifications
* CRC check (from sample) now supports compressed Zip files
* Use of reflection removed to allow easy obfuscation
* Service leak fixed
* Unprintable character removed from ZipResourceFile
* Minor formatting changes
* Additional comments and edits to this file

Packages
--------

downloader_library
A library that works with the google_market_licensing library to download APK Expansion files in a background service.  This library depends on the licensing library, and must be built as a library project.
zip_file
A library that uses multiple zip files as a virtual read-only filesystem with hooks to support APK Expansion lies. This also must be built as an Android library project.
downloader_sample
A sample application that assumes that zip format files have been uploaded as the main/patch file(s) on Android Market.  It downloads these files and then validates that the CRC's for every entry in the zip match.  This application depends on the downloader_library and the zip_file library. Because of dependency issues involving multiple libraries, you may have to do a clean build after creating each project.

IMPORTANT THINGS TO KNOW
------------------------

1) Do not plan to extract the contents of an APK Expansion file.  They are intended to be used in-place.  By not compressing audio and video files and storing them in a Zip file they can be played from within an expansion file.
2) See com.google.android.vending.expansion.downloader/Constants.java to turn on verbose logging in the library.  Please turn it off when you publish
3) You must add your SALT and Public key to the SampleDownloaderService and update the xAPKS structure in SampleDownloaderActivity in order to test with the sample code
4) There is no strong need to include the validator with your Android applications.  It is included as a demonstration, and can be used if you wish.

For more information, see the documentation at http://developer.android.com/guide/market/expansion-files.html

This library requires the Android License Verification Library.

See the licensing documentation at http://developer.android.com/guide/publishing/licensing.html
