#signal-generator.py 
import RPi.GPIO as IO
import time
import math

def get_sin_wave_amplitude(freq, time):
    y = math.sin(2 * math.pi * freq * time)
    return (y+1)/2
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)

def get_triangle_wave_amplitude(freq, time):
    T=1/freq
    x=time%T
    if x<=T/2:
        return (2/T)*x
    else:
        return 1-(2/T)*(x-T/2)
    
#8-bit-dac-manual.py
import RPi.GPIO as IO
import time

DAC=[16,20,21,25,26,17,27,22]
period=1
value=3.3

def d2b(n):
    return [int(element) for element in bin(n)[2:].zfill(8)]

def voltage_to_number(V):
    if not(0.0 <= V <= value):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{value:.2f} В)")
        print("устанавливаем 0.0")
        return 0
    return int(255*V/3.3)


IO.setmode(IO.BCM)
IO.setup(DAC, IO.OUT)
IO.output(DAC, 0)
try:
    while True:
        try:
            Volt=float(input("Введите напряжение в вольтах: "))
            nV=voltage_to_number(Volt)
            state=d2b(nV)
            print(f"Число на вход ЦАП {nV}, ,биты {state}")
            for i in DAC:
                IO.output(i, state[DAC.index(i)])
            time.sleep(period)
        except:
            print("Вы ввели не число")
        
finally:
    IO.output(DAC, 0)
    IO.cleanup()


#r2r_dac.py
import RPi.GPIO as IO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        IO.setmode(IO.BCM)
        IO.setup(self.gpio_bits, IO.OUT, initial = 0)
    
    def deinit(self):
        IO.output(self.gpio_bits, 0)
        IO.cleanup()
    
    def set_number(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    
    def set_voltage(self, V):
        if not(0.0 <= V <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{self.dynamic_range:.2f} В)")
            print("устанавливаем 0.0")
            V = 0
        nV=int(255*V/self.dynamic_range)
        v_ar = self.set_number(nV)
        for i in self.gpio_bits:
                IO.output(i, v_ar[self.gpio_bits.index(i)])


if __name__ == "__main__":
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Не число!\n") 

    finally:
        dac.deinit()

#pwm_dac.py
import RPi.GPIO as IO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_freq, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_freq = pwm_freq
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        IO.setmode(IO.BCM)
        IO.setup(self.gpio_pin, IO.OUT)
        self.pwm=IO.PWM(self.gpio_pin, self.pwm_freq)
        duty=0
        self.pwm.start(duty)

    def deinit(self):
        IO.output(self.gpio_pin, 0)
        IO.cleanup()

    def set_voltage(self, V):
        if not(0.0 <= V <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0-{self.dynamic_range:.2f} В)")
            print("устанавливаем 0.0")
            V = 0
        duty=int(100*V/self.dynamic_range)
        self.pwm.ChangeDutyCycle(duty)


if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Не число!\n") 

    finally:
        dac.deinit()    

