import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='aroc_truck_description').find('aroc_truck_description')
    #default_model_path = os.path.join(pkg_share, 'models/aroc_truck/model.sdf')
    default_model_path = os.path.join(pkg_share, 'src/description/aroc_truck_description.urdf')
    world_file_name = 'turtlebot.world'
    world = os.path.join(pkg_share, 'world', world_file_name)

    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'aroc_truck', '-topic', 'robot_description',
        ],
        output='screen'
    )

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'source_list': ['joint_states']
        }],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )

    return launch.LaunchDescription([
                launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='Flag to enable joint_state_publisher_gui'),
                launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                                description='Absolute path to robot urdf file'),

        robot_state_publisher_node,          
        joint_state_publisher_node,
        spawn_entity,
        
    ])
