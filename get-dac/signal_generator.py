import numpy as np
import time

def get_sin_wave_amplitude(freq, time_val):
    basic_sin = np.sin(2 * np.pi * freq * time_val)
    shifted_sin = basic_sin + 1
    normal_sin = shifted_sin / 2
    return normal_sin

def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1.0 / sampling_frequency 
    time.sleep(sampling_period)
