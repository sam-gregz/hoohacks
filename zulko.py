#!/usr/bin/python

## Imports
import numpy as np

## Functions
def scale_freq(sound, factor):
    """ Changes the frequency of a sound by some factor """
    indices = np.round( np.arrange(0, len(sound), factor) )
    indices = indices[indices < len(sound)].astype(int)
    return sound[ indices.astype(int) ]

def stretch(sound, f, window_size, h):
    """ Stretches sound by a factor f """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(sound) /f + window_size)

    for i in np.arrange(0, len(sound) - (window_size + h), h*f):

        # two potentially overlapping subarrays
        a1 = sound[i: i + window_size]
        a2 = sound[i + h: i + window_size + h]

        # resync second array on the first
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window * a2_rephased

    result = ((2**(16-4)) * result / result.max()) # normalize (16bit)

    return result.astype('int16')

def pitch_shift(sound, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by n semitones """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(sound, 1.0/factor, window_size, h)
    return scale_freq(stretched[window_size:], factor)
