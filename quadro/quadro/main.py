import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import threading
from quadro_interface.srv import Coder, Decoder
import pickle
import struct
import time
class Main(Node):
    def __init__(self):
        self.check = 'loremipsum'
        super().__init__('main')
        self.publisher = self.create_publisher(String, 'actions', 10)
        self.keyPublisher = self.create_publisher(String, 'ket_data',10)
        self.subcriber = self.create_subscription(String, 'telemetry', self.callback, 10)
        self.Mainsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Mainsocket.bind(('',8080))
        self.Mainsocket.listen(1)
        self.enc = self.create_client(Coder, 'coder')
        while not self.enc.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('encoding service not available, waiting again...')
        self.reqEn = Coder.Request()
        self.dec = self.create_client(Coder, 'coder')
        while not self.dec.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('decoding service not available, waiting again...')
        self.reqDec = Decoder.Request()
        self.conn, self.addr = self.Mainsocket.accept()
        
        self.key = self.getKey()
        msg = String()
        msg.data = self.key
        self.keyPublisher.publish(msg)
        while True:
            data = self.getData()
            self.get_logger().info('received daa : %s' %data)
            data = self.decode_data(data).data.split()
            if data[0] == self.check():
                print(data)
                #self.controls(data[1::])
            else:
                pass
    
   




    def controls(self,data):
        comands = data[1].split(';')
        waypoints = data[2].split(';')

        pass

    def callback(self, msg):
        data = self.encode_data(msg.data)
        self.con.sendall(data.encode())   

    def getData(self):
        data = b''
        payload_size = struct.calcsize('Q')
        while len(data)< payload_size:
            packet = self.conn.recv(1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += self.conn.recv(1024)
        key_data = data[:msg_size]
        data = data[msg_size:]
        return pickle.loads(key_data)


    def getKey(self):
        time.sleep(3)
        data = b''
        payload_size = struct.calcsize('Q')
        print(payload_size)
        while len(data)< payload_size:
            packet = self.conn.recv(1)
            if not packet:
                break
            print(packet)
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += self.conn.recv(1)
        key_data = data[:msg_size]
        data = data[msg_size:]
        return pickle.loads(key_data)


    

    def encode_data(self, data):
        self.reqEn.data = data
        self.future = self.enc.call_async(self.reqEn)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    def decode_data(self, encoded):
        self.reqDec.encoded = encoded
        self.future = self.dec.call_async(self.reqDec)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
def main(args = None):
    rclpy.init(args=args)
    main = Main()
    
    


if __name__ == '__main__':
    main()
