
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from quadro_interface.srv import Coder

class coder(Node):
    def __init__(self):
        super().__init__('coder')
        self.subscription = self.create_subscription(String, 'key_data', self.callback, 10)
        self.coderSrv = self.create_service(Coder, 'coder', self.encode)
        
        self.key = ''

    def callback(self, msg):
        self.key = msg.data
        self.get_logger().info('received coder key : %s' %self.key)
    def encode(self, request, response):
        data = list(request.data)
        data = data[::-1]
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
        response.encoded = ''.join(data)[::-1]
        return response


    
    
def main(args = None):
    rclpy.init(args=args)
    cod = coder()
    rclpy.spin(cod)
    cod.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    