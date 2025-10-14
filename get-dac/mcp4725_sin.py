import time
import mcp4725
import signal_generator

amplitude = 2
signal_frequency = 10.0
sampling_frequency = 500.0
time_elapsed = 0.0

if __name__ == "__main__":
    dac = mcp4725.MCP4725(dynamic_range = 5.0)
    
    try:
        while True:
            voltage = amplitude * signal_generator.get_sin_wave_amplitude(signal_frequency, time_elapsed)
            dac.set_voltage(voltage)
            time.sleep(1 / sampling_frequency)
            time_elapsed += 1 / sampling_frequency
        
    finally:
        dac.deinit()