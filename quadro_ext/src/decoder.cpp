#include "rclcpp/rclcpp.hpp"
#include "quadro_interface/srv/binary_decoder.hpp"   
#include "std_msgs/msg/string.hpp"
#include <memory>
#include <string>
#include <vector>

using std::placeholders::_1;
using std::placeholders::_2;
using std::placeholders::_3;
using std::string;
class Decoder : public rclcpp::Node{



public:
    Decoder()
    : Node("Decoder"){
         // CHANGE
      rclcpp::Service<quadro_interface::srv::BinaryDecoder>::SharedPtr service = 
      this->create_service<quadro_interface::srv::BinaryDecoder>("binary_decoder",  &Decoder::decode);
      subscriber_ = this->create_subscription<std_msgs::msg::String>("key_topic", 10, std::bind(&Decoder::topic_callback, this, _1));

    }

  private:
    string key_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
    size_t count_;
    void decode(std::shared_ptr<quadro_interface::srv::BinaryDecoder::Request> request,
    std::shared_ptr<quadro_interface::srv::BinaryDecoder::Response> response){

                   }

    void topic_callback(const std_msgs::msg::String & msg)
    {
      key_ = msg.data;
    }
    
};















int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Decoder>());
  rclcpp::shutdown();
  return 0;



}