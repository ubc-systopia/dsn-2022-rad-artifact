import os
import sys
import grpc
import time
import argparse

from datetime import datetime
from timeit import default_timer

# Path to this file test_ratracer.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project ratracer) git repo
ratracer_path = os.path.dirname(os.path.dirname(file_path))

# This import is needed if we are not testing using the PyPI (or TestPyPI)
# ratracer package but instead using the ratracer files from source
sys.path.append(ratracer_path)

from ratracer.shared.tracing import Tracer
from ratracer.middlebox.ratracer_server import RATracerServer
from ratracer.lab_computer.ratracer_client import RATracerClient

import ratracer.protos.ratracer_pb2 as ratracer_pb2
import ratracer.protos.ratracer_pb2_grpc as ratracer_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument(
    '-D',
    '--distributed',
    help=
    'Distributed testing. Do not start server. Assume it is started on the provided host and port.',
    action="store_true")
parser.add_argument(
    '-H',
    '--host',
    default='localhost',
    help='Provide server hostname or IP address. Defaults to "localhost".',
    type=str)
parser.add_argument('-P',
                    '--port',
                    default='1337',
                    help='Provide the server port. Defaults to 1337.',
                    type=str)
parser.add_argument(
    '-K',
    '--keysdir',
    default=os.path.join(ratracer_path, "ratracer", "keys", "localhost"),
    help=
    'Provide path to the directory containing the "server.crt" file. Defaults to <project-dir>/ratracer/keys/localhost.',
    type=str)
parser.add_argument(
    '-T',
    '--tracedir',
    default=os.path.join(ratracer_path, "ratracer", "traces"),
    help=
    'Provide path to the trace directory. Defaults to <project-dir>/ratracer/traces/.',
    type=str)
parser.add_argument(
    '-t',
    '--trace_file',
    default='trace.log',
    help=
    'Provide the trace file name. Defaults to "trace.log"',
    type=str)
parser.add_argument(
    '-r',
    '--replay_trace_file',
    default='replayed_trace.log',
    help=
    'Provide the replay trace file name. Defaults to "replayed_trace.log"',
    type=str)

args = parser.parse_args()


class RATracerReplayClient:

    def __init__(self):
        print("RATracerReplayClient: Initialize an insecure GRPC channel")
        channel = grpc.insecure_channel(args.host + ':' + args.port)
        self.stub = ratracer_pb2_grpc.RATracerStub(channel)

    def load_trace(self, tracedir, trace_file):
        print("RATracerReplayClient: Load trace")
        self.trace_array = Tracer.get_trace_array(
            os.path.join(tracedir, trace_file))
        resp = self.stub.LoadTrace(
            ratracer_pb2.LoadTraceReq(trace_file=trace_file))
        return resp.status

    def sim_trace(self, trace_msg):
        msg_type = Tracer.get_msg_type(trace_msg)
        if msg_type == "StaticGetterTraceMsg":
            self.stub.StaticGetter(trace_msg.req)
        elif msg_type == "StaticSetterTraceMsg":
            self.stub.StatiSetter(trace_msg.req)
        elif msg_type == "InitializeTraceMsg":
            self.stub.Initialize(trace_msg.req)
        elif msg_type == "UninitializeTraceMsg":
            self.stub.Uninitialize(trace_msg.req)
        elif msg_type == "GenericMethodTraceMsg":
            self.stub.GenericMethod(trace_msg.req)
        elif msg_type == "GenericGetterTraceMsg":
            self.stub.GenericGetter(trace_msg.req)
        elif msg_type == "GenericSetterTraceMsg":
            self.stub.GenericSetter(trace_msg.req)
        else:
            print("msg_type: %s" % msg_type)
            assert (False)

    def replay_traces(self):
        self.time_profiles = {}
        start_time = default_timer()
        for trace_msg, inter_arrival_time_ms in self.trace_array:
            start = default_timer()
            replay_arrival_time = datetime.now().strftime(
                "%Y:%m:%d:%H:%M:%S.%f")
            self.sim_trace(trace_msg)
            replay_departure_time = datetime.now().strftime(
                "%Y:%m:%d:%H:%M:%S.%f")
            self.time_profiles[trace_msg.req.id] = [
                replay_arrival_time, replay_departure_time
            ]
            end = default_timer()
            sleep_duration_sec = (inter_arrival_time_ms / 1000.0) - (end -
                                                                     start)
            if sleep_duration_sec > 0:
                time.sleep(sleep_duration_sec)

    def update_traces(self, tracedir, new_trace_file):
        tracer = Tracer(tracedir, new_trace_file)
        for trace_msg, inter_arrival_time in self.trace_array:
            for k in range(0, len(trace_msg.req.time_profiles)):
                id = trace_msg.req.time_profiles[k].id
                trace_msg.req.time_profiles[
                    k].arrival_time = self.time_profiles[id][0]
                trace_msg.req.time_profiles[
                    k].departure_time = self.time_profiles[id][1]
            tracer.write_to_file(trace_msg)


if __name__ == "__main__":

    if args.distributed == False:
        ratracer_server = RATracerServer(args.port,
                                         args.tracedir,
                                         args.keysdir,
                                         replay=True)
        ratracer_server.start()

    client = RATracerReplayClient()

    load_status = client.load_trace(args.tracedir, args.trace_file)
    if load_status == False:
        print("Error: Load trace failed!")
        exit(1)

    client.replay_traces()
    client.update_traces(args.tracedir, args.replay_trace_file)
