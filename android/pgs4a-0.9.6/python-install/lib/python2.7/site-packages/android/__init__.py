#@PydevCodeAnalysisIgnore
import android.core
import android.apk
import os

from android.core import *

expansion = os.environ.get("ANDROID_EXPANSION", None)
assets = android.apk.APK(apk=expansion)

# Web browser support.
class AndroidBrowser(object):
    
    def open(self, url, new=0, autoraise=True):
        open_url(url)
        
    def open_new(self, url):
        open_url(url) 
        
    def open_new_tab(self, url):
        open_url(url) 
        
import webbrowser
webbrowser.register("android", AndroidBrowser, None, -1)
