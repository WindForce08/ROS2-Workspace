from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    port_arg = DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0')
    baud_arg = DeclareLaunchArgument('baudrate', default_value='115200')

    return LaunchDescription([
        port_arg,
        baud_arg,
        Node(
            package='sar_control',
            executable='esp32_bridge_node',
            name='esp32_bridge_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('serial_port'),
                'baudrate': LaunchConfiguration('baudrate')
            }]
        )
    ])
