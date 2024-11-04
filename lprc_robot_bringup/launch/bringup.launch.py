from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():

    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('lprc_robot_description'), 'launch', 'description.launch.py']
    )

    laser_launch_path = PathJoinSubstitution(
        [FindPackageShare('sllidar_ros2'), 'launch', 'sllidar_a1_launch.py']
    )

    odom_launch_path = PathJoinSubstitution(
        [FindPackageShare('rf2o_laser_odometry'), 'launch', 'rf2o_laser_odometry.launch.py']
    )

    slam_launch_path = PathJoinSubstitution(
        [FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py']
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path)
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(laser_launch_path)
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(odom_launch_path),
            launch_arguments={
                'laser_scan_topic': '/scan',
                'odom_topic': '/scan_odom',
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch_path),
            launch_arguments={
                'odom_topic': '/scan_odom',
                'scan_topic': '/scan',
            }.items()
        )
    ])
