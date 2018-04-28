import serial
import time

class Remover:
    def __init__(self, port_servo, port_winch):
        self.servo_ser_port = port_servo
        self.winch_ser_port = port_winch
        self.connected = False

        self.servo_ser = serial.Serial(self.servo_ser_port, 115200, timeout=30)
        self.winch_ser = serial.Serial(self.winch_ser_port, 115200, timeout=30)

        if self.servo_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from servo Arduino')

        if self.winch_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from winch Arduino')
        time.sleep(1)
        self.disconnect()
        time.sleep(1)


    def send_command_winch(self, command):
        self.winch_ser.write(command)
        response = self.winch_ser.readline().strip()
        if response != 'OK':
            raise ValueError('Received unexpected response from Arduino: {}'.format(response))

    def send_command_servo(self, command):
        self.servo_ser.write(command)
        response = self.servo_ser.readline().strip()
        if response != 'OK':
            raise ValueError('Received unexpected response from Arduino: {}'.format(response))

    def move(self, index):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_winch("i {}".format(index))

    def up(self, mm):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_winch("o {}".format(mm))

    def open(self):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_servo("o")

    def close(self):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_servo("c")

    def remove_print(self, index):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_servo("e")
        self.send_command_winch("i {}".format(index))
        self.send_command_servo("c")
        self.send_command_winch("o 100")
        self.send_command_servo("F 53")
        self.send_command_servo("F -40")
        self.send_command_servo("F 53")
	if index == 2:
            self.send_command_winch("o -93")
	else:
            self.send_command_winch("o -99")
        self.send_command_servo("o")

    def knock(self):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_winch("o 25")
        self.send_command_servo("c")
        self.send_command_servo("o")
        self.send_command_servo("d")

    def winch_home(self):
        if not self.connected:
            raise ValueError('Not Connected')
            return
        self.send_command_servo("e")
        self.send_command_servo("o")
        self.send_command_servo("d")
        self.send_command_winch("h")

    def connect(self):
        self.servo_ser.open()
        self.winch_ser.open()
        time.sleep(1)
        if self.servo_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from servo Arduino')

        if self.winch_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from winch Arduino')
        self.connected = True 

    def disconnect(self):
        self.servo_ser.close()
        self.winch_ser.close()
        time.sleep(1)
        self.connected = False

if __name__ == "__main__":
    prefix = "/dev/serial/by-id/"
    winch_port = "usb-1a86_USB2.0-Serial-if00-port0"
    servo_port = "usb-FTDI_FT232R_USB_UART_A601F7Y5-if00-port0"
    r = Remover(prefix + winch_port, prefix + servo_port)

