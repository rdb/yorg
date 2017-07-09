yorg
=========

**Yorg** is a free open source racing game developed by Ya2 using Panda3D for Windows, OSX and Linux. More info on [its page](http://www.ya2.it/yorg).

It requires Python 2.x. You should clone it recursively since it uses [yyagl submodule](https://github.com/cflavio/yyagl). In order to run it you should create assets. This requires the following dependencies:

* [Panda3D](https://github.com/panda3d/panda3d)
* SCons
* ImageMagick
* gettext

To build the assets, run this command:

    scons images=1 lang=1 tracks=1

If you want to use deploy-ng you must specify the switch ng, as instance:

    scons ng=1 linux_64=1

In order to create a build you should specify the target OS (windows, osx, linux_32, linux_64) e.g.:

    scons linux_64=1

NB Only building from Linux is supported.

Prerequisites for building: Panda3D, SConstruct, ImageMagick.

[![Bountysource Raised](https://www.bountysource.com/badge/team?team_id=213581&style=raised)](https://salt.bountysource.com/teams/ya2)
