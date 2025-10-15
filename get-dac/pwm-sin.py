import numpy
import time
import pwm_dac
import signal_generator as sg

amplitude = 1.2
signal_frequency = 10.0
sampling_frequency = 1000.0
tim = 0.0

if __name__ == "__main__":
    try:
        while True:
            try:
                voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, tim)
                pwm_dac.dac.set_voltage(voltage)
                sg.wait_for_sampling_period(sampling_frequency)
                tim = tim + 1 / sampling_frequency

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз \n")

    finally:
        pwm_dac.dac.deinit()
