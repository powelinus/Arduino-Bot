#!/usr/bin/env python3
import sys
import rospy
import moveit_commander

"""
  arduinobot - moveit_interface

  This script uses the MoveIt! API for Python in order to reach a given goal
  and eventually prints the current robot status and informations.

  When triggered, the reach_goal function uses the MoveIt! API for creating a planning request
  that generates a new trajectory that allows the robot to reach its new destination.
  Then, this trajectory is executed via controllers that have been registered and launched with MoveIt!

  Copyright (c) 2021 Antonio Brandi.  All right reserved.
"""


# define the robot group names created with the MoveIt! Setup Assistant
ARM_GROUP_NAME = 'arduinobot_arm'
GRIPPER_GROUP_NAME = 'arduinobot_hand'

class MoveitInterface:

    def __init__(self):
        # Constructor that gets called when a new instance of this class is created
        # it basically inizialize the MoveIt! API that will be used throughout the script
        # initialize the ROS interface with the robot via moveit
        moveit_commander.roscpp_initialize(sys.argv)

        # create a robot commander object that will be the interface with the robot
        self.robot = moveit_commander.RobotCommander()

        # create a move group commander object that will be the interface with the robot joints
        self.arm_move_group = moveit_commander.MoveGroupCommander(ARM_GROUP_NAME)

        # create a move group commander object for the gripper
        self.gripper_move_group = moveit_commander.MoveGroupCommander(GRIPPER_GROUP_NAME)
    
    def reach_goal(self, arm_goal, gripper_goal):
        # This function requires a JointState message as input 
        # with a list of 5 angles in radians for each joint
        # The first 3 elemnt of this list are passed to the arm group 
        # and the last 2 elements are passed to the gripper group.
        # Consider that the last two element of this list have to be the same 
        # as absolute value and with opposite sign

        # Plan and Execute a trajectory that brings the robot from the current pose
        # to the target pose
        self.arm_move_group.go(arm_goal, wait=True)
        self.gripper_move_group.go(gripper_goal, wait=True)

        # Make sure that no residual movement remains
        self.arm_move_group.stop()
        self.gripper_move_group.stop()

    def set_max_velocity(self, scaling_factor):
        # This function sets the the max velocity of the ARM and GRIPPER move group as percentage
        # of the max speed of the joint defined in the joint_linits.yaml file
        # it requires a float number as input >= 0 and <= 1
        self.arm_move_group.set_max_velocity_scaling_factor(scaling_factor)
        self.gripper_move_group.set_max_velocity_scaling_factor(scaling_factor)

    def set_max_acceleration(self, scaling_factor):
        # This function sets the the max acceleration of the ARM and GRIPPER move group as percentage
        # of the max speed of the joint defined in the joint_linits.yaml file
        # it requires a float number as input >= 0 and <= 1
        self.arm_move_group.set_max_acceleration_scaling_factor(scaling_factor)
        self.gripper_move_group.set_max_acceleration_scaling_factor(scaling_factor)
