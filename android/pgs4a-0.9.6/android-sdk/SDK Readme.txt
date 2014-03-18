Welcome to the Android SDK!

The Android SDK archive initially contains only the basic SDK tools. It does
not contain an Android platform or any third-party libraries. In fact, it
doesn't even have all the tools you need to develop an application.

In order to start developing applications, you must install the Platform-tools
and at least one version of the Android platform, using the SDK Manager.

Platform-tools contains build tools that are periodically updated to support new
features in the Android platform (which is why they are separate from basic
SDK tools), including adb, dexdump, and others.

To install Platform-tools, Android platforms and other add-ons, you must
have an Internet connection, so if you plan to use the SDK while
offline, please make sure to download the necessary components while online.

To start the SDK Manager, please execute the program "android".

From the command-line you can also directly trigger an update by
executing:
  tools/android update sdk --no-ui

Tip: use --help to see the various command-line options.


For more information, please consult the Android web site at
  http://developer.android.com/sdk/

