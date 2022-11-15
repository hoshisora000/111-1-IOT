#!/usr/bin/env python3

import cv2
import os
import numpy as np

from sensor_msgs.msg import Image,PointCloud2
import sensor_msgs.point_cloud2 as pcl2
from std_msgs.msg import Header

import rospy
from cv_bridge import CvBridge
 

DATA_PATH = '/home/duckie/Desktop/kitti/2011_09_26/2011_09_26_drive_0011_sync/'

if __name__ == '__main__':
	frame = 0
	
	rospy.init_node('kitti_node',anonymous=True)
	cam_pub = rospy.Publisher('kitti_cam', Image, queue_size=10)
	pcl_pub = rospy.Publisher('kitti_PointCloud', PointCloud2, queue_size=10)
	rate = rospy.Rate(10)
	
	bridge = CvBridge()
	
	while not rospy.is_shutdown():
		img = cv2.imread(os.path.join(DATA_PATH, 'image_02/data/%010d.png' %frame))
		cam_pub.publish(bridge.cv2_to_imgmsg(img , "bgr8"))
		
		point_cloud = np.fromfile(os.path.join(DATA_PATH, 'velodyne_points/data/%010d.bin'%frame), dtype=np.float32).reshape(-1,4)
		header = Header()
		header.stamp = rospy.Time.now()
		header.frame_id = 'map'
		pcl_pub.publish(pcl2.create_cloud_xyz32(header, point_cloud[:,:3]))
		
		rospy.loginfo("cam_image_published")
		rate.sleep()
		frame += 1
		frame %= 108
