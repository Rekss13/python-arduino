#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
    ser.flush()
    count = 0
    count += 1
    print('----- Received from JS -----')
    msg = 'restart'
    print(msg)
    ser.write(str(msg + "\n").encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        if (len(line) > 0):
            print('----- Received from Arduino -----')
            print(line)
            if (line == 'getState'):
                count += 1
                print('----- Received from JS ----- ' + str(count))
                msg = 'work' if (count < 10) else 'error'
                if (count == 10): count = 0
                print(msg)
                ser.write(str(msg + "\n").encode('utf-8'))