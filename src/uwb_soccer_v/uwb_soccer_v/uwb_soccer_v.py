import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from unitree_go.msg._uwb_state import UwbState


class UwbSoccerV(Node):
    
    def __init__(self):
        super().__init__('uwb_soccer_v')
        self.cmd_ball_vel = [0, 0, 0, 0]
        self.ball_velcity = Float32MultiArray()
        self.velcity_scale = 0.5
        self.uwb_sub = self.create_subscription(UwbState, 'uwb_state', self.uwb_callback, 10)
        self.ball_velcity_pub = self.create_publisher(Float32MultiArray, 'ball_velcity', 10)

    def uwb_callback(self, msg):
        beta = msg.orientation_est
        # tag 的正方向和狗的正方向初始化一致面向球门里
        gamma = msg.yaw_est    
        dst = msg.distance_est
        cos_ = math.cos(gamma)
        sin_ = math.sin(gamma)
        self.cmd_ball_vel = [cos_, sin_, 0, 0] * self.velcity_scale
        self.ball_velcity.data = self.cmd_ball_vel[:2]
        self.get_logger().info(f'lx: {self.cmd_ball_vel[0]}, ly: {self.cmd_ball_vel[1]}')
        self.ball_velcity_pub.publish(self.ball_velcity)


def main(args=None):
    rclpy.init(args=args)
    uwb_soccer_v = UwbSoccerV()
    rclpy.spin(uwb_soccer_v)
    uwb_soccer_v.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()