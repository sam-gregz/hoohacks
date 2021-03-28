#!/usr/bin/python

###
### Sample file handling
###

## Important import statements
import numpy as np
from scipy import signal
from pydub import AudioSegment
import zulko
from audio_object import audio_object

class sound_byte(audio_object):
    def __init__(self, file_path, file_type, fr=None, chnls=None, sw=None):
        """ Constructor """
        super.__init__(file_name, file_type, fr, chnls, sw)

    def scale_freq(self, factor):
        return zulko.scale_freq(self.get_numpy_samples(), factor)

    def sretch(self, f, window_size, h):
        return zulko.stretch(self.get_numpy_samples(), f, window_size, h)

    def pitch_shift(self, n, window_size=2**13, h=2**11):
        return zulko.pitch_shift(self.get_numpy_samples(), n, window_size, h)
    
