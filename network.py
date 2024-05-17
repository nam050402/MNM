import socket
import pickle
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.5"
        # "192.168.1.112"
        self.port = 8081
        self.addr = (self.server, self.port)
        self.client_state = self.connect()
        # print(self.client_state)

    def get_client_state(self):
        return self.client_state

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096))
        except:
            pass
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            #return self.client.recv(4096).decode()
        except socket.error as e:
            print(e)
    def recieve(self):
        return pickle.loads(self.client.recv(4096))
