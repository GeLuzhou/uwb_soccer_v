import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from unitree_go.msg._uwb_state import UwbState
from unitree_go.msg._wireless_controller import WirelessController


class UwbSoccerV(Node):
    
    def __init__(self, use_uwb=False):
        super().__init__('uwb_soccer_v')
        self.use_uwb = use_uwb
        self.cmd_ball_vel = [0, 0, 0, 0]
        self.ball_velcity = Float32MultiArray()
        self.velcity_scale = 0.5
        self.uwb_sub = self.create_subscription(UwbState, '/uwbstate', self.uwb_callback, 10)
        self.rc_sub = self.create_subscription(WirelessController, '/wirelesscontroller', self.rc_callback, 10)
        self.ball_velcity_pub = self.create_publisher(Float32MultiArray, '/ball_velcity', 10)

    def uwb_callback(self, msg):
        if self.use_uwb:
            beta = msg.orientation_est
            # tag 的正方向和狗的正方向初始化一致面向球门里?
            gamma = msg.yaw_est    
            dst = msg.distance_est
            cos_ = math.cos(beta)
            sin_ = math.sin(beta)
            self.cmd_ball_vel = [cos_ * self.velcity_scale, sin_ * self.velcity_scale, 0, 0] 
            self.ball_velcity.data = self.cmd_ball_vel[:2]
            self.get_logger().info(f'lx: {self.cmd_ball_vel[0]}, ly: {self.cmd_ball_vel[1]}')
            self.ball_velcity_pub.publish(self.ball_velcity)

    def rc_callback(self, msg):
        if not self.use_uwb:
            self.cmd_ball_vel = [msg.lx, msg.ly, msg.rx, msg.ry]
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