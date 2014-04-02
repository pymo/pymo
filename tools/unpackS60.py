# Copyright (c) 2005 Nokia Corporation
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
# ROTATE_90=3,ROTATE_180=4,ROTATE_270=5,

import string
import os
import struct
import e32
from audio import *

def load_voice(vofilename):
    global voice, voicefile
    if voice.has_key(vofilename):
        tempfile=file(THIS_PATH+u'temp.wav','wb')
        voicefile.seek(voice[vofilename][0])
        tempfile.seek(0)
        tempfile.write(voicefile.read(voice[vofilename][1]))
        tempfile.close()

def remove_null_end(srcstring):
    pos=srcstring.find('\0')
    if pos==-1:
        return srcstring
    else:
        return srcstring[:pos]

def load_voice_list():
    global voice,voicefile
    #read the voice file list
    voicefilecount=struct.unpack('i',voicefile.read(4))[0]
    voice={}
    i=0
    while i< voicefilecount:
        filename=remove_null_end(voicefile.read(32))
        fileoffset=struct.unpack('i',voicefile.read(4))[0]
        filelength=struct.unpack('i',voicefile.read(4))[0]
        voice[filename]=(fileoffset,filelength)
        i+=1

if e32.in_emulator():
    THIS_PATH=u'c:\\data\\python\\'
else:
    THIS_PATH=u'e:\\python\\'

vo=None
voice={}
voicefile=file(THIS_PATH+u'voice.pak','rb')
load_voice_list()
for i in voice:
    if vo:
        vo.stop()
        vo.close()
    print i
    load_voice(i)
    lowername=i.lower()
    vo=Sound.open(THIS_PATH+u'temp.wav')
    vo.set_volume(1)
    if not e32.in_emulator():
        vo.play()
    e32.ao_sleep(5)
    
