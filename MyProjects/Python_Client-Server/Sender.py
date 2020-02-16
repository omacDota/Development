# Message Sender
import os
from socket import *
import array
host = "127.0.0.1" # set to IP address of target computer
port = 13000  # Find Empty Port
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)


while True:
    data = input("Enter message to send or type 'exit': ")
    print(data.encode())
    UDPSock.sendto(data.encode(), addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)