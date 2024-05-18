import pigpio
import time

class IRReceiver:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self.pi = pigpio.pi()
        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_glitch_filter(self.gpio_pin, 100)
        self.pi.callback(self.gpio_pin, pigpio.EITHER_EDGE, self.callback)
        self.data = []
        self.in_code = False
        self.last_tick = 0

        # Mapeo de códigos IR a comandos
        self.command_map = {
            '10000000100001010001001011101100': 'up',
            '10000000100001010001001011101000': 'down',
            '10000000100001010001001011100100': 'left',
            '10000000100001010001001011100010': 'right',
            '10000000100001010001001011011100': 'select'
        }

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
        if len(self.data) < 32:  # La mayoría de los códigos IR tienen 32 bits
            return
        
        binary_string = ''.join(['1' if t > 1000 else '0' for t in self.data])
        command = self.command_map.get(binary_string)
        
        if command:
            self.execute_command(command)

    def execute_command(self, command):
        print(f"Command received: {command}")
        # Aquí puedes añadir la lógica para controlar tu interfaz
        if command == 'up':
            print("Move up")
        elif command == 'down':
            print("Move down")
        elif command == 'left':
            print("Move left")
        elif command == 'right':
            print("Move right")
        elif command == 'select':
            print("Select option")

    def stop(self):
        self.pi.stop()

if __name__ == "__main__":
    gpio_pin = 17  # Reemplaza con el pin GPIO al que está conectado el VS1838B
    receiver = IRReceiver(gpio_pin)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        receiver.stop()
