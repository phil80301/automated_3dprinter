import time
from printer_driver import Printer
import serial

class Remover:
    def __init__(self, port_servo, port_winch):
        self.servo_ser = serial.Serial(port_servo, 115200, timeout=30)
        self.winch_ser = serial.Serial(port_winch, 115200, timeout=30)

        if self.servo_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from servo Arduino')

        if self.winch_ser.readline().strip() != 'Ready':
            raise ValueError('Received unexpected response from winch Arduino')

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

    def remove_print(self, index):
        self.send_command_winch("i {}".format(index))
        self.send_command_servo("c")
        self.send_command_winch("o 75")
        self.send_command_servo("f")
        self.send_command_winch("o -75")
        self.send_command_servo("o")

    def open(self):
        self.send_command_servo("o")

    def close(self):
        self.send_command_servo("c")

    def winch_home(self):
        self.send_command_servo("o")
        self.send_command_winch("h")

    def close_ser(self):
        self.servo_ser.close()
        self.winch_ser.close()

def connect_to_printers():
    ids = []
    mp_list = []
    baud_rate = 9600
    baud_rate = 115200
    prefix = "/dev/serial/by-id/"
    # prefix = "COM"

    # ids.append("13")
    # ids.append("5")
    # ids.append("7")
    #ids.append("6")
    #ids.append("4")
    # printer_levels = [1, 2, 3, 4]
    printer_levels = [3]

    # ids.append("usb-Malyan_System_Malyan_3D_Printer_2058324D5748-if00")
    # mp_list.append(True)
    # ids.append("usb-Malyan_System_LTD._Malyan_3D_Printer_Port_8D8B33775656-if00")
    # mp_list.append(False)
    ids.append("usb-Malyan_System_Malyan_3D_Printer_205932725748-if00")
    mp_list.append(True)
    # ids.append("usb-Malyan_System_Malyan_3D_Printer_207E39595250-if00")
    # mp_list.append(True)
    printer_list = []
    for p, mp in zip(ids, mp_list):
        printer_list.append(Printer(prefix + p, baud_rate, mp=mp))
    time.sleep(1)

    return printer_list, printer_levels

def connect_to_remover():
    prefix = "/dev/serial/by-id/"
    winch_port = "usb-1a86_USB2.0-Serial-if00-port0"
    servo_port = "usb-FTDI_FT232R_USB_UART_A601F7Y5-if00-port0"
    return Remover(prefix + winch_port, prefix + servo_port)

def get_prints(file_name):
    print_list = []
    content = None
    with open(file_name) as f:
        content = f.readlines()
    for i in content:
        line = i.split()
        print_list.append(line[0])
    return print_list, len(print_list)


def remove_print(remover, printer_index, printer):
    print("Removing Print from Printer {}".format(printer_index))
    printer.write("M104 S210") # Set extruder temperature to 199 degrees celcius
    printer.write("M140 S61k") # Set bed temperature to 59 degrees celcius
    printer.write("G0 X0 Y120 F100000")
    # printer.write("M400")
    remover.remove_print(printer_index)
    printer.write("G28 X Y")
    remover.send_command_winch("o 40")
    remover.send_command_servo("c")
    remover.send_command_servo("o")
    remover.send_command_servo("c")
    remover.send_command_servo("o")
    remover.winch_home()
    time.sleep(1.0)

printers, levels  = connect_to_printers()
remover = connect_to_remover()
for i, p in enumerate(printers):
    p.startup()
    print("Finished Setting Up Printer {}".format(i))
