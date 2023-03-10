import rclpy
from rclpy.node import Node
import socket
import struct
import pickle
import numpy as np
import cv2

class cameraNode(Node):
    def __init__(self):
        super().__init__('main')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 5050))
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()


    def capture(self):
        pass



    def send(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = cameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()