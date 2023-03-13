#include "rclcpp/rclcpp.hpp"
#include "quadro_interface/srv/decoder.hpp"   

#include <memory>
#include <string>
#include <vector>



class Decoder : public rclcpp::Node{



public:
    Decoder()
    : Node("Decoder"), count_(0)
    {
      rclcpp::Service<quadro_interface::srv::Decoderbin>::SharedPtr service =               // CHANGE
      node->create_service<quadro_interface::srv::Decoderbin>("decoder",  &Decoder::decode);   // CHANGE
      subscriber_ = this->create_subscriber<std_msgs::msg::String>("key_topic", 10, std::bind(&Decoder::topic_callback, this, _1));

    }

  private:
    std::string key_;

    void decode(std::shared_ptr<quadro_interface::srv::Decoderbin::Request> request,std::shared_ptr<quadro_interface::srv::Decoderbin::Response> response){
          auto data = request -> encoded;
          std::byte temp;
          for(int i = 0; i < data.size()-1; i++){
              if(i%2 == 0){
                temp = data[i];
                data[i] = data[i+1];
                data[i+1] = temp;
              }
              
              }

                   }

    void topic_callback(const std_msgs::msg::String & msg) const
    {
      key_ = msg.data
    }
    rclcpp::Subscriber<std_msgs::msg::String>::SharedPtr subscriber_;
    size_t count_;
};













void add(const std::shared_ptr<quadro_interface::srv::Decoder::Request> request,     // CHANGE
          std::shared_ptr<quadro_interface::srv::Decoder::Response>       response)  // CHANGE
{
  response->data = request->encoded;                                     // CHANGE
 
}

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Decoder>());
  rclcpp::shutdown();
  return 0;



}