import pigpio
import time

class IRReceiver:
    def __init__(self, gpio_pin, file_name):
        self.gpio_pin = gpio_pin
        self.file_name = file_name
        self.pi = pigpio.pi()
        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_glitch_filter(self.gpio_pin, 100)
        self.pi.callback(self.gpio_pin, pigpio.EITHER_EDGE, self.callback)
        self.data = []
        self.in_code = False
        self.last_tick = 0

    def callback(self, gpio, level, tick):
        if level == pigpio.FALLING_EDGE:
            if not self.in_code:
                self.data = []
                self.in_code = True
            self.data.append(pigpio.tickDiff(self.last_tick, tick))
        elif level == pigpio.RISING_EDGE:
            if self.in_code:
                self.data.append(pigpio.tickDiff(self.last_tick, tick))
                self.in_code = False
                self.save_data()
        self.last_tick = tick

    def save_data(self):
        if len(self.data) > 0:
            with open(self.file_name, 'a') as file:
                file.write(','.join(map(str, self.data)) + '\n')
                file.write('-----------\n')
            print("Data saved:", self.data)

    def stop(self):
        self.pi.stop()

if __name__ == "__main__":
    gpio_pin = 17  # Reemplaza con el pin GPIO al que está conectado el VS1838B
    file_name = 'ir_data.txt'  # Nombre del archivo donde se guardarán los datos
    receiver = IRReceiver(gpio_pin, file_name)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        receiver.stop()
