import sys
import time
import serial

def writeMessage(topic, message):
    payload = 'topic ' + topic + ' ' + message + ' ' + str(len(message)) + '\n'
    print(payload)
    
    ser.write(payload.encode())
    ser.flush()
    time.sleep(1)
    while ser.in_waiting != 0:
        data_in = ser.readline()
        print(data_in)

def callRSLoop(topic):
    payload = 'fast100 ' + topic + '\n'
    print(payload)

    ser.write(payload.encode())

def fast():
    for i in range(100):
        writeMessage('fast', str(i))
        time.sleep(3)

def everyMinute():
    for i in range(10):
        writeMessage('everyMinute', str(i))
        time.sleep(60)

if __name__ == "__main__":
    port = sys.argv[1] # For example /dev/ttyUSB0
    baudrate = sys.argv[2] # For example 115200
    ser = serial.Serial(port, baudrate, timeout=0.050)
    
    # Uncomment the function that should be runned
    #callRSLoop('RSLoop')
    fast()
    #everyMinute()
    #time.sleep(600)
    sys.exit()
