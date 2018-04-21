import time
from printer_driver import Printer

def connect_to_printers():
    ids = []
    mp_list = []
    baud_rate = 9600
    prefix = "/dev/serial/by-id/"
    # prefix = "COM"

    # ids.append("13")
    # ids.append("5")
    # ids.append("7")
    #ids.append("6")
    #ids.append("4")

    ids.append("usb-Malyan_System_Malyan_3D_Printer_2058324D5748-if00")
    mp_list.append(True)
    ids.append("usb-Malyan_System_LTD._Malyan_3D_Printer_Port_8D8B33775656-if00")
    mp_list.append(False)
    ids.append("usb-Malyan_System_Malyan_3D_Printer_205932725748-if00")
    mp_list.append(True)
    ids.append("usb-Malyan_System_Malyan_3D_Printer_207E39595250-if00")
    mp_list.append(True)
    printer_list = []
    for p, mp in zip(ids, mp_list):
        printer_list.append(Printer(prefix + p, baud_rate, mp=mp))
    time.sleep(1)

    return printer_list

def get_prints(file_name):
    print_list = []
    content = None
    with open(file_name) as f:
        content = f.readlines()
    for i in content:
        line = i.split()
        print_list.append(line[0])
    return print_list, len(print_list)


def remove_print(printer_index, printer):
    print("Removing Print from Printer {}".format(printer_index))
    printer.write("M104 S210") # Set extruder temperature to 199 degrees celcius
    print("a")
    printer.write("M140 S61k") # Set bed temperature to 59 degrees celcius
    print("a")
    time.sleep(0.4)

    pass

def main():
    printers = connect_to_printers()
    file_name = "print_que.txt"
    print_list, num_prints = get_prints(file_name)
    for i, p in enumerate(printers):
        p.startup()
        print("Finished Setting Up Printer {}".format(i))

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
                    remove_print(i, p)
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
                        remove_print(i, p)
                    else:
                        print("Printer {} Not Finished yet".format(i))
        time.sleep(0.0)





if __name__== "__main__":
    main()
    print("FINISHED MAIN")