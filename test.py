#!/usr/bin/env python3
import serial
import os
import select
import json
# from datetime import datetime
from threading import Thread

IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"

def pipoWrite():
    print('start pipoWrite')
    isOpen = False
    while True:
        if (isOpen == False):
            try:
                fifo_b = os.open(IPC_FIFO_NAME_B, os.O_WRONLY)
                print("Pipe B ready")
                isOpen = True
            except:
                pass
        line = ser.readline().decode('utf-8').rstrip()
        if (len(line) > 0):
            print('----- Received from Arduino -----')
            print(line)
            if (line == 'getState'):
                os.write(fifo_b, line.encode())

def pipoRead():
    print('start pipoRead')
    try:
        os.mkfifo(IPC_FIFO_NAME_A)
    except:
        pass
    fifo_a = os.open(IPC_FIFO_NAME_A, os.O_RDONLY | os.O_NONBLOCK)
    print('Pipe A ready')
    poll = select.poll()
    poll.register(fifo_a, select.POLLIN)
    while True:
        if (fifo_a, select.POLLIN) in poll.poll():
            msg = os.read(fifo_a, 50).decode("utf-8")
            try:
                print('----- Received from JS -----')
                print(msg)
                msg = json.loads(msg)
                print(msg['status'])
                #print(datetime.fromtimestamp(msg["date"] / 1000.0))
                if (msg['status'] == 'start' or msg['status'] == 'work'):
                    print('send to Arduino: ' + msg['status'])
                    ser.write(str(msg['status'] + "\n").encode('utf-8'))
            except:
                pass

thread_1, thread_2 = Thread(target=pipoWrite), Thread(target = pipoRead)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
    ser.flush()

    thread_1.start(), thread_2.start()
    thread_1.join(), thread_2.join()
