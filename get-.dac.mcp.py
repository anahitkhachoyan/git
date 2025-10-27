#mcp_driver4725.py
import smbus

class MCP4725:
    def __init__(self, dynamic_range,address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.dynamic_range = dynamic_range
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

        
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа!")

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4752")

        first_byte = self.wm | self.pds | number >>8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X},0x{first_byte:02X}, 0x{second_byte:02X}]\n")
        

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический ЦАП (0.00 - {self.dynamic_range:.2f} ) В")
            self.set_number(0)
            return 0
        self.set_number(int(voltage/self.dynamic_range * 4095))
        return int(voltage/self.dynamic_range * 4095)


if __name__ == "__main__":
    try:
        dac = MCP4725(5.18)

        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()

#mcp4725-sin.py
import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 5.18
signal_frequency = 10
sampling_frequency = 1000



if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(5.18)

        while True:
            try:
              
                signal_amplitude = sg.get_sin_wave_amplitude(signal_frequency, time.time())
                voltage = signal_amplitude * amplitude
                dac.set_voltage(voltage)

                time.sleep(sg.wait_for_sampling_period(sampling_frequency))

            except ValueError:
                print("Ошибка значения. Попробуйте еще раз\n")
            except KeyboardInterrupt:
                print("\nПрограмма завершена")
                break
    finally:
        dac.deinit()

#mcp4725-trangle.py
import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 2.0
signal_frequency = 10
sampling_frequency = 1000



if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(5.18)
        while True:
            try:
              
                signal_amplitude = sg.get_triangle_wave_amplitude(signal_frequency, time.time())
                voltage = signal_amplitude * amplitude
                dac.set_voltage(voltage)

                time.sleep(sg.wait_for_sampling_period(sampling_frequency))

            except ValueError:
                print("Ошибка значения. Попробуйте еще раз\n")
            except KeyboardInterrupt:
                print("\nПрограмма завершена")
                break
    finally:
        dac.deinit()
