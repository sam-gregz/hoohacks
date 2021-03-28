#!/usr/bin/python

###
### Parent class for sound_byte and audio_template
###

## Important import statements
import numpy as np
from scipy import signal
from pydub import AudioSegment
import zulko

class audio_object:
    def __init__(self, file_path, file_type, fr=None, chnls=None, sw=None):
        """ Constructor """
        self.fp = file_path
        self.ft = file_type

        # Import the audio data
        if file_type == "raw":
            self.audio = AudioSegment.from_file(file_path, format="raw", 
                    frame_rate=fr, channels=chnls, sample_width=sw)
        else:
            self.audio = AudioSegment.from_file(file_path, format=file_type)
    
    def __get_item__(self, key):
        """ Handle slice behaviour """
        return self.audio[key]

    def get_numpy_samples(self):
        """ Get a numpy array of the audio samples """
        return np.array(self.get_array_of_samples())

    def dominant_freq(self):
        """ Returns the power spectral density """
        np_audio = self.get_numpy_samples() 

        # Get a periodogram of the audio file and find the max freq
        f, Pxx_den = signal.periodogram(np_audio, self.audio.frame_rate)
        max_i = np.argmax(Pxx_den)

        return f[max_i]
