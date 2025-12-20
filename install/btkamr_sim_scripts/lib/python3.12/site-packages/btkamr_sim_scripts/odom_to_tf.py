#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdomToTF(Node):
    def __init__(self):
        super().__init__('odom_to_tf')

        # İstersen parametre yap
        self.declare_parameter('odom_topic', 'btkamr/odom')
        self.declare_parameter('default_parent_frame', 'odom')   # Odometry.header.frame_id boşsa
        self.declare_parameter('default_child_frame', 'base_link')  # Odometry.child_frame_id boşsa

        odom_topic = self.get_parameter('odom_topic').value
        self.default_parent = self.get_parameter('default_parent_frame').value
        self.default_child = self.get_parameter('default_child_frame').value

        self.br = TransformBroadcaster(self)
        self.sub = self.create_subscription(Odometry, odom_topic, self.cb, 50)

        self.get_logger().info(f"Subscribing: {odom_topic}  | Broadcasting TF")

    def cb(self, msg: Odometry):
        t = TransformStamped()

        # Zaman damgasını aynen kullan
        t.header.stamp = msg.header.stamp
        
        t.header.frame_id = "odom_frame"
        t.child_frame_id  = "base_footprint"

        # Pose -> TF
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation

        t.transform.translation.x = float(p.x)
        t.transform.translation.y = float(p.y)
        t.transform.translation.z = float(p.z)

        t.transform.rotation.x = float(q.x)
        t.transform.rotation.y = float(q.y)
        t.transform.rotation.z = float(q.z)
        t.transform.rotation.w = float(q.w)

        self.br.sendTransform(t)


def main():
    rclpy.init()
    node = OdomToTF()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
