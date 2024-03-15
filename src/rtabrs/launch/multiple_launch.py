from launch import LaunchDescription
from launch_ros.actions import Node

from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir, PythonExpression

def generate_launch_description():
    return LaunchDescription([
        # Launch RealSense Camera Node with specified options
        Node(
            package='realsense2_camera',
            namespace='camera',
            executable='realsense2_camera_node',
            name='realsense2_camera',
            parameters=[{
                'align_depth.enable': True,
                'pointcloud.enable': True,
                # 'enable_sync': True  # d435 should give already synced
            }],
            # remappings=[
            #     ('/camera/depth/image_rect_raw', '/camera/depth_registered/image_raw'),
            #     ('/camera/color/camera_info', '/camera/rgb/camera_info'),
            #     ('/camera/color/image_raw', '/camera/rgb/image_rect_color')
            # ],
            remappings=[
                # ('/camera/depth/image_rect_raw', '/depth/image'), # non-aligned depth: (848x480)
                ('/camera/aligned_depth_to_color/image_raw', '/depth/image'),   # aligned depth to color (640x480)
                ('/camera/color/camera_info', '/rgb/camera_info'),
                ('/camera/color/image_raw', '/rgb/image')
            ],
            output='screen'
        ),

        # RGB-D Odometry Node
        Node(
            package='rtabmap_odom',
            executable='rgbd_odometry',
            name='rgbd_odometry',
            parameters=[{
                'frame_id': 'camera_link',
                'odom_frame_id': 'odom',
                'publish_tf': True,
            }],
            # remappings=[
            #     ('/camera/depth_registered/image_raw', '/camera/depth/image_rect_raw'),
            #     ('/camera/rgb/camera_info', '/camera/color/camera_info'),
            #     ('/camera/rgb/image_rect_color', '/camera/color/image_raw')
            # ],
            output='screen'
        ),

        # RTAB-Map Node
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            parameters=[{
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'subscribe_odom': True,
                'rtabmap_args': '-d',
                'frame_id': 'camera_link',

                # 'approx_sync': False,

                # Add other RTAB-Map specific parameters here
            }],
            arguments=['--delete_db_on_start'],
            output='screen'
        ),

        # # Rtabmap Viz
        # Node(
        #     package='rtabmap_viz',
        #     executable='rtabmap_viz',
        #     name='rtabmap_viz',
        #     output='screen'
        # )

    #     Node(
    #         package='rtabmap_viz', executable='rtabmap_viz', name="rtabmap_viz", output='screen',
    #         parameters=[{
    #             "subscribe_depth": True,
    #             "subscribe_rgbd": True,
    #             "subscribe_rgb": False,
    #             "subscribe_stereo": False,
    #             "subscribe_scan": False,
    #             "subscribe_scan_cloud": False,
    #             "subscribe_user_data": False,
    #             "subscribe_odom_info": False,
    #             "frame_id": LaunchConfiguration('frame_id'),
    #             "odom_frame_id": LaunchConfiguration('odom_frame_id').perform(context),
    #             "wait_for_transform": LaunchConfiguration('wait_for_transform'),
    #             "approx_sync": LaunchConfiguration('approx_sync'),
    #             "queue_size": LaunchConfiguration('queue_size'),
    #             "qos_image": LaunchConfiguration('qos_image'),
    #             "qos_scan": LaunchConfiguration('qos_scan'),
    #             "qos_odom": LaunchConfiguration('qos_odom'),
    #             "qos_camera_info": LaunchConfiguration('qos_camera_info'),
    #             "qos_user_data": LaunchConfiguration('qos_user_data')
    #         }],
    #         remappings=[
    #             ("rgb/image", LaunchConfiguration('rgb_topic_relay')),
    #             ("depth/image", LaunchConfiguration('depth_topic_relay')),
    #             ("rgb/camera_info", LaunchConfiguration('camera_info_topic')),
    #             ("rgbd_image", LaunchConfiguration('rgbd_topic_relay')),
    #             ("left/image_rect", LaunchConfiguration('left_image_topic_relay')),
    #             ("right/image_rect", LaunchConfiguration('right_image_topic_relay')),
    #             ("left/camera_info", LaunchConfiguration('left_camera_info_topic')),
    #             ("right/camera_info", LaunchConfiguration('right_camera_info_topic')),
    #             ("scan", LaunchConfiguration('scan_topic')),
    #             ("scan_cloud", LaunchConfiguration('scan_cloud_topic')),
    #             ("odom", LaunchConfiguration('odom_topic'))],
    #         condition=IfCondition(LaunchConfiguration("rtabmap_viz")),
    #         arguments=[LaunchConfiguration("gui_cfg")],
    #         prefix=LaunchConfiguration('launch_prefix'),
    #         namespace=LaunchConfiguration('namespace')),
    ])
