from printer_driver import Printer

print_list = []

print_file = "print_que.txt"
content = None
with open(print_file) as f:
    content = f.readlines()
for i in content:
    line = i.split()
    print_list.append(line)

for p in print_list:
    times = p[0]
    sd_file = p[1]
    for t in range(times):
        print("Printing file: " + sd_file)
        printer.write("M32 " + sd_file)

# printer = Printer("/dev/ttyACM0", 9600, verbose=True)
# printer.write("G90")
# printer.write("G1 X30 F4800")
# printer.write("G1 X0 F3600")
# printer.write("M32 top.gcode")
