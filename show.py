def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    
    def binary_counter(self, number):
        for i in range(8):
            GPIO.output(self.bits_gpio[i], (number >> (7 - i)) & 1)
    
    def sequential_counting_adc(self):
        for number in range(256):
            self.binary_counter(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 0:
                return number
        return 255
    
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number * self.dynamic_range / 255
        return voltage

try:
    adc = R2R_ADC(dynamic_range=3.3)
    while True:
        voltage = adc.get_sc_voltage()
        print(f"{voltage:.2f} V")
        time.sleep(0.5)
finally:
    dac.deinit()
