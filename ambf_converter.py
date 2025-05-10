import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyCmd


class PoseToRigidBodyPublisher(Node):
    def __init__(self):
        super().__init__('pose_to_rigidbody_cmd_publisher')

        self.pose_topic = '/tumor_transform'  # Replace with your actual PoseStamped topic
        self.cmd_topic = '/ambf/env/Chassis/Command'  # Replace with your actual RigidBody command topic

        self.publisher_ = self.create_publisher(RigidBodyCmd, self.cmd_topic, 10)
        self.subscription = self.create_subscription(
            PoseStamped,
            self.pose_topic,
            self.pose_callback,
            10
        )

        self.get_logger().info(f"Subscribed to: {self.pose_topic}")
        self.get_logger().info(f"Publishing to: {self.cmd_topic}")

    def pose_callback(self, msg: PoseStamped):
        cmd_msg = RigidBodyCmd()
        cmd_msg.header.stamp = self.get_clock().now().to_msg()

        cmd_msg.pose.position.x = msg.pose.position.x
        cmd_msg.pose.position.y = msg.pose.position.y
        cmd_msg.pose.position.z = msg.pose.position.z

        cmd_msg.pose.orientation.x = msg.pose.orientation.x
        cmd_msg.pose.orientation.y = msg.pose.orientation.y
        cmd_msg.pose.orientation.z = msg.pose.orientation.z
        cmd_msg.pose.orientation.w = msg.pose.orientation.w

        cmd_msg.enable_position_controller = True
        cmd_msg.enable_orientation_controller = True

        self.publisher_.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseToRigidBodyPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
