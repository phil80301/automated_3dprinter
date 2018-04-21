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



print_file = "print_que.txt"
# printer = Printer("/dev/serial/by-id/usb-Malyan_System_Malyan_3D_Printer_207E39595250-if00", 9600, verbose=True)
# printer = Printer("/dev/serial/by-id/usb-Malyan_System_Malyan_3D_Printer_205932725748-if00", 115200, verbose=True)
printer = Printer("COM13", 115200, verbose=True)
time.sleep(0.5)
printer.write("G28 X Y", resp=True)
printer.write("M21", resp=True)
printer.write("M105", resp=True)
time.sleep(0.2)
printer.write("M105", resp=False)
time.sleep(0.2)
printer.write("M105", resp=False)
time.sleep(0.2)
# printer.write("M400")
# printer.write("G90")
# printer.write("G0 X0 Y0 Z10 F10000")
# printer.write("M400")
# print_from_file(print_file, printer)

# printer.write("G90")
# printer.write("G1 X30 F4800")
# printer.write("G91")
# printer.write("M32 top.gcode")
