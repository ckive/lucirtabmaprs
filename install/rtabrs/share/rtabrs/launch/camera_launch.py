from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Launch RealSense Camera Node
        Node(
            package='realsense2_camera',
            namespace='camera',
            executable='realsense2_camera_node',
            name='realsense2_camera',
            parameters=[{'align_depth.enable': True,
                         'pointcloud.enable': True}],
            # remappings=[
            #     ('/camera/depth/image_rect_raw', '/camera/depth_registered/image_raw'),
            #     ('/camera/color/camera_info', '/camera/rgb/camera_info'),
            #     ('/camera/color/image_raw', '/camera/rgb/image_rect_color')
            # ],
            output='screen'
        ),

        # Now launch rtabmap via cmdline since the published names should be correct 

        # # Launch RTAB-Map Node
        # Node(
        #     package='rtabmap_ros',
        #     executable='rtabmap',
        #     name='rtabmap',
        #     parameters=[{'subscribe_depth': True,
        #                  'subscribe_rgb': True,
        #                  'rtabmap_args': '-d'}],
        #     remappings=[
        #         ('/camera/depth_registered/image_raw', '/camera/depth/image_rect_raw'),
        #         ('/camera/rgb/image_rect_color', '/camera/color/image_raw'),
        #         ('/camera/rgb/camera_info', '/camera/color/camera_info')
        #     ],
        #     arguments=['-d', '--approx_sync:=false'],
        #     output='screen'
        # ),

        # Additional RTAB-Map related nodes like odometry can be added here
        # with appropriate parameters and remappings as needed.
    ])
