import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    desc_share = get_package_share_directory('sar_description')
    xacro_file = os.path.join(desc_share, 'urdf', 'rover.urdf.xacro')
    rviz_config_file = os.path.join(desc_share, 'rviz', 'rover.rviz')

    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Launch Arguments
    use_sim_arg = DeclareLaunchArgument('use_sim', default_value='false', description='Use simulated ESP32 node')
    serial_port_arg = DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0', description='Serial port for ESP32')
    enable_camera_arg = DeclareLaunchArgument('enable_camera', default_value='false', description='Launch USB camera and AI vision node')
    enable_rviz_arg = DeclareLaunchArgument('enable_rviz', default_value='true', description='Launch RViz2 visualization')

    # Robot State Publisher
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    # Real Hardware ESP32 Bridge Node
    esp32_hardware_node = Node(
        condition=UnlessCondition(LaunchConfiguration('use_sim')),
        package='sar_control',
        executable='esp32_bridge_node',
        name='esp32_bridge_node',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('serial_port'),
            'baudrate': 115200
        }]
    )

    # Simulated ESP32 Bridge Node
    esp32_sim_node = Node(
        condition=IfCondition(LaunchConfiguration('use_sim')),
        package='sar_control',
        executable='dummy_esp32_simulator',
        name='dummy_esp32_simulator',
        output='screen'
    )

    # Camera & Vision Launch
    vision_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('sar_vision'), 'launch', 'camera_ai.launch.py')
        ),
        condition=IfCondition(LaunchConfiguration('enable_camera'))
    )

    # RViz2 Node
    rviz_node = Node(
        condition=IfCondition(LaunchConfiguration('enable_rviz')),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        use_sim_arg,
        serial_port_arg,
        enable_camera_arg,
        enable_rviz_arg,
        robot_state_pub,
        esp32_hardware_node,
        esp32_sim_node,
        vision_launch,
        rviz_node
    ])
