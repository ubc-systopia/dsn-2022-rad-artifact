import os
import sys
import argparse

# Path to this file start_server.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))

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
    parser.add_argument('-S', '--secure',
                        help='Use a secure connection.',
                        action="store_true")
    args=parser.parse_args()

    if args.secure == False:
        args.keysdir = None

    niraapad_server = NiraapadServer(args.port, args.tracedir, args.keysdir)
    niraapad_server.start(wait=True)
