import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    sin_value = np.sin(2 * np.pi * freq * time)
    shifted_value = sin_value + 1 
    normalized_value = shifted_value / 2
    return normalized_value

def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1.0 / sampling_frequency
    time.sleep(sampling_period)
