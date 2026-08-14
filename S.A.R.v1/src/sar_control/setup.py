from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sar_control'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Sparta AI Rover Team',
    maintainer_email='user@todo.todo',
    description='ROS 2 control bridge node for ESP32 hardware interface',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'esp32_bridge_node = sar_control.esp32_bridge_node:main',
            'dummy_esp32_simulator = sar_control.dummy_esp32_simulator:main',
        ],
    },
)
