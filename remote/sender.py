import socket

WIFI_IP = "192.168.1.1"
WIFI_PORT = 2345
WIFI_INTERFACE = "192.168.1.20"

ETHERNET_TARGET_IP = "192.168.1.105"
ETHERNET_PORT = 6789

def forward_data():
    wifi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wifi_socket.bind((WIFI_INTERFACE, 0))
    wifi_socket.connect((WIFI_IP, WIFI_PORT))

    ethernet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ethernet_socket.connect((ETHERNET_TARGET_IP, ETHERNET_PORT))

    print("Forwarding DJI Data to PC...")

    try:
        while True:
            data = bytearray(wifi_socket.recv(1024))
            if len(data) > 0:
                ethernet_socket.sendall(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        wifi_socket.close()
        ethernet_socket.close()

if __name__ == "__main__":
    forward_data()