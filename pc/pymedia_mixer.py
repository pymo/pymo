#! /bin/env python
import pymedia
import threading

class Sound(object):
    def __init__(self, filename):
        self.name = filename
        self.snd=None
        self.playing=False

    def load(self, filename):
        self.stop()
        self.name = filename

    def play(self, loops=0):
        self.thread=threading.Thread(target=self._play, args=(loops,))
        self.thread.daemon=True
        self.thread.start()
        return self

    def _play(self, loops):
        dm= pymedia.muxer.Demuxer( str.split( self.name, '.' )[ -1 ].lower() )
        snds= pymedia.audio.sound.getODevices()
        card =0
        f= open( self.name, 'rb' )
        dec= None
        s= f.read( )
        if len( s ) <= 0:
            return
        self.playing=True
        i=loops
        while (loops<0 or i>=0) and self.playing:
            frames= dm.parse( s )
            if frames:
              for fr in frames:
                if not self.playing:
                    break
                if dec== None:
                  dec= pymedia.audio.acodec.Decoder( dm.streams[ fr[ 0 ] ] )
                r= dec.decode( fr[ 1 ] )
                if r and r.data:
                  if self.snd == None:
                    self.snd = pymedia.audio.sound.Output( int( r.sample_rate ), r.channels, pymedia.audio.sound.AFMT_S16_LE, card )
                  data= r.data
                  self.snd.play( data )
            i-=1

    def stop(self):
        self.playing = False
        if self.snd and self.snd.isPlaying():
            self.snd.stop()
            self.snd=None

    def get_busy(self):
        if self.snd and self.snd.isPlaying():
            return True
        else:
            return False

music = Sound(None)

# Test for the basic parser functionality
if __name__== '__main__':
    import time
    snd=Sound("E:\\001.mp3")
    snd.play(-1)
    time.sleep( 40 )
    snd.stop()
