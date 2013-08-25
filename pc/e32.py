
import pygame

try:
    import android
except ImportError:
    android = None

def ao_sleep(period):
    pygame.time.wait(int(period*1000))

def ao_yield():
    return
    # Android-specific:
##    if android:
##        if android.check_pause():
##            android.wait_for_resume()

def reset_inactivity():
    pass
