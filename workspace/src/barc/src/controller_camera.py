#!/usr/bin/env python
import roslib
import sys
import rospy
from barc.msg import LineData, ECU
from numpy import pi

# This script reads the output from the top_down_view.py node and computes the actuator messages appropriate to follow a white line on the ground.
Kp_angle = 1.0
Kp_disp = 3.5
ang_o = 0

class LineFollowController:

    def __init__(self):

        self.subscriber = rospy.Subscriber("/line/ang_disp", LineData, self.callback_data)
        self.publisher = rospy.Publisher("ecu", ECU, queue_size=1)
        self.angle = 0.0
        self.displacement = 0.0

    def callback_data(self, data):
        global ang_o
        global ang_n
        ang_o = self.angle
        # Do all computation from the incoming message to the output message here
        self.angle = data.angle
        self.displacement = data.horizontal_displacement

        if self.angle > 0:
            self.angle = self.angle - pi

        ang_ctrl = Kp_angle*(self.angle) + Kp_disp * (self.displacement)

        self.publisher.publish(ECU(6.5, ang_ctrl + pi))


def main(args):    

    rospy.init_node("controller_camera") #initialize ros node
    rate = rospy.Rate(30)

    controller = LineFollowController()

    rospy.spin()
    rate.sleep()

if __name__ == '__main__':
    try:
        main(sys.argv)
    except rospy.ROSInterruptException:
        pass
