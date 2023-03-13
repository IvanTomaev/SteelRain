#include "rclcpp/rclcpp.hpp"
#include "quadro_interface/srv/Coder.hpp"
#include "quadro_interface/srv/Decoder.hpp"  

#include <memory>
#include "std_msgs/msg/string.hpp"




// using namespace boost::asio;
// using ip::tcp;
// using boost::asio::ip::adress;
// using std::string;
// using std::cout;
// using std::endl;



class Receiver  : public rclcpp::Node{


    private:
    // types
        string key;

    public:
    Receiver()
    : Node("Receiver"), count_(0)
    {
      publisher_ = this->create_subscriber<std_msgs::msg::String>("key_topic", 10);
      timer_ = this->create_wall_timer(
      500ms, std::bind(&Receiver::timer_callback, this));
    }
}





int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
