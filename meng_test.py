import time
from printer_driver import Printer

def connect_to_printer():
    ids = []
    mp_list = []
    baud_rate = 38400
    prefix = "/dev/serial/by-id/"

    printer_levels = [3]
    # printer_levels = [1, 2]

    ids.append("usb-Malyan_System_Malyan_3D_Printer_205932725748-if00")
    mp_list.append(True)
    printer =  Printer(prefix + p, baud_rate, mp=mp, id_=id_i)
    time.sleep(0.2)
    return printr

printer = connect_to_printer()
printer.startup()
printer.write("G28")

