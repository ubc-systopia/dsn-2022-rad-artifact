import os
import sys
import signal
import argparse

# Path to this file start_server.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project ratracer) git repo
ratracer_path = os.path.dirname(os.path.dirname(file_path))

# This import is needed if we are not testing using the PyPI (or TestPyPI)
# ratracer package but instead using the ratracer files from source
sys.path.append(ratracer_path)

import ratracer.backends
from ratracer.middlebox.ratracer_server import RATracerServer

server = None


def signal_handler(signal_received, frame):
    print("Signal %s received, exiting gracefully" % str(signal_received))
    if server != None:
        server.stop()


parser = argparse.ArgumentParser()
parser.add_argument('-P',
                    '--port',
                    default='1337',
                    help='Provide an unused port. Defaults to 1337.',
                    type=str)
parser.add_argument(
    '-K',
    '--keysdir',
    default=os.path.join(ratracer_path, "ratracer", "keys", "localhost"),
    help=
    'Provide path to the directory containing the "server.key" and "server.crt" files. Defaults to <project-dir>/ratracer/keys/localhost.',
    type=str)
parser.add_argument(
    '-T',
    '--tracedir',
    default=os.path.join(ratracer_path, "ratracer", "traces"),
    help=
    'Provide path to the trace directory. Defaults to <project-dir>/ratracer/traces/.',
    type=str)
parser.add_argument('-S',
                    '--secure',
                    help='Use a secure connection.',
                    action="store_true")
parser.add_argument('-R',
                    '--replay',
                    help='Start replay server instead of the regular server.',
                    action="store_true")
args = parser.parse_args()

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    if args.secure == False:
        args.keysdir = None

    server = RATracerServer(args.port, args.tracedir, args.keysdir, args.replay)
    server.start(wait=True)
