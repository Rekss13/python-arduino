#!/usr/bin/env python3
import serial
import os
import select
import json
from datetime import datetime

IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"

def get_message(fifo):
    '''Read n bytes from pipe. Note: n=24 is an example'''
    return os.read(fifo, 50)

def process_msg(msg):
    '''Process message read from pipe'''
    return json.loads(msg.decode("utf-8"))

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS1', 9600, timeout=1)
    try:
        os.mkfifo(IPC_FIFO_NAME_A)
    except:
        print('fifo already exists')
    ser.flush()
    try:
        fifo_a = os.open(IPC_FIFO_NAME_A, os.O_RDONLY | os.O_NONBLOCK)  # pipe is opened as read only and in a non-blocking mode
        print('Pipe A ready')
        while True:
            try:
                fifo_b = os.open(IPC_FIFO_NAME_B, os.O_WRONLY)
                print("Pipe B ready")
                break
            except:
                pass # Wait until Pipe B has been initialized
        try:
            poll = select.poll()
            poll.register(fifo_a, select.POLLIN)
            try:
                while True:
                    line = ser.readline().decode('utf-8').rstrip()
                    print('----- Received from Arduino -----')
                    print(line)
                    if (line == 'getState'):
                        os.write(fifo_b, line.encode())
                    if (fifo_a, select.POLLIN) in poll.poll():
                        msg = get_message(fifo_a)                   # Read from Pipe A
                        msg = process_msg(msg)                      # Process Message
                        print('----- Received from JS -----')
                        print(msg['status'])
                        print(datetime.fromtimestamp(msg["date"] / 1000.0))
                        if (msg['status'] == 'start' or msg['status'] == 'work'):
                            ser.write(str(msg['status'] + "\n").encode('utf-8'))
            finally:
                poll.unregister(fifo_a)
        finally:
            os.close(fifo_a)
    finally:
        os.remove(IPC_FIFO_NAME_A)
        os.remove(IPC_FIFO_NAME_B)
