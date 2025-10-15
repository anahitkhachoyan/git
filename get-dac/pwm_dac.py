import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        

    def deinit(self):
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

    def set_voltage(self, voltage):
        number = int(voltage / self.dynamic_range * 255)
        if not (0.0 <= voltage <= self.dynamic_range):
            #print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            #print("Устанавливаем 0.0 B")
            number = 0
        duty = (number/255.0) * 100
        #print(f"Коэффициент заполнения:\t")
        #print(format(duty, ".2f"))
        self.pwm.ChangeDutyCycle(duty)
        self.pwm.start(duty)

dac = PWM_DAC(12, 10000, 3.100, True)
        

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 10000, 3.100, True)

        while True:
            try:
                dynamic_range = 3.166
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()
