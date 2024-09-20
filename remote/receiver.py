import socket
from ctypes import *

vjoy = CDLL('C:\\Program Files\\vJoy\\x64\\vJoyInterface.dll')
vjoy.AcquireVJD(1)
vjoy.ResetVJD(1)

def word(b0, b1):
    return (b0 << 8) | b1

def scale(x):
    return int((x - 364) / 1320 * 32768)

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 6789

def receive_and_process_data():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTEN_IP, LISTEN_PORT))
    server_socket.listen(1)

    print(f"Listening for incoming data on port {LISTEN_PORT}...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        while True:
            data = bytearray(client_socket.recv(1024))
            if len(data) == 26:
                rightX = word(data[12], data[11])
                rightY = word(data[14], data[13])
                leftY = word(data[16], data[15])
                leftX = word(data[18], data[17])
                cam = word(data[20], data[19])

                print(f"leftX: {leftX}, leftY: {leftY}, rightX: {rightX}, rightY: {rightY}, cam: {cam}")

                vjoy.SetAxis(scale(leftX), 1, 48)
                vjoy.SetAxis(scale(leftY), 1, 49)
                vjoy.SetAxis(scale(rightX), 1, 50)
                vjoy.SetAxis(scale(rightY), 1, 51)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    receive_and_process_data()
