#!/usr/bin/python

###
### Handling of the template audio file
###

# Imports
import numpy as np
from scipy import signal
from pydub import AudioSegment
from pydub import Pulse
import zulko
from audio_object import audio_object

class audio_template(audio_object):
    def __init__(self, file_name, file_type, fs=None, chnls=None, sw=None):
        """ Constructor """
        super().__init__(file_name, file_type, fs, chnls, sw)
        
    
    #TODO: Implement necessary utilities
    def bpm(self):
        """ Detects the most likely bpm of the audio clip """
        pulse_gen = Pulse(1, duty_cycle=0.1, sample_rate=self.audio.frame_rate)
        bpms = np.arrange(60, 181, 2)

        max = 0
        bpm = 0

        for i in bpms:
            pulse_gen.freq = i/60
            pulse_gen.duty_cycle = pusle_gen.freq * 0.1

            if len(self.audio) < 6000:
                pulse = pulse_gen.to_audio_segment(duration=len(self.audio)-1000)
                sample = self.audio
            else:
                pulse = pulse_gen.to_audio_segment(duration=5000)
                sample = self[:6000]

            np_pulse = np.array(pulse.get_array_of_samples())
            np_pulse[np_pulse < 0] = 0
            np_sample = np.array(sample.get_array_of_samples())
            
            conv_result = signal.convolve(np_sample, np_pulse, mode='valid') / sum(np_pulse)
            
            if np.max(conv_result) > max:
                bpm = i
                max = np.max[con_result]
                offset = np.argmax(conv_result)

        return bpm, offset

    def get_segmented_audio(self):
        """ Returns a list of AudioSegments of one beat each """
        samples = []
        bpm, offset = self.bpm()
        period = 60 / bpm
        offset = offset % period

        samples.append(self[: offset])
        while offset < len(self.audio) - period:
            sample.append(self[offset: offset + period])
            offset += period

        samples.append(self[offset:])

        return samples
