import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]

    def set_voltage(self, voltage):
        number = int(voltage / self.dynamic_range * 255)
        GPIO.output(self.gpio_bits, [int(element) for element in bin(number)[2:].zfill(8)])

dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.100, True)

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.100, True)
        while True:
            try:
                dynamic_range = 3.157
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                number = int(voltage / dynamic_range * 255)
                print(f"Число на вход ЦАП: {number}, биты: {dac.set_number(number)}\n")

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз \n")

    finally:
        dac.deinit()
