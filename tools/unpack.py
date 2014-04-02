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

def load_voice(vofilename):
    global voice, voicefile
    if voice.has_key(vofilename):
        tempfile=file(DST_PATH+vofilename+u'.jpg','wb')
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

SRC_PATH=u'./'
DST_PATH=u'./'

vo=None
voice={}
voicefile=file(SRC_PATH+u'bg.pak','rb')
load_voice_list()
for i in voice:
    load_voice(i)
    
