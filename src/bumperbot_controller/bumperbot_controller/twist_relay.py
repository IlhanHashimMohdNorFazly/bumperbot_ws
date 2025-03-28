#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistRelay(Node):
    def __init__(self):
        super().__init__('twist_relay')
        self.controller_sub = self.create_subscription(
            Twist,
            '/bumperbot_controller/cmd_vel_unstamped',
            self.controller_twist_callback,
            10
        )
        self.controller_pub = self.create_publisher(
            TwistStamped,
            '/bumperbot_controller/cmd_vel',
            10
        )

        self.joy_sub = self.create_subscription(
            TwistStamped,
            "/input_joy/cmd_vel_stamped",
            self.joy_twist_callback,
            10
        )

        self.joy_pub = self.create_publisher(
            Twist,
            "/input_joy/cmd_vel",
            10
        )

    def controller_twist_callback(self, msg):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now().to_msg() # add time stamp
        twist_stamped.twist = msg
        self.controller_pub.publish(twist_stamped)

    def joy_twist_callback(self, msg):
        twist = Twist()
        twist = msg.twist #  remove time stamp
        self.joy_pub.publish(twist)

def main():
    rclpy.init()
    twist_relay = TwistRelay()
    rclpy.spin(twist_relay)
    twist_relay.destroy_node()
    rclpy.shutdown() 

if __name__ == '__main__':
    main()