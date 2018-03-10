from printer_driver import Printer

printer = Printer("/dev/ttyACM0", 9600, verbose=True)
printer.write("G91")
printer.write("G1 X30 F4800")
# printer.write("G1 X0 F3600")
# printer.write("M32 top.gcode")
