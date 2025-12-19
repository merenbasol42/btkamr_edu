import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # ============================================================================
    # Paket Yolları
    # ============================================================================
    pkg_share = get_package_share_directory("btkamr_simulate")
    desc_pkg_share = get_package_share_directory("btkamr_description")
    ros_gz_sim_pkg_share = get_package_share_directory("ros_gz_sim")
    
    config_dir = os.path.join(pkg_share, "config")
    worlds_dir = os.path.join(pkg_share, "worlds")
    
    # ============================================================================
    # Dosya Yolları 
    # ============================================================================
    models_path = os.path.join(pkg_share, "models")
    gz_bridge_config_path = os.path.join(config_dir, "gz_bridge.yaml")
    world_path = os.path.join(worlds_dir, "my_world.sdf")
    rviz_config_path = os.path.join(config_dir, "base.rviz")
    urdf_path = os.path.join(desc_pkg_share, "urdf", "main.urdf.xacro")

    # ============================================================================
    # Nodes ve Actions
    # ============================================================================
    # Robot description'ı xacro'dan oluştur
    robot_desc = ParameterValue(
        Command(["xacro ", urdf_path]), 
        value_type=str
    )
          
    
    # Gazebo resource pathi ayarla
    #!!! Modellerimizi görsün diye

    existing_resource_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    if existing_resource_path:
        new_resource_path = models_path + ":" + existing_resource_path
    else:
        new_resource_path = models_path

    set_gz_resource_path_env = SetEnvironmentVariable(
        name = "GZ_SIM_RESOURCE_PATH",
        value = new_resource_path
    )

    # Gazebo Simülasyonu
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": [
                "-v 4 ",            # Verbose level 4
                world_path
            ]
        }.items()
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_desc,
            "use_sim_time": True
        }]
    )
    
    # Gazebo'da Robot Spawn
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        parameters=[{"topic": "robot_description"}]
    )
    
    # ROS-Gazebo Bridge
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{
            "config_file": gz_bridge_config_path,
            "use_sim_time": True
        }]
    )
    
    # RViz (norviz=false ise)
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config_path],
        parameters=[{
            "use_sim_time": True
        }]
    )
    
    # ============================================================================
    # Launch Description
    # ============================================================================
    return LaunchDescription([
        set_gz_resource_path_env,
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        ros_gz_bridge,
        rviz
    ])