# Copyright (c) 2007 Nokia Corporation
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
#
# viewfinder.py - shows viewfinder on the screen
#

import appuifw 
import camera
import e32

class ViewFinder:
    def __init__(self):
        self.script_lock = e32.Ao_lock()
        self.finder_on=0

    def run(self):
        old_title = appuifw.app.title
        self.refresh()
        self.script_lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None

    def refresh(self):
        appuifw.app.title = u"Viewfinder"
        appuifw.app.menu = [(u"Start", self.start_finder),
                            (u"Stop", self.stop_finder),
                            (u"Exit", self.do_exit)]
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body=self.canvas=appuifw.Canvas()
        self.start_finder()
        self.finder_on=1

    def stop_finder(self):
        camera.stop_finder()
        self.finder_on=0
        appuifw.note(u"Viewfinder stopped")

    def start_finder(self):
        if (not self.finder_on):
            camera.start_finder(self.show_img)
            self.finder_on=1
        else:
            appuifw.note(u"Viewfinder already on")

    def show_img(self, image_frame):
        self.canvas.blit(image_frame)

    def do_exit(self):
        self.exit_key_handler()

    def exit_key_handler(self):
        camera.stop_finder()
        self.canvas=None
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()

if __name__ == '__main__':
    ViewFinder().run()
