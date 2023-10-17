from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='brokk_gazebo' 
    general_package='brokk'

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_gui = LaunchConfiguration('use_gui')
    rsp = IncludeLaunchDescription(
               PythonLaunchDescriptionSource([os.path.join(
                   get_package_share_directory(general_package),'launch','rsp.launch_brokk.py'
               )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # use_sim_time = LaunchConfiguration('use_sim_time')
    # use_gui = LaunchConfiguration('use_gui')

    # Process the URDF file
    # pkg_path = os.path.join(get_package_share_directory('brokk'))
    # xacro_file = os.path.join(pkg_path,'description','testurdf.urdf.xacro')
    # robot_description_config = xacro.process_file(xacro_file)
    
    # # Create a robot_state_publisher node
    # params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}

    # node_robot_state_publisher = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     output='screen',
    #     parameters=[params]
    # )

    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher'
    # )


    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),    
             )
    
    # gazebo_server = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzserver.launch.py'
    #         ])
    #     ]),
    #     launch_arguments={
    #         'pause': 'true'
    #     }.items()
    # )

    # gazebo_client = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzclient.launch.py'
    #         ])
    #     ])
    # )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'testurdf'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),

        DeclareLaunchArgument(
        'use_ros2_control',
        default_value='true',
        description='Use ros2_control if true'),

        rsp,
        # node_robot_state_publisher,
        # joint_state_publisher_node,
        spawn_entity,
        gazebo,
        # gazebo_server,
        # gazebo_client,
    ])