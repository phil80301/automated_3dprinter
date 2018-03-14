from printer_driver import Printer
def removal_pos(p):
    p.write("G90")
    p.write("G0 X100 Y100 Z100 F6000")

printer = Printer("/dev/ttyACM0", 9600, verbose=True)
# printer.write("G91")
# printer.write("G1 X0 F3600")
# printer.write("M32 top.gcode")
removal_pos(printer)

