#!/usr/bin/env python

import subprocess
import traceback
import os
import zipfile
import tarfile
import urllib
import shutil

import plat


##############################################################################
def run(*args):
    try:
        subprocess.check_call(args)
        return True
    except:
        traceback.print_exc()
        return False

##############################################################################
def check_java(interface):
    """
    Checks for the presence of a minimally useful java on the user's system.
    """
    
    interface.info("""\
I'm compiling a short test program, to see if you have a working JDK on your
system.
""")
    
    SOURCE = """\
class test {
    public static void main(String args[]) {
    }
}
"""
   
    f = file("test.java", "w")
    f.write(SOURCE)
    f.close()
    
    if not run(plat.javac, "test.java"):
        interface.info("""\
I was unable to use javac to compile a test file. If you haven't installed
the JDK yet, please download it from:

http://www.oracle.com/technetwork/java/javase/downloads/index.html

The JDK is different from the JRE, so it's possible you have Java
without having the JDK.""")

        interface.fail("""\
Without a working JDK, I can't continue.
""")
        
    interface.success("The JDK is present and working. Good!")
    
    os.unlink("test.java")
    os.unlink("test.class")
        
def unpack_sdk(interface):
     
    if os.path.exists("android-sdk"):
        interface.success("The Android SDK has already been unpacked.")
        return
    
    if "PGS4A_NO_TERMS" not in os.environ:
        interface.terms("http://developer.android.com/sdk/terms.html", "Do you accept the Android SDK Terms and Conditions?")
        
    if plat.windows:        
        archive = "android-sdk_r20-windows.zip"
        unpacked = "android-sdk-windows"
    elif plat.macintosh:
        archive = "android-sdk_r20-macosx.zip"        
        unpacked = "android-sdk-macosx"
    elif plat.linux:
        archive = "android-sdk_r20-linux.tgz"
        unpacked = "android-sdk-linux"
    
    url = "http://dl.google.com/android/" + archive
    
    interface.info("I'm downloading the Android SDK. This might take a while.")
    
    urllib.urlretrieve(url, archive)
    
    interface.info("I'm extracting the Android SDK.")
    
    if archive.endswith(".tgz"):
        tf = tarfile.open(archive, "r:*")
        tf.extractall()
        tf.close()
    else:
        zf = zipfile.ZipFile(archive)
        zf.extractall()
        zf.close()
        
    os.rename(unpacked, "android-sdk")
    
    interface.success("I've finished unpacking the Android SDK.")
    
def unpack_ant(interface):
    if os.path.exists("apache-ant"):
        interface.success("Apache ANT has already been unpacked.")
        return
    
    archive = "apache-ant-1.8.4-bin.tar.gz"
    unpacked = "apache-ant-1.8.4"
    url = "http://archive.apache.org/dist/ant/binaries/" + archive

    interface.info("I'm downloading Apache Ant. This might take a while.")
    
    urllib.urlretrieve(url, archive)
    
    interface.info("I'm extracting Apache Ant.")

    tf = tarfile.open(archive, "r:*")
    tf.extractall()
    tf.close()
    
    os.rename(unpacked, "apache-ant")

    interface.success("I've finished unpacking Apache Ant.")
    
def get_packages(interface):
    
    packages = [ ]

    if not os.path.exists("android-sdk/platforms/android-8"):
        packages.append("android-8")

    if not os.path.exists("android-sdk/platforms/android-15"):
        packages.append("android-15")
        
    if not os.path.exists("android-sdk/platform-tools"):
        packages.append("platform-tools")
    
    if not os.path.exists("android-sdk/extras/google/play_licensing"):
        packages.append("extra-google-play_licensing")

    if not os.path.exists("android-sdk/extras/google/play_apk_expansion"):
        packages.append("extra-google-play_apk_expansion")
    
    # TODO: Install the play_ libraries, and maybe update them.
    
    if not packages:
        interface.success("The required Android packages are already installed.")
        return
    
    interface.info("I'm about to download and install the required Android packages. This might take a while.")
    
    if not run(plat.android, "update", "sdk", "-u", "-a", "-t", ",".join(packages)):
        interface.fail("I was unable to install the required Android packages.")

    interface.info("I'm updating the library packages.")
    
    if "extra-google-play_apk_expansion" in packages:
        with open("android-sdk/extras/google/play_apk_expansion/downloader_library/project.properties", "r") as f:
            data = f.read()
            
        data = data.replace("../market_licensing", "../../play_licensing/library")
        
        with open("android-sdk/extras/google/play_apk_expansion/downloader_library/project.properties", "w") as f:
            f.write(data)
            
    run(plat.android, "update", "project", "-p", "android-sdk/extras/google/play_licensing/library")
    run(plat.android, "update", "project", "-p", "android-sdk/extras/google/play_apk_expansion/downloader_library")
        
    if os.path.exists("android-sdk/extras/google/play_apk_expansion/downloader_library/res/values-v9"):
        shutil.rmtree("android-sdk/extras/google/play_apk_expansion/downloader_library/res/values-v9")
        
    interface.success("I've finished installing the required Android packages.")
    
def generate_keys(interface):
    
    if os.path.exists("android.keystore"):
        interface.info("You've already created an Android keystore, so I won't create a new one for you.")
        return
        
    if not interface.yesno("""\
I can create an application signing key for you. Signing an application with
this key allows it to be placed in the Android Market and other app stores.

Do you want to create a key?"""):
        return

    if not interface.yesno("""\
I will create the key in the android.keystore file.

You need to back this file up. If you lose it, you will not be able to upgrade
your application. 

You also need to keep the key safe. If evil people get this file, they could
make fake versions of your application, and potentially steal your users'
data.

Will you make a backup of android.keystore, and keep it in a safe place?"""):
        return

    org = interface.input("Please enter your name or the name of your organization.")
    
    dname = "CN=" + org
    
    run(plat.keytool, "-genkey", "-keystore", "android.keystore", "-alias", "android", "-keyalg", "RSA", "-keysize", "2048", "-keypass", "android", "-storepass", "android", "-dname", dname, "-validity", "20000")
    
    f = file("local.properties", "a")
    print >>f, "key.alias=android"
    print >>f, "key.store.password=android"
    print >>f, "key.alias.password=android"
    print >>f, "key.store=android.keystore"
    f.close()
    
    interface.success("""I've finished creating android.keystore. Please back it up, and keep it in a safe place.""")
    
def install_sdk(interface):
    check_java(interface)
    unpack_ant(interface)
    unpack_sdk(interface)

    if plat.macintosh or plat.linux:
        os.chmod("android-sdk/tools/android", 0755)
    
    get_packages(interface)
    generate_keys(interface)
    
    interface.success("It looks like you're ready to start packaging games.")

