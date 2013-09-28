.. _writing:

==============
Writing a Game
==============

A Pygame Subset for Android game consists of a game written using the subset of
pygame we support, with calls to android-specific APIs as necessary. Execution
starts by importing the main module, and calling its main function. This means
that the start point of your game is in the main.py file.

Here's a main.py file for a trivial game::

    import pygame

    # Import the android module. If we can't import it, set it to None - this
    # lets us test it, and check to see if we want android-specific behavior.
    try:
        import android
    except ImportError:
        android = None

    # Event constant.
    TIMEREVENT = pygame.USEREVENT

    # The FPS the game runs at.
    FPS = 30

    # Color constants.
    RED = (255, 0, 0, 255)
    GREEN = (0, 255, 0, 255)

    def main():
        pygame.init()

        # Set the screen size.
        screen = pygame.display.set_mode((480, 800))

        # Map the back button to the escape key.
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        # Use a timer to control FPS.
        pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

        # The color of the screen.
        color = RED

        while True:

            ev = pygame.event.wait()

            # Android-specific: 
            if android:
                if android.check_pause():
                    android.wait_for_resume()

            # Draw the screen based on the timer.
            if ev.type == TIMEREVENT:
                screen.fill(color)
                pygame.display.flip()

            # When the touchscreen is pressed, change the color to green. 
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                color = GREEN

            # When it's released, change the color to RED.
            elif ev.type == pygame.MOUSEBUTTONUP:
                color = RED

            # When the user hits back, ESCAPE is sent. Handle it and end
            # the game.
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                break

    # This isn't run on Android.
    if __name__ == "__main__":
        main()

This simple program barely qualifies as a game - all it does is change the
color of the screen when the user is touching it. It's probably only
entertaining to the one-year-old crowd, for whom making anything at all
occur is a source of fun.

This code can be run both on a PC with pygame installed, and on Pygame
Subset for Android.

Main
----

Note that all code is in the main function, with little code at the
module level. This ensures that the code will run when it is imported
without the import lock being held.

While we include the standard::

    if __name__ == "__main__":
        main()

clause, it doesn't do anything on Android. It's just there to ensure this
code works on the PC platform.


Importing Android
-----------------

::

    try:
        import android
    except ImportError:
        android = None

This code imports the android module, which contains android-specific
functionality. By catching the import error and later testing
``android``, we can be sure it runs on the PC as well.


Lifecycle Management
--------------------

::

            if android:
                if android.check_pause():
                    android.wait_for_resume()

At any time, Android may ask that your game pause itself. This
may occur when the user hits the pause button, when the device
goes to sleep, or when the user switches to another application.

You can check for a pause request using the :func:`android.check_pause`
function. If this returns true, you should prepare your game to sleep.
When ready to sleep, call the :func:`android.wait_for_resume` method.

When in sleep mode, two things can happen. The first is that wait_for_resume
returns. In that case, the game should resume itself. The second is that
Android can choose to terminate the game, in which case a return to the
game will cause the game to begin executing from the start.

Since the game can be terminated wihout further notice while in sleep
mode, it may make sense to save the game before calling
wait_for_resume. The save can be deleted if wait_for_resume
returns, or loaded when the game next starts.

When in sleep mode, the game is expected to take up no CPU time.
SDL timers are suspended automatically, but it may be necessary to
suspend other Python threads.


Key Mapping
-----------

::

        if android:
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

The :func:`android.map_key` function is used to map an Android keycode
to a Pygame keysym. The Android keycodes are available as constants
in the android module.

A list of Android keycodes and their meanings can be found
`here <http://developer.android.com/reference/android/view/KeyEvent.html>`_.


Sound and Music
---------------

Although not used here, a big difference between the Pygame Subset and
Pygame is the handling of sound and music. In Pygame Subset, sound
playback is handled by the :mod:`android.mixer` module.


Hardware Support
----------------

Device hardware such as the vibrator and accelerometer are supoorted
through the :mod:`android` module.

