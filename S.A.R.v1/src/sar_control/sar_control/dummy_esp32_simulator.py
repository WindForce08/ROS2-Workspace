#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState, Imu
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class DummyESP32Simulator(Node):
    def __init__(self):
        super().__init__('dummy_esp32_simulator')
        self.get_logger().info("Dummy ESP32 Simulator Node Started!")
        
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.linear_x = 0.0
        self.angular_z = 0.0

        self.arm_joints = [0.0] * 6
        self.gripper_pos = 0.0

        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.arm_sub = self.create_subscription(JointState, '/arm/joint_commands', self.arm_callback, 10)

        self.last_time = self.get_clock().now()
        self.create_timer(0.05, self.update)

    def cmd_callback(self, msg: Twist):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def arm_callback(self, msg: JointState):
        if len(msg.position) >= 6:
            self.arm_joints = list(msg.position[:6])
        if len(msg.position) >= 7:
            self.gripper_pos = msg.position[6]

    def update(self):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        if dt <= 0:
            return
        self.last_time = now

        # Integrate pose
        delta_x = self.linear_x * math.cos(self.th) * dt
        delta_y = self.linear_x * math.sin(self.th) * dt
        delta_th = self.angular_z * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        qz = math.sin(self.th / 2.0)
        qw = math.cos(self.th / 2.0)

        stamp = now.to_msg()

        # Publish TF
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t)

        # Publish Odometry
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = self.linear_x
        odom.twist.twist.angular.z = self.angular_z
        self.odom_pub.publish(odom)

        # Publish Joint States
        js = JointState()
        js.header.stamp = stamp
        js.name = [
            'front_left_wheel_joint', 'front_right_wheel_joint',
            'rear_left_wheel_joint', 'rear_right_wheel_joint',
            'arm_joint1', 'arm_joint2', 'arm_joint3',
            'arm_joint4', 'arm_joint5', 'arm_joint6',
            'gripper_joint'
        ]
        w_rot = self.x / 0.045
        js.position = [
            w_rot, w_rot, w_rot, w_rot,
            self.arm_joints[0], self.arm_joints[1], self.arm_joints[2],
            self.arm_joints[3], self.arm_joints[4], self.arm_joints[5],
            self.gripper_pos
        ]
        self.joint_pub.publish(js)

        # Publish IMU
        imu = Imu()
        imu.header.stamp = stamp
        imu.header.frame_id = 'imu_link'
        imu.linear_acceleration.z = 9.81
        imu.angular_velocity.z = self.angular_z
        self.imu_pub.publish(imu)

def main(args=None):
    rclpy.init(args=args)
    node = DummyESP32Simulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
