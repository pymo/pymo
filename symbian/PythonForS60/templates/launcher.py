# Copyright (c) 2008 - 2009 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import series60_console
import appuifw

sys.path.insert(0, os.path.join(os.getcwd(), 'lib.zip'))
default_namespace = {'__builtins__': __builtins__, '__name__': '__main__'}

my_console = series60_console.Console()
saved_exit_key_handler = appuifw.app.exit_key_handler


def restore_defaults():
    appuifw.app.body = my_console.text
    sys.stderr = sys.stdout = my_console
    appuifw.app.screen = 'large'
    appuifw.app.menu = []

restore_defaults()


def display_traceback():
    import traceback
    traceback.print_exc()


try:
    try:
        execfile('default.py', default_namespace)
    finally:
        default_namespace.clear()
        appuifw.app.exit_key_handler = saved_exit_key_handler
        restore_defaults()
except SystemExit, err:
    # Check whether it is a successful or an abnormal termination. '' is also
    # checked as not passing any arguments in the sys.exit() call evaluates to
    # `None`.
    if str(err) not in [str(0), '']:
        display_traceback()
    else:
        appuifw.app.set_exit()
except:
    display_traceback()
else:
    # If nothing was written onto the text widget, exit immediately
    if not appuifw.app.body.len():
        appuifw.app.set_exit()
