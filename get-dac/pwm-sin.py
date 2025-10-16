import time
import RPi.GPIO as GPIO
import signal_generator as sg  

amplitude = 1.2
signal_frequency = 100.0
sampling_frequency = 1000.0
tim = 0.0

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, pwm_frequency)
        self.pwm.start(0)
        self.dynamic_range = dynamic_range
        
    def set_voltage(self, voltage):
        duty_cycle = (voltage / self.dynamic_range) * 100
        duty_cycle = max(0, min(100, duty_cycle))
        self.pwm.ChangeDutyCycle(duty_cycle)
        
    def deinit(self):  
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 10000, 3.166, True)  
        
        while True:
            try:
            
                voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, tim)  
                dac.set_voltage(voltage)
                sg.wait_for_sampling_period(sampling_frequency) 
                tim = tim + 1 / sampling_frequency
                
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")  
                
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
        
    finally:
        dac.deinit()
