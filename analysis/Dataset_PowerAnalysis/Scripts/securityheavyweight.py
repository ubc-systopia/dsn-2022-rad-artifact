import csv
import datetime
from pathlib import Path

from hein_robots.universal_robots.ur3 import UR3Arm
from hein_robots.universal_robots.urscript_sequence import URScriptSequence


def write_dict_to_csv(time_stmp, exp_name, command):
    field_names = ['TIME', 'EXP_NAME', 'COMMAND']
    # Dictionary
    dict = {'TIME': time_stmp, 'EXP_NAME': exp_name, 'COMMAND': command}
    # Open your CSV file in append mode
    # Create a file object for this file
    with open('event_1lb.csv', 'a') as f_object:
        # Pass the file object and a list
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)

        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(dict)

        # Close the file object
        f_object.close()

def movements():
    ur =  UR3Arm('192.168.254.88')
    quantos_sequence_file = str(Path(r'C:\Users\User\PycharmProjects\automated_solubility_h1\ur\configuration\sequences\securityheavyweight.script'))

    quantos_sequence = URScriptSequence(quantos_sequence_file)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='ur.open_gripper(0)')
    ur.open_gripper(0)

    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_joints(quantos_sequence.jointsWaypoint_1, velocity=30)')
    ur.move_joints(quantos_sequence.joints['Waypoint_1'], velocity=30)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_to_location(quantos_sequenceWaypoint_2, velocity=80)')
    ur.move_to_location(quantos_sequence['Waypoint_2'], velocity=80)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='ur.open_gripper(0.30)')
    ur.open_gripper(0.30)

    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_to_location(quantos_sequenceWaypoint_1, velocity=80)')
    ur.move_to_location(quantos_sequence['Waypoint_1'], velocity=80)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_joints(quantos_sequence.jointsWaypoint_5, velocity=30)')
    ur.move_joints(quantos_sequence.joints['Waypoint_5'], velocity=30)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_joints(quantos_sequence.jointsWaypoint_6, velocity=30)')
    ur.move_joints(quantos_sequence.joints['Waypoint_6'], velocity=30)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_joints(quantos_sequence.jointsWaypoint_1, velocity=30)')
    ur.move_joints(quantos_sequence.joints['Waypoint_1'], velocity=30)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_to_location(quantos_sequenceWaypoint_2, velocity=100)')
    ur.move_to_location(quantos_sequence['Waypoint_2'], velocity=100)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='ur.open_gripper(0)')
    ur.open_gripper(0)
    write_dict_to_csv(time_stmp=datetime.datetime.now(), exp_name='2lbs',
                      command='    ur.move_to_location(quantos_sequenceWaypoint_1, velocity=80)')
    ur.move_to_location(quantos_sequence['Waypoint_1'], velocity=80)

if __name__ == '__main__':
    for i in range(10):
        movements()