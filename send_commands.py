import time
from printer_driver import Printer
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
            for i in range(1000000):
                time.sleep(0.2)
                printer.write("M400")
            removal_pos(printer)
            printer.write("M106 S0") # turn off fan



print_file = "print_que.txt"
printer = Printer("/dev/ttyACM0", 9600, verbose=True)
time.sleep(0.5)
printer.write("M21")
time.sleep(0.2)
printer.write("G28")
printer.write("M400")
printer.write("G90")
printer.write("G0 X0 Y0 Z10 F10000")
printer.write("M400")
print_from_file(print_file, printer)

# printer.write("G90")
# printer.write("G1 X30 F4800")
# printer.write("G91")
# printer.write("M32 top.gcode")
