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
        archive = "tools_r25.2.5-windows.zip"
        unpacked = "tools"
    elif plat.macintosh:
        archive = "tools_r25.2.5-macosx.zip"        
        unpacked = "tools"
    elif plat.linux:
        archive = "tools_r25.2.5-linux.zip"
        unpacked = "tools"
    
    url = "http://dl-ssl.google.com/android/repository/" + archive
    
    interface.info("I'm downloading the Android SDK. This might take a while.")
    
    urllib.urlretrieve(url, archive)
    
    interface.info("I'm extracting the Android SDK.")
    
    os.makedirs("android-sdk")

    if archive.endswith(".tgz"):
        tf = tarfile.open(archive, "r:*")
        tf.extractall()
        tf.close()
    else:
        zf = zipfile.ZipFile(archive)
        zf.extractall("android-sdk")
        zf.close()
        
    
    interface.success("I've finished unpacking the Android SDK.")
    
def unpack_ant(interface):
    if os.path.exists("apache-ant"):
        interface.success("Apache ANT has already been unpacked.")
        return
    
    archive = "apache-ant-1.9.13-bin.tar.gz"
    unpacked = "apache-ant-1.9.13"
    url = "http://apache.40b.nl//ant/binaries/" + archive

    interface.info("I'm downloading Apache Ant. This might take a while.")
    
    urllib.urlretrieve(url, archive)
    
    interface.info("I'm extracting Apache Ant.")

    tf = tarfile.open(archive, "r:*")
    tf.extractall()
    tf.close()
    
    os.rename(unpacked, "apache-ant")

    interface.success("I've finished unpacking Apache Ant.")
    
def get_packages(interface):
    interface.info("Going to install 4 packages via the android SDK Manager (SDK Build-tools, Platform-tools, SDK Platform android-28, android-support).")
    subprocess.call([plat.android, "update", "sdk", "--no-ui", "--all", "--filter", "android-28"])
    subprocess.call([plat.android, "update", "sdk", "--no-ui", "--all", "--filter", "build-tools-28.0.2"])
    subprocess.call([plat.android, "update", "sdk", "--no-ui", "--all", "--filter", "platform-tools"])
    subprocess.call([plat.android, "update", "sdk", "--no-ui", "--all", "--filter", "extra-android-m2repository"])
    try:
        jar = "android-sdk/extras/android/m2repository/com/android/support/support-v4/19.1.0/support-v4-19.1.0.jar"
        shutil.copyfile(jar, "libs/android-support-v4.jar")
    except: interface.info("Could not copy the android-support-v4.jar into the libs folder.")
    
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
    
    run(plat.keytool, "-genkey", "-keystore", "android.keystore", "-alias", "android", "-keyalg", "RSA", "-keysize", "2048", "-keypass", "android", "-storepass", "android", "-dname", dname, "-validity", "36500")
    
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

