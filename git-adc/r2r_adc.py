import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
            
    def numer_to_dac(self, number):
        lig = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, lig)
   
    def sequential_counting_adc(self):
        for number in range(256):
            self.numer_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return number 
        return 255
    
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number * self.dynamic_range / 255
        return voltage

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3)
        while True:
            voltage = adc.get_sc_voltage()
            print(f"напряжение: {voltage} B")
    
    finally:
        adc.deinit()