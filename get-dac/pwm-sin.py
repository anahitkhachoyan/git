import time
import pwm_dac
import signal_generator as sg

amplitude = 1.2
signal_frequency = 10.0
sampling_frequency = 1000.0
tim = 0.0

if __name__ == "__main__":
    try:
        dac = pwm_dac.PWM_DAC(12, 10, 3)
        
        while True:
            voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, tim)
            dac.set_voltage(voltage)
            time.sleep(1 / sampling_frequency)
            tim += 1 / sampling_frequency
            
    except KeyboardInterrupt:
        print("Остановлено")
        
    finally:
        dac.__del__()