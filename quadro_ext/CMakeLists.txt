cmake_minimum_required(VERSION 3.8)
project(quadro_ext)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(quadro_interface REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tutorial_interfaces REQUIRED) 

# add_executable(receiver src/receiver.cpp)
# ament_target_dependencies(receiver rclcpp std_msgs quadro_interface)
# add_executable(coder src/coder.cpp)
# ament_target_dependencies(coder rclcpp std_msgs tutorial_interfaces)
add_executable(decoder src/decoder.cpp)
ament_target_dependencies(decoder rclcpp std_msgs quadro_interface)
install(TARGETS
  #receiver
  #coder
  decoder
  DESTINATION lib/${PROJECT_NAME})
ament_package()
