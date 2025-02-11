import math

import rospy
from geometry_msgs.msg import Vector3
from industrial_reconstruction_msgs.msg import NormalFilterParams
from industrial_reconstruction_msgs.srv import (
    StartReconstruction,
    StartReconstructionRequest,
    StopReconstruction,
    StopReconstructionRequest,
)
from std_msgs.msg import Bool

# reconstruction parameters
start_srv_req = StartReconstructionRequest()
start_srv_req.tracking_frame = 'tcp'
start_srv_req.relative_frame = 'base'
start_srv_req.translation_distance = 0.0
start_srv_req.rotational_distance = 0.0
start_srv_req.live = False
start_srv_req.tsdf_params.voxel_length = 0.001
start_srv_req.tsdf_params.sdf_trunc = 0.002
start_srv_req.tsdf_params.min_box_values = Vector3(x=0.0, y=0.0, z=0.0)
start_srv_req.tsdf_params.max_box_values = Vector3(x=0.0, y=0.0, z=0.0)
start_srv_req.rgbd_params.depth_scale = 1000
start_srv_req.rgbd_params.depth_trunc = 0.5
start_srv_req.rgbd_params.convert_rgb_to_intensity = False

stop_srv_req = StopReconstructionRequest()

stop_srv_req.mesh_filepath = '/home/v/test.ply'



class OsvRecon:
    def __init__(self) -> None:

        self.name = rospy.get_name()
        self.do_sub = rospy.Subscriber('/DO_state', Bool, self.do_callback)
        self.recon_started = False
        rospy.wait_for_service('/start_reconstruction')
        rospy.loginfo(f'{self.name} waiting for /start_reconstruction srv')
        self.start_recon = rospy.ServiceProxy(
            '/start_reconstruction', StartReconstruction
        )
        self.stop_recon = rospy.ServiceProxy('/stop_reconstruction', StopReconstruction)

    def do_callback(self, do_state) -> None:
        
        if not self.recon_started and do_state.data:

            resp = self.start_recon(start_srv_req)
            if resp:
                rospy.loginfo(f'{self.name}: reconstruction started successfully')
                self.recon_started = True
            else:
                rospy.loginfo(f'{self.name}: failed to start reconstruction')

        if self.recon_started and not do_state.data:

            resp = self.stop_recon(stop_srv_req)
            if resp:
                rospy.loginfo(f'{self.name}: reconstruction stopped successfully')
            else:
                rospy.loginfo(f'{self.name}: failed to stop reconstruction')

            self.recon_started = False


if __name__ == '__main__':
    rospy.init_node('osv_recon')
    OsvRecon()
    rospy.spin()
