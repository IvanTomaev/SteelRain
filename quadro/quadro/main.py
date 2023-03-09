import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import threading
from quadro_interface.srv import Coder, Decoder
import pickle
import struct
class Main(Node):
    def __init__(self):
        self.check = 'loremipsum'
        super().__init__('main')
        self.publisher = self.create_publisher(String, 'actions', 10)
        self.keyPublisher = self.create_publisher(String, 'ket_data',10)
        self.subcriber = self.create_subscription(String, 'telemetry', self.callback, 10)
        self.Mainsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Mainsocket.bind('',9090)
        self.Mainsocket.listen(1)
        self.enc = self.create_client(Coder, 'coder')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.reqEn = Coder.Request()
        self.dec = self.create_client(Coder, 'coder')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.reqDec = Decoder.Request()
        self.conn, self.addr = self.Mainsocket.accept()
        
        self.key = self.getKey()
        self.keyPublisher.publish(self.key)
        while True:
            data = self.getData()
            data = self.decode(data).split()
            if data[0] == self.check():
                self.controls(data[1::])
            else:
                pass
    
    def encode(self, data):
        data = data[::-1]
        data = list(data)
        j= 0
        for i,item in enumerate(data):
            next_pos = ord(item) + ord(self.key[j])
            while next_pos > 126:
                next_pos = 32+(next_pos-126)
            data[i] = chr(next_pos)
            j+=1
            if j == len(self.key):
                j = 0
            if i % 2 != 0:
                temp = data[i-1]
                data[i-1]= data[i]
                data[i] = temp
        return ''.join(data)




    def controls(self,data):
        comands = data[1].split(';')
        waypoints = data[2].split(';')

        pass

    def callback(self, msg):
        data = self.encode(msg.data)
        self.con.sendall(data.encode())   

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
        return pickle.loads(key_data)


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
        return pickle.loads(key_data)


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

    def send_data(self, data):
        self.reqEn.data = data
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    def send_encoded(self, encoded):
        self.reqDec.encoded = encoded
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
def main(args = None):
    rclpy.init(args=args)
    main = Main()
    
    


if __name__ == '__main__':
    main()
