import socket
from network import Network

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.48.205", 8081))
print(s)

while True:
    msg = s.recv(1024)
    print(msg.decode('utf-8'))