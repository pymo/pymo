import json
import os

class Configuration(object):
    
    def __init__(self, directory):
    
        self.package = None
        self.name = None
        self.icon_name = None    
        self.version = None
        self.numeric_version = None
        self.orientation = None
        self.permissions = []        
        self.include_pil = False
        self.include_sqlite = False
        self.layout = "internal"
        self.source = False
        self.expansion = False
	self.targetsdk = 26
        
        try:
            with file(os.path.join(directory, ".android.json"), "r") as f:
                d = json.load(f)
            
            self.__dict__.update(d)            
        except:
            pass
        
    def save(self, directory):

        with file(os.path.join(directory, ".android.json"), "w") as f:
            json.dump(self.__dict__, f)

def set_version(config, value):
    """
    Sets the version, and tries to set the numeric versions based on the 
    version number.
    """
    
    config.version = value
    
    try:
        v = 0
        
        for i in config.version.split('.'):
            v *= 100
            v += int(i)

        config.numeric_version = str(v)
    except:
        pass
    
def configure(interface, directory):

    renpy = os.path.exists("renpy")
        
    config = Configuration(directory)
    config.name = interface.input("""What is the full name of your application? This name will appear in the list of installed applications.""", config.name)
    
    if config.icon_name is None:
        config.icon_name = config.name
    
    config.icon_name = interface.input("What is the short name of your application? This name will be used in the launcher, and for application shortcuts.", config.icon_name)

    config.package = interface.input("""\
What is the name of the package?

This is usually of the form com.domain.program or com.domain.email.program. It
must only contain ASCII letters and dots.""", config.package)

    version = interface.input("""\
What is the application's version?

This should be the human-readable version that you would present to a person.""", config.version)

    set_version(config, version)
    
    config.numeric_version = interface.input("""What is the version code? 

This should be an integer number, and the value should increase between versions.""", config.numeric_version)    

    config.targetsdk = interface.input("""What is the targetsdk version of the app? 

This should be an integer number, for example API 28 for targeting android Pie (9.0).""", config.targetsdk)

    config.orientation = interface.choice("How would you like your application to be displayed?", [
            ("sensorLandscape", "In landscape mode."),
            ("sensorPortrait", "In portrait mode."),
        ], config.orientation)

    config.expansion = interface.choice("Would you like to create an expansion APK?", [
        (False, "No. Size limit of 50 MB on Google Play, but can be distributed through other store and sideloaded."),
        (True, "Yes. 2 GB size limit, but won't work outside of Google Play.")
        ], config.expansion)

    if not renpy:

        config.layout = interface.choice("How is your application laid out?", [
            ("internal", "A single directory, that will be placed on device internal storage."),
            ("external", "A single directory, that will be placed on device external storage."),
            ("split", "Multiple directories that correspond to internal, external, and asset storage."),
            ], config.layout)

        config.source = interface.yesno("Do you want to include the Python source code of your application in the archive? If you include it once, you'll need to include it always.", config.source)

        permissions = " ".join(config.permissions)
        permissions = interface.input("""\
What permissions should your application have? Possible permissions include:

INTERNET (network access), VIBRATE (vibration control).
    
Please enter a space-separated list of permissions.""", permissions)
        config.permissions = permissions.split()
    
        config.include_sqlite = interface.yesno("Do you want to include SQLite3 with your application?", config.include_sqlite)
        config.include_pil = interface.yesno("Do you want to include the Python Imaging Library (PIL) with your application?", config.include_pil)
        
    if renpy:
        
        if not config.expansion:
            internet = "INTERNET" in config.permissions
            internet = interface.yesno("Do you want to allow the app to access the Internet?", internet)
        else:
            internet = False # included in template.
            
        permissions = [ i for i in config.permissions if i not in [ "INTERNET" ] ]
        
        if internet:
            permissions.append("INTERNET")
            
        config.permissions = permissions
        
        
    config.save(directory)
    
def set_config(iface, directory, var, value):

    config = Configuration(directory)

    if var == "version":
        set_version(config, value)
    elif var == "permissions":
        config.permissions = value.split()
    elif hasattr(config, var):
        setattr(config, var, value)
    else:
        iface.fail("Unknown configuration variable: {}".format(var))
        
    config.save(directory)
        
        
    
        
    


