import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from quadro_interface.srv import  Decoder


class decoder(Node):
    def __init__(self):
        super().__init__('decoder')
        self.subscription = self.create_subscription(String, 'key_data', self.callback, 10)
        self.key = ''
        self.decoderSrv = self.create_service(Decoder, 'decoder', self.decode)
    def callback(self, msg):
        self.key = msg.data
        self.get_logger().info('received decoder key : %s' %self.key)


    def decode(self, request, response):
        j = 0
        data = list(request.encoded)
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
        response.data = ''.join(data)[::-1]
        return response
    
def main(args = None):
    rclpy.init(args=args)
    cod = decoder()
    rclpy.spin(cod)
    cod.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()