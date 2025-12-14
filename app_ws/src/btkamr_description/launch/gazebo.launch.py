import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

PKG_NAME: str = "btkamr_description"


def generate_launch_description():

    pkg_share = get_package_share_directory(PKG_NAME)
    urdf_path = os.path.join(pkg_share, "urdf", "main.urdf.xacro")
    gz_bridge_yaml = os.path.join(pkg_share, "config", "gz_bridge.yaml")

    robot_desc = ParameterValue(Command(["xacro ", urdf_path]), value_type=str) # boşluk önemli xacro' '

    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('ros_gz_sim'),
                    'launch',
                    'gz_sim.launch.py'
                )
            ),
            launch_arguments={
                'gz_args': ['-r -v 4 ', "empty.sdf"] #cli'dan çalışırken de verebileceğimiz argümanlar
            }.items()
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            parameters=[{'topic': 'robot_description'}],
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{
                "robot_description": robot_desc,
                'use_sim_time': use_sim_time
            }]
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': gz_bridge_yaml}],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            parameters=[{
                'use_sim_time': use_sim_time
            }]
        ),
    ])