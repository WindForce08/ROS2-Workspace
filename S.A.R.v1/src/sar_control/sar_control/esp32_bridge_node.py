#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState, Imu
from tf2_ros import TransformBroadcaster
import serial
import json
import math
import time

class ESP32BridgeNode(Node):
    def __init__(self):
        super().__init__('esp32_bridge_node')
        
        # Parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_track', 0.22)    # Distance between left & right wheels (m)
        self.declare_parameter('wheel_radius', 0.045)  # Wheel radius (m)
        self.declare_parameter('encoder_cpr', 1344.0)  # Pulses per revolution

        self.port = self.get_parameter('port').value
        self.baudrate = self.get_parameter('baudrate').value
        self.track_width = self.get_parameter('wheel_track').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.encoder_cpr = self.get_parameter('encoder_cpr').value

        # Serial Connection
        self.serial_conn = None
        self.connect_serial()

        # State Variables for Odometry
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.prev_enc_l = None
        self.prev_enc_r = None
        self.last_time = self.get_clock().now()

        # Arm Joints State (6-DOF + Gripper)
        self.arm_joints = [0.0] * 6
        self.gripper_pos = 0.0
        self.target_cmd_l = 0.0
        self.target_cmd_r = 0.0

        # ROS 2 Publishers & Subscribers
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.arm_sub = self.create_subscription(JointState, '/arm/joint_commands', self.arm_cmd_callback, 10)

        # Timers
        self.create_timer(0.05, self.update_loop)  # 20 Hz loop

        self.get_logger().info(f"ESP32 Bridge Node initialized on port {self.port}")

    def connect_serial(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=0.05)
            self.get_logger().info(f"Successfully connected to ESP32 on {self.port} at {self.baudrate} baud.")
        except Exception as e:
            self.get_logger().warn(f"Could not open serial port {self.port}: {e}. Operating in disconnected mode.")
            self.serial_conn = None

    def cmd_vel_callback(self, msg: Twist):
        # 2-Motor 4WD Differential Drive Kinematics
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Calculate target wheel linear velocities (m/s)
        self.target_cmd_l = linear_x - (angular_z * self.track_width / 2.0)
        self.target_cmd_r = linear_x + (angular_z * self.track_width / 2.0)

    def arm_cmd_callback(self, msg: JointState):
        if len(msg.position) >= 6:
            self.arm_joints = list(msg.position[:6])
        if len(msg.position) >= 7:
            self.gripper_pos = msg.position[6]

    def update_loop(self):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        if dt <= 0:
            return
        self.last_time = now

        # Send command packet to ESP32
        if self.serial_conn and self.serial_conn.is_open:
            try:
                cmd_packet = {
                    "cL": round(self.target_cmd_l, 3),
                    "cR": round(self.target_cmd_r, 3),
                    "arm": [round(a, 3) for a in self.arm_joints],
                    "grip": round(self.gripper_pos, 3)
                }
                self.serial_conn.write((json.dumps(cmd_packet) + '\n').encode('utf-8'))

                # Read response packet from ESP32
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith('{') and line.endswith('}'):
                        data = json.loads(line)
                        self.process_esp32_data(data, dt)
            except Exception as e:
                self.get_logger().error(f"Serial communication error: {e}")
                self.serial_conn = None
        else:
            # Reconnect attempt periodically
            if int(now.nanoseconds / 1e9) % 5 == 0:
                self.connect_serial()

        # Always publish joint states & odometry
        self.publish_joint_states()
        self.publish_odometry(self.target_cmd_l, self.target_cmd_r, dt)

    def process_esp32_data(self, data, dt):
        enc_l = data.get('encL', 0)
        enc_r = data.get('encR', 0)

        if self.prev_enc_l is not None and self.prev_enc_r is not None:
            d_l = (enc_l - self.prev_enc_l) * (2.0 * math.pi * self.wheel_radius / self.encoder_cpr)
            d_r = (enc_r - self.prev_enc_r) * (2.0 * math.pi * self.wheel_radius / self.encoder_cpr)
            
            v_l = d_l / dt
            v_r = d_r / dt
            
            self.publish_odometry(v_l, v_r, dt)

        self.prev_enc_l = enc_l
        self.prev_enc_r = enc_r

        # IMU Data if available
        if 'ax' in data:
            imu_msg = Imu()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'imu_link'
            imu_msg.linear_acceleration.x = float(data.get('ax', 0.0))
            imu_msg.linear_acceleration.y = float(data.get('ay', 0.0))
            imu_msg.linear_acceleration.z = float(data.get('az', 9.81))
            imu_msg.angular_velocity.x = float(data.get('gx', 0.0))
            imu_msg.angular_velocity.y = float(data.get('gy', 0.0))
            imu_msg.angular_velocity.z = float(data.get('gz', 0.0))
            self.imu_pub.publish(imu_msg)

    def publish_odometry(self, v_l, v_r, dt):
        v = (v_r + v_l) / 2.0
        w = (v_r - v_l) / self.track_width

        delta_x = v * math.cos(self.th) * dt
        delta_y = v * math.sin(self.th) * dt
        delta_th = w * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        # Quaternion calculation for yaw
        qz = math.sin(self.th / 2.0)
        qw = math.cos(self.th / 2.0)

        stamp = self.get_clock().now().to_msg()

        # TF Broadcast
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t)

        # Odometry Message
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = w

        self.odom_pub.publish(odom)

    def publish_joint_states(self):
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [
            'front_left_wheel_joint', 'front_right_wheel_joint',
            'rear_left_wheel_joint', 'rear_right_wheel_joint',
            'arm_joint1', 'arm_joint2', 'arm_joint3',
            'arm_joint4', 'arm_joint5', 'arm_joint6',
            'gripper_joint'
        ]
        
        # Wheel rotations (simulated or encoder integrated)
        wheel_pos = (self.x / self.wheel_radius)
        
        js.position = [
            wheel_pos, wheel_pos, wheel_pos, wheel_pos,
            self.arm_joints[0], self.arm_joints[1], self.arm_joints[2],
            self.arm_joints[3], self.arm_joints[4], self.arm_joints[5],
            self.gripper_pos
        ]
        self.joint_state_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = ESP32BridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
