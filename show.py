
import RPi.GPIO as GPIO
import time

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):  # Исправлено: pmm_frequency -> pwm_frequency
        self.gpio_pin = gpio_pin
        self.frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        
        # Создание ШИМ
        self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
        self.pwm.start(0)  # Запуск с 0% заполнения
        
        if self.verbose:
            print(f"PWM DAC инициализирован на пине {gpio_pin}, частота {pwm_frequency} Гц, диапазон {dynamic_range} В")
    
    def deinit(self): 
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        if self.verbose:
            print("PWM DAC деинициализирован")
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение должно быть в диапазоне 0.0 - {self.dynamic_range:.2f} В")
            return
          
        duty_cycle = (voltage / self.dynamic_range) * 100
        duty_cycle = max(0, min(100, duty_cycle))
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.2f} В, коэффициент заполнения: {duty_cycle:.1f}%")

# Основной блок
if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)  # Исправлено: doc -> dac
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage) 
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n") 
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    finally:
        dac.deinit()  
