import time
import RPi.GPIO as GPIO
import signal_generator as sg  # Исправлено: signal_Generator

# Параметры сигнала
amplitude = 1.2
signal_frequency = 10.0
sampling_frequency = 1000.0
tim = 0.0

# Предполагаем, что у нас есть класс PWM_DAC (нужно импортировать или определить)
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
        
    def deinit(self):  # Исправлено: denrit -> deinit
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)

if __name__ == "__main__":
    try:
        # Инициализация ЦАП
        dac = PWM_DAC(12, 500, 3.3, True)  # Добавлено: создание объекта dac
        
        while True:
            try:
                # Генерация синусоидального сигнала
                voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, tim)  # Исправлено: убраны лишние скобки
                dac.set_voltage(voltage)  # Исправлено: set_voltage/voltage -> set_voltage(voltage)
                
                # Ожидание следующего периода дискретизации
                sg.wait_for_sampling_period(sampling_frequency)  # Исправлено: Sg -> sg
                tim = tim + 1 / sampling_frequency
                
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")  # Исправлен текст
                
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
        
    finally:
        dac.deinit()  # Исправлено: @BSc.denrit() -> dac.deinit()
