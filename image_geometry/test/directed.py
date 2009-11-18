import roslib
PKG = 'image_geometry'
roslib.load_manifest(PKG)
import rostest
import rospy
import cv
import unittest
import sensor_msgs.msg

from image_geometry import PinholeCameraModel, StereoCameraModel

class TestDirected(unittest.TestCase):

    def setUp(self):
        pass

    def test_monocular(self):
        ci = sensor_msgs.msg.CameraInfo()
        ci.width = 640
        ci.height = 480
        print ci
        cam = PinholeCameraModel()
        cam.fromCameraInfo(ci)
        print cam.rectifyPoint((0, 0))

        print cam.project3dToPixel((0,0,0))

    def test_stereo(self):
        lmsg = sensor_msgs.msg.CameraInfo()
        rmsg = sensor_msgs.msg.CameraInfo()
        for m in (lmsg, rmsg):
            m.width = 640
            m.height = 480

        # These parameters taken from a real camera calibration
        lmsg.D =  [-0.363528858080088, 0.16117037733986861, -8.1109585007538829e-05, -0.00044776712298447841, 0.0]
        lmsg.K =  [430.15433020105519, 0.0, 311.71339830549732, 0.0, 430.60920415473657, 221.06824942698509, 0.0, 0.0, 1.0]
        lmsg.R =  [0.99806560714807102, 0.0068562422224214027, 0.061790256276695904, -0.0067522959054715113, 0.99997541519165112, -0.0018909025066874664, -0.061801701660692349, 0.0014700186639396652, 0.99808736527268516]
        lmsg.P =  [295.53402059708782, 0.0, 285.55760765075684, 0.0, 0.0, 295.53402059708782, 223.29617881774902, 0.0, 0.0, 0.0, 1.0, 0.0]

        rmsg.D =  [-0.3560641041112021, 0.15647260261553159, -0.00016442960757099968, -0.00093175810713916221]
        rmsg.K =  [428.38163131344191, 0.0, 327.95553847249192, 0.0, 428.85728580588329, 217.54828640915309, 0.0, 0.0, 1.0]
        rmsg.R =  [0.9982082576219119, 0.0067433328293516528, 0.059454199832973849, -0.0068433268864187356, 0.99997549128605434, 0.0014784127772287513, -0.059442773257581252, -0.0018826283666309878, 0.99822993965212292]
        rmsg.P =  [295.53402059708782, 0.0, 285.55760765075684, -26.507895206214123, 0.0, 295.53402059708782, 223.29617881774902, 0.0, 0.0, 0.0, 1.0, 0.0]

        cam = StereoCameraModel()
        cam.fromCameraInfo(lmsg, rmsg)

        for x in (16, 320, m.width - 16):
            for y in (16, 240, m.height - 16):
                for d in range(1, 10):
                    pt3d = cam.projectPixelTo3d((x, y), d)
                    ((lx, ly), (rx, ry)) = cam.project3dToPixel(pt3d)
                    self.assertAlmostEqual(y, ly, 3)
                    self.assertAlmostEqual(y, ry, 3)
                    self.assertAlmostEqual(x, lx, 3)
                    self.assertAlmostEqual(x, rx + d, 3)

if __name__ == '__main__':
    if 1:
        rostest.unitrun('image_geometry', 'directed', TestDirected)
    else:
        suite = unittest.TestSuite()
        suite.addTest(TestDirected('test_stereo'))
        unittest.TextTestRunner(verbosity=2).run(suite)
