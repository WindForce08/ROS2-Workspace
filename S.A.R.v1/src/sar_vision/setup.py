from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sar_vision'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'opencv-python'],
    zip_safe=True,
    maintainer='Sparta AI Rover Team',
    maintainer_email='user@todo.todo',
    description='USB Webcam and AI Vision processing node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ai_vision_node = sar_vision.ai_vision_node:main',
        ],
    },
)
