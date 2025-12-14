import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("klavye_kontrol")

def main():
    rclpy.init()
    n = MyNode()
    rclpy.spin(n)
    rclpy.shutdown()