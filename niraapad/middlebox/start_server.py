import os
import sys
import signal
import argparse

# Path to this file start_server.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))

# This import is needed if we are not testing using the PyPI (or TestPyPI)
# niraapad package but instead using the niraapad files from source
sys.path.append(niraapad_path)

from niraapad.middlebox.niraapad_server import NiraapadServer

server = None


def signal_handler(signal_received, frame):
    print("Signal %s received, exiting gracefully" % str(signal_received))
    if server != None:
        server.stop()


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-P',
                        '--port',
                        default='1337',
                        help='Provide an unused port. Defaults to 1337.',
                        type=str)
    parser.add_argument(
        '-K',
        '--keysdir',
        default=os.path.join(niraapad_path, "niraapad", "keys", "localhost"),
        help=
        'Provide path to the directory containing the "server.key" and "server.crt" files. Defaults to <project-dir>/niraapad/keys/localhost.',
        type=str)
    parser.add_argument(
        '-T',
        '--tracedir',
        default=os.path.join(niraapad_path, "niraapad", "traces"),
        help=
        'Provide path to the trace directory. Defaults to <project-dir>/niraapad/traces/.',
        type=str)
    parser.add_argument('-S',
                        '--secure',
                        help='Use a secure connection.',
                        action="store_true")
    args = parser.parse_args()

    if args.secure == False:
        args.keysdir = None

    server = NiraapadServer(args.port, args.tracedir, args.keysdir)
    server.start(wait=True)
