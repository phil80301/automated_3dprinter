import time
from printer_driver import Printer
from remover_driver import Remover

def connect_to_printers():
    ids = []
    mp_list = []
    baud_rate = 9600
    baud_rate = 115200
    prefix = "/dev/serial/by-id/"

    # printer_levels = [1, 2, 3, 4]
    printer_levels = [1, 2]

    ids.append("usb-Malyan_System_Malyan_3D_Printer_2058324D5748-if00")
    mp_list.append(True)
    ids.append("usb-Malyan_System_LTD._Malyan_3D_Printer_Port_8D8B33775656-if00")
    mp_list.append(False)
    # ids.append("usb-Malyan_System_Malyan_3D_Printer_205932725748-if00")
    # mp_list.append(True)
    # ids.append("usb-Malyan_System_Malyan_3D_Printer_207E39595250-if00")
    # mp_list.append(True)
    printer_list = []
    for id_i, p, mp in zip(printer_levels, ids, mp_list):
        printer_list.append(Printer(prefix + p, baud_rate, mp=mp, id_=id_i))

    time.sleep(1)
    return printer_list

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
    remover.connect()
    printer.write("M104 S210") # Set extruder temperature to 199 degrees celcius
    printer.write("M140 S61k") # Set bed temperature to 59 degrees celcius
    printer.write("G0 X0 Y120 Z100 F100000")
    printer.write("M400")
    remover.remove_print(printer_index)
    printer.write("G28 X Y")
    printer.write("G0 Z100 F100000")
    printer.write("M400")
    remover.knock()
    remover.winch_home()
    time.sleep(0.5)
    remover.disconnect()

def main(printers, remover):
    for i, p in enumerate(printers):
        p.startup()
        print("Finished Setting Up Printer {}".format(i))
    # remove_print(remover, 2, printers[0])
    # return
    file_name = "print_que.txt"
    print_list, num_prints = get_prints(file_name)

    print("Done setting up Printers")
    print("Total of {} prints".format(num_prints))

    finished = False
    print_index = 0
    finished_prints = 0
    while not finished:
        if print_index == num_prints - 1:
            # only check for if parts are done
            for i, p in enumerate(printers):
                if p.is_finished():
                    remove_print(remover, p.id(), p)
                else:
                    print("Printer {} Not Finished yet".format(i))
        else:
            for i, p in enumerate(printers):
                if not p.is_busy():
                    print("Printer {} is starting new print".format(i))
                    new_print = print_list[print_index]
                    print(new_print)
                    print_index += 1
                    p.start_print_from_sd(new_print)
                    continue
                else:
                    if p.is_finished():
                        remove_print(remover, p.id(), p)
                    else:
                        print("Printer {} Not Finished yet".format(i))
        time.sleep(0.1)

def remove_all(printers, remover):
    time.sleep(0.1)
    remover.connect()
    time.sleep(0.1)
    for p in printers:
        p.write("G0 X0 Y120 Z100 F100000")
    p[0].write("M400")
    for p in printers:
        remover.remove_print(p.id())
        p.write("G28 X Y")
        remover.knock()

    remover.winch_home()
    time.sleep(0.5)
    remover.disconnect()
    time.sleep(0.1)

if __name__== "__main__":
    printers = connect_to_printers()
    remover = connect_to_remover()
    # main(printers, remover)
    # remove_all(printers, remover)
    print("FINISHED MAIN")
