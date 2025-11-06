#mcp3021_driver.py
import smbus as i2c
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = i2c.SMBus(1)
        self.verbose = verbose
        self.dynamic_range=dynamic_range
        self.address=0x4D
    def deinit(self):
        self.bus.close()
    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные {data}, старший бит {upper_data_byte}, младший бит {lower_data_byte}, число {number}")
        return number    
    def get_voltage(self):
        return self.get_number()/1023*self.dynamic_range

if (__name__ == "__main__"):
    try:
        adc=MCP3021(5.18)
        while True:
            V=adc.get_voltage()
            print(V)
            time.sleep(1)
            
    finally:
        adc.deinit()

#mcp.py (updated)
import RPi.GPIO as IO
import time
import mcp3021_driver as mcp
import adc_plot as plt

adc = mcp.MCP3021(5.18)
time_values = []
voltage_values = []
duration = 3.0
try:
    start_time=time.time()
    now_time=time.time()
    while now_time-start_time<duration:
        now_time=time.time()
        voltage_values.append(adc.get_voltage())
        time_values.append(now_time-start_time)
    plt.plot_voltage_vs_time(time_values, voltage_values, 5.18)
    plt.plot_sampling_period_hist(time_values)
finally:
        adc.deinit()


import RPi.GPIO as GPIO
import time
import smbus

class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт; {upper_data_byte:x}, Младший байт; {lower_data_byte:x}, Число: {number}")
        return number
    
    def get_voltage(self):
        return float(self.dynamic_range * MCP3021.get_number(self) / 644)

if __name__ == "__main__":
    mcp = MCP3021(3.278, True)
    try:
        while True:
            try:
                #print(dac.sequential_counting_adc())
                voltage = mcp.get_voltage()
                print(mcp.get_number())
                print(f"Напряжение: {voltage:.3f} В\n")
                time.sleep(0.5)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз \n")

    finally:
        mcp.deinit()
