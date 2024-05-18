import pigpio

class IRReceiver:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.pi = pigpio.pi()
        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_glitch_filter(self.gpio_pin, 100)  # Filtro para eliminar ruido
        self.pi.callback(self.gpio_pin, pigpio.EITHER_EDGE, self.callback)
        self.data = []
        self.in_code = False

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
                self.decode_data()
        self.last_tick = tick

    def decode_data(self):
        # Aquí puedes decodificar self.data para obtener los comandos del control remoto
        print("Raw data:", self.data)

    def stop(self):
        self.pi.stop()

if __name__ == "__main__":
    gpio_pin = 17  # Reemplaza con el pin GPIO al que está conectado el VS1838B
    receiver = IRReceiver(gpio_pin)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        receiver.stop()
