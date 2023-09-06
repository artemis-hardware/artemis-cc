import serial
from time import sleep
import sys

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS)

# Send one message command to CC and print response
def send(topic, msg):
	command = 'send ' + topic + ' ' + msg + ' ' + str(len(msg)) + '\n'
	ser.write(command.encode())
	print('USB device: ', ser.port, '\ttopic: ', topic, '\tmessage: ', msg)

if __name__ == '__main__':
	usage_str = 'usage:\n\tsend <topic> <message>\n\tmany <topic> <number of sends> <seconds of sleep between sends>\n\tloop <topic> <number of messages> <sleep between messages>'
	if sys.argv[1] == 'send' and len(sys.argv) == 4:
		topic = sys.argv[2]
		msg = sys.argv[3]
		send(topic, msg)
	elif sys.argv[1] == 'loop' and len(sys.argv) == 5:
		topic = sys.argv[2]
		amount = sys.argv[3]
		sleeptime = sys.argv[4]
		ser.write(('loop ' + topic + ' ' + amount + ' ' + sleeptime).encode())
	elif sys.argv[1] == 'many' and len(sys.argv) == 5:
		topic = sys.argv[2]
		number = int(sys.argv[3])
		sleeptime = float(sys.argv[4])
		for i in range (0, number):
			send(topic, str(i))
			sleep(sleeptime)
	elif (sys.argv[1] == 'z'):
		ser.write('z'.encode())
	else:
		print(usage_str)
