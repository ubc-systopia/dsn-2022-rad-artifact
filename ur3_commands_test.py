import sys
from hein_robots.universal_robots.ur3 import UR3Arm
from hein_robots.robotics import Location
from datetime import datetime
import math


arm = UR3Arm('192.168.217.128', gripper_base_port = 30002)
print ("robot created")

connected=arm.connected
print("arm is connected!", connected)

StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
count= arm.joint_count
print("count StartTime is: ", StartTime)
print ("joint_count is: ", count) 

StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
Velocity=arm.default_joint_velocity
print("velocity StartTime is: ", StartTime)
print ("velocity is: ", Velocity)

StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
Acceleration=arm.acceleration
print("acceleration StartTime is: ", StartTime)
print ("acceleration is: ", Acceleration)

StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
position = arm.pose
print("pose StartTime is: ", StartTime)
print ("printing first position")
print(position)


StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
location=arm.location
print("location StartTime is: ", StartTime)
print ("printing first location..")
print (location)

targets = [ Location(x=-170, y=100, z=50),
            Location(x=-270, y=110, z=150),
              ]

for target in targets:
    StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    arm.move_to_location(target)
    print("move_to_location StartTime is: ", StartTime)
    print ("printing next location..")
    print(target)

StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
position = arm.pose
print("position StartTime is: ", StartTime)
print ("printing next position")
print(position)
angles = list(map(lambda i: math.degrees(i), position.orient.to_euler('xyz')))
print ("printing angles and locations..")
print (angles)
location = arm.location
print(location)

targets = [
            ([-97.35, 108.65, 79.33, 19.45, 131.58, 39.06], Location(-.1, -.322, .449, -80, 31, -140)),
            ([-97.35, 109.03, 181.52, 22.03, 131.58, 19.06], Location(-.1, -.322, .439, -80, 30.99, -140)),
        ]

for joints, location in targets:
    StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    arm.move_joints(joints)
    print("move_joints StartTime is: ", StartTime)
    
      
StartTime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
JPosition=arm.joint_positions
print("joint_position StartTime is: ", StartTime)
print ("printing joint position")
print(JPosition)   

arm.disconnect()