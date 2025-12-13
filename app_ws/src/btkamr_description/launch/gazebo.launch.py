import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess

PKG_NAME: str = "btkamr_description"



def generate_launch_description():
    pkg_share = get_package_share_directory(PKG_NAME)
    urdf_path = os.path.join(pkg_share, "urdf", "main.urdf.xacro")
    gz_bridge_yaml = os.path.join(pkg_share, "config", "gz_bridge.yaml")

    robot_desc = ParameterValue(Command(["xacro ", urdf_path]), value_type=str) # boşluk önemli xacro' '

    return LaunchDescription([
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
        # ExecuteProcess(
        #     cmd=['gz', 'sim', '-v4', 'empty.sdf'],
        #     output='screen'
        # ),
        Node(
            package='ros_gz_sim',
            executable='create',
            parameters=[{'topic': 'robot_description'}],
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_desc}]
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': gz_bridge_yaml}],
        ),
        Node(
            package="rviz2",
            executable="rviz2"
        ),
    ])