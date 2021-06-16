import os
import sys
import argparse

# Path to this file start_server.py
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

from niraapad.middlebox.niraapad_server import NiraapadServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--port',
                        default='1337',
                        help='Provide an unused port. Defaults to 1337.',
                        type=str)
    parser.add_argument('-K', '--keysdir',
                        default= os.path.join(niraapad_path, "niraapad", "keys", "localhost"),
                        help='Provide path to the directory containing the "server.key" and "server.crt" files. Defaults to <project-dir>/niraapad/keys/localhost.',
                        type=str)
    parser.add_argument('-T', '--tracedir',
                        default= os.path.join(niraapad_path, "niraapad", "traces"),
                        help='Provide path to the trace directory. Defaults to <project-dir>/niraapad/traces/.',
                        type=str) 
    args=parser.parse_args()

    niraapad_server = NiraapadServer(args.port, args.tracedir, args.keysdir)
    niraapad_server.start(wait=True)