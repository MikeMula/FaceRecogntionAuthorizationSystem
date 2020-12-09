import serial                                           # import serial library
arduino = serial.Serial('/dev/cu.usbmodem14201', 9600)   # create serial object named arduino

# Send 'open' command to arduino board
def openDoor(command):
        print("Door opening...")
        arduino.write(str.encode(command))         
