import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.pwm = None
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()

    def set_voltage(self, voltage):
        duty = int(voltage / self.dynamic_range * 100)
        duty = max(0, min(100, duty))
        
        if self.pwm:
            self.pwm.ChangeDutyCycle(duty)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage}, коэффициент заполнения: {duty}%")

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.100, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
                
    finally:
        dac.cleanup()
