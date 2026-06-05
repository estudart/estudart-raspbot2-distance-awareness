import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Range


class UltrasonicProcessor(Node):
    def __init__(self):
        super().__init__("ultrasonic_processor")

        self.latest_distance = None

        self.subscription = self.create_subscription(
            Range,
            "/ultrasonic",
            self.ultrasonic_callback,
            10,
        )

        self.timer = self.create_timer(
            0.1,  # 10 Hz
            self.control_loop,
        )

    def ultrasonic_callback(self, msg: Range):
        self.latest_distance = msg.range
        print(self.latest_distance)

    def control_loop(self):
        if self.latest_distance is None:
            return

        if self.latest_distance < 0.3:
            self.stop_robot()
        else:
            self.move_forward()

    def stop_robot(self):
        self.get_logger().warning("STOP")

    def move_forward(self):
        self.get_logger().info("MOVING")


def main(args=None):
    rclpy.init(args=args)

    node = UltrasonicProcessor()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()