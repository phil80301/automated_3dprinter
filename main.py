import time
from printer_driver import Printer

def connect_to_printer():
    ids = []
    baud_rate = 960
    ids.append(111)
    ids.append(222)
    ids.append(333)
    ids.append(444)
    printer_list = [Printer(id_i, baud_rate) for id_i in ids]
    return printer_list

def removal_pos(p):
    p.write("G90")
    # z 40 for now for speed of tests
    p.write("G0 X0 Y100 Z40 F10000")
    p.write("M400")
    # p.write("G0 X0 Y100 Z100 F10000")

def print_from_file(filename, printer):
    print_list = []
    content = None
    with open(filename) as f:
        content = f.readlines()
    for i in content:
        line = i.split()
        print_list.append(line)
    for p in print_list:
        times = p[0]
        sd_file = p[1]
        for t in range(int(times)):
            print("Printing file: " + sd_file)
            printer.write("M23 " + sd_file)
            printer.write("M400")
            printer.write("M24")
            printer.write("M400")
            done = False
            while not done:
                time.sleep(10)
                response = printer.write("M27")
		print(response)
                ratio = [int(s) for s in response.split()[-1].split("/") if s.isdigit()]
		if not len(ratio) == 2:
			continue
                if float(ratio[0])/float(ratio[1]) >= 0.9999:
                    done = True
                    print("Finished Printing")

            removal_pos(printer)
            printer.write("M106 S0") # turn off fan


def main():


if __name__== "__main__":
    main()
