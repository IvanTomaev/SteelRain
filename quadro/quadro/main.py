import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import threading
import pickle
import struct
class Main(Node):
    def __init__(self):
        self.check = 'ZOV'
        super().__init__('main')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.Mainsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Mainsocket.bind('',9090)
        self.Mainsocket.listen(1)
        self.conn, self.addr = self.Mainsocket.accept()
        self.key = self.getKey()
        while True:
            data = self.getData()
            data = self.decode(data).split()
            if data[0] == self.check():
                self.controls(data)
            else:
                pass
    
    def controls(self,data):
        pass



    def getData(self):
        data = b''
        payload_size = struct.calcsize('Q')
        while len(data)< payload_size:
            packet = self.Mainsocket.recv(1024)
            if not packet:
                break
        data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += self.Mainsocket.recv(1024)
        key_data = data[:msg_size]
        data = data[msg_size:]
        return pickle.loads(key_data).decode()


    def getKey(self):
        data = b''
        payload_size = struct.calcsize('Q')
        while len(data)< payload_size:
            packet = self.Mainsocket.recv(1)
            if not packet:
                break
        data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += self.Mainsocket.recv(1)
        key_data = data[:msg_size]
        data = data[msg_size:]
        return pickle.loads(key_data).decode('utf-8')



    def decode(self, data):
        j = 0
        data = list(data)
        for i,item in enumerate(data):
            if i%2 == 0 and i<len(data)-1:
                temp = data[i+1]
                data[i+1]= data[i]
                data[i] = temp
        for i,item in enumerate(data):
            next_pos = ord(item) - ord(self.key[j])
            while next_pos <32:
                next_pos = -32+(next_pos+126)
            data[i] = chr(next_pos)
            j+=1
            if j == len(self.key):
                j = 0

        return ''.join(data)[::-1]





def main(args = None):
    rclpy.init(args=args)
    main = Main()
    


if __name__ == '__main__':
    main()
