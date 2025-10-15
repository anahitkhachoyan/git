import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 1.0
signal_frequency = 100.0
sampling_frequency = 10000.0
tim = 0.0

if __name__ == "__main__":
    try:
        while True:
            try:
                voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, tim)
                r2r.dac.set_voltage(voltage)
                sg.wait_for_sampling_period(sampling_frequency)
                tim = tim + 1 / sampling_frequency

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз \n")

    finally:
        r2r.dac.deinit()
