import os
import sys
import unittest
import argparse

# Path to this file test_niraapad.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))
sys.path.append(niraapad_path)

# Path to the hein_robots git repo (submodule)
hein_robots_path = os.path.join(niraapad_path, "hein_robots")
sys.path.append(hein_robots_path)

# Path to the urx git repo (submodule)
urx_path = os.path.join(niraapad_path, "python-urx")
sys.path.append(urx_path)

# Path to the ftdi_serial git repo (submodule)
ftdi_serial_path = os.path.join(niraapad_path, "ftdi_serial")
sys.path.append(ftdi_serial_path)

from niraapad.shared.utils import *
from niraapad.lab_computer.ur3 import UR3Arm
from niraapad.lab_computer.ftdi_serial import Serial
from niraapad.lab_computer.niraapad_client import NiraapadClient

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
                    default='ispy',
                    help='Provide server hostname or IP address. Defaults to "ispy".',
                    type=str)
parser.add_argument('-P', '--port',
                    default='1337',
                    help='Provide the server port. Defaults to 1337.',
                    type=str)
parser.add_argument('-K', '--keysdir',
                    default= os.path.join(niraapad_path, "niraapad", "keys"),
                    help='Provide path to the directory containing the "server.crt" file. Defaults to <project-dir>/niraapad/keys/.',
                    type=str)
args=parser.parse_args()

class TestClientServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_handshake(self):
        print("Starting NiraapadClientHelper")
        NiraapadClient.start_niraapad_client_helper(args.host, args.port, args.keysdir)        
        NiraapadClient.mo = MO.VIA_MIDDLEBOX
        print("Initializing UR3Arm")
        ur3_arm = UR3Arm(connect=False)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestClientServer('test_simple_handshake'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())