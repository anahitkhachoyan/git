import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 16.5
sampling_frequency = 1192

try:
    dac = r2r.R2RDAC([12, 20, 21, 25, 26, 17, 27, 22])
    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        normalized_amplitude = sg.get_sin_views_amplitude(signal_frequency, current_time)
        signal_amplitude = normalized_amplitude * amplitude
        dac.output(signal_amplitude)
        sg.wait_for_sampling_period(sampling_frequency)

except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if 'dac' in locals():
        dac.cleanup()
    print("Завершение работы")