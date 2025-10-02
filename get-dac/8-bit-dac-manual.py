import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
leds = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(leds, GPIO.OUT)

dynamic_range = 3.166

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0

    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    return[int(bit) for bit in bin(number)[2:].zfill(8)]

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            bits = number_to_dac(number)
            print(f"Число на вход ЦАП: {number}, биты: {bits}\n")
            GPIO.output(leds, bits) 

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()