from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    video_device_arg = DeclareLaunchArgument('video_device', default_value='/dev/video0')

    return LaunchDescription([
        video_device_arg,
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam_node',
            output='screen',
            parameters=[{
                'video_device': LaunchConfiguration('video_device'),
                'image_width': 640,
                'image_height': 480,
                'pixel_format': 'yuyv',
                'camera_frame_id': 'camera_optical_frame',
                'io_method': 'mmap'
            }]
        ),
        Node(
            package='sar_vision',
            executable='ai_vision_node',
            name='ai_vision_node',
            output='screen'
        )
    ])
