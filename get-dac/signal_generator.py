import numpy
import time
import math

def get_sin_wave_amplitude(freq, tim):
    return float(0.5 * math.sin(2 * 3.1415 * freq * tim) + 0.5)

def wait_for_sampling_period(sampling_frequency):
    time.sleep(float(1 / sampling_frequency))
