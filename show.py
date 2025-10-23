def set_number(self, number):
        lig = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.gpio_bits, lig)
