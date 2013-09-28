====================
More about Packaging
====================

Icon and Presplash
------------------

|PGS4A| uses an icon to represent your project in the launcher. It
also displays a presplash image as your project is loading, before
Pygame initializes the screen. Both images can be customized by
placing files in the game directory. The relevant files are:

``android-icon.png``
    The icon. This may include transparency.

``android-presplash.jpg``
    The presplash image. The border around this image is filled with
    the color of the top-left pixel.

Split Layout Packages
---------------------

|PGS4A| supports packages that use a split layout, in which files are
divided between the internal storage, external storage, and the assets
directory.

When the split layout is chosen, a project should consist one, two, or
three of the following directories:

``internal``
    Files to be unpacked to the internal storage.

``external``
    Files to be unpacked to the external storage.

``assets``
    Files that are stored as assets that can be accessed using
    :func:`android.assets.open`.

One of ``internal`` or ``external`` must exist to contain the main.py
file. Without additonal code, |PGS4A| can't import modules from the
``assets`` directory.

