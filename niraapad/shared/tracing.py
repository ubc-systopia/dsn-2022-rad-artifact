from datetime import datetime

import os

import niraapad.shared.utils as utils
import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc


class Tracer:

    trace_file_counter = 1
    ignored_msg_types = [
        "StartServerTraceMsg", "DeleteConnectionTraceMsg",
        "InitializeConnectionTraceMsg", "StopServerTraceMsg"
    ]

    def __init__(self, trace_path=None, trace_file=None):
        if trace_file == None:
            self.trace_path = trace_path
            self.trace_file = Tracer.get_trace_file(self.trace_path)
        else:
            self.trace_file = Tracer.get_trace_file_after_replay(
                trace_path, trace_file)
        self.tracing = True
        self.tracing_day = datetime.now().date().day

    def write_to_file(self, trace_msg):
        if self.tracing == False:
            return

        now = datetime.now()
        today = now.date().day
        if today != self.tracing_day:
            self.trace_file = Tracer.get_trace_file(self.trace_path)
        self.tracing_day = today

        logf = open(self.trace_file, "ab+")

        trace_msg_str = trace_msg.SerializeToString()
        trace_msg_type = (str(type(trace_msg))).split("'")[1].split(".")[-1]

        trace_metadata = niraapad_pb2.TraceMetadata(
            timestamp=now.strftime("%Y:%m:%d:%H:%M:%S.%f"),
            trace_msg_type=trace_msg_type,
            trace_msg_size=len(trace_msg_str))
        trace_metadata_str = trace_metadata.SerializeToString()

        trace_header = niraapad_pb2.TraceHeader(
            metadata_size=len(trace_metadata_str))
        trace_header_str = trace_header.SerializeToString()

        logf.write(trace_header_str)
        logf.write(trace_metadata_str)
        logf.write(trace_msg_str)

        logf.close()

    def stop_tracing(self):
        if self.tracing:
            self.tracing = False

    @staticmethod
    def get_trace_file(trace_path):
        # if trace_path == None:
        #     file_path = os.path.dirname(os.path.abspath(__file__))
        #     trace_path = os.path.join(os.path.dirname(file_path), "traces")
        os.makedirs(trace_path, exist_ok=True)
        trace_file_name = "%s-%s.log" % \
            (datetime.now().strftime("%Y%m%d%H%M%S"), Tracer.trace_file_counter)
        trace_file = os.path.join(trace_path, trace_file_name)
        Tracer.trace_file_counter += 1
        return trace_file

    @staticmethod
    def get_trace_file_after_replay(trace_path, trace_file):
        os.makedirs(trace_path, exist_ok=True)
        trace_file = os.path.join(trace_path, "replayed-" + trace_file)
        Tracer.trace_file_counter += 1
        return trace_file

    @staticmethod
    def get_trace_header_str_length():
        trace_header = niraapad_pb2.TraceHeader(metadata_size=100)
        trace_header_str = trace_header.SerializeToString()
        return len(trace_header_str)

    @staticmethod
    def parse_file(trace_file):
        try:
            f = open(trace_file, "rb")

            # Get the file size (no. of bytes) for termination
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            f.seek(0)

            while True:
                # Read the constant-sized trace header first
                trace_header_str_length = Tracer.get_trace_header_str_length()
                if f.tell() + trace_header_str_length > file_size:
                    break
                trace_header = niraapad_pb2.TraceHeader()
                trace_header.ParseFromString(f.read(trace_header_str_length))

                # Read the trace metadata next
                trace_metadata_str_length = trace_header.metadata_size
                if f.tell() + trace_metadata_str_length > file_size:
                    break
                trace_metadata = niraapad_pb2.TraceMetadata()
                trace_metadata.ParseFromString(
                    f.read(trace_metadata_str_length))

                # Read the trace message next
                trace_msg_str_length = trace_metadata.trace_msg_size
                if f.tell() + trace_msg_str_length > file_size:
                    break
                trace_msg = getattr(niraapad_pb2,
                                    trace_metadata.trace_msg_type)()
                trace_msg.ParseFromString(f.read(trace_msg_str_length))

                # Return msg type and msg for this iteration
                yield trace_metadata.timestamp, trace_metadata.trace_msg_type, trace_msg

            f.close()

        except Exception as e:
            print("Error: parse_file failed with exception %s" % e)

    @staticmethod
    def get_msg_type(trace_msg):
        return (str(type(trace_msg))).split("'")[1].split(".")[-1]

    @staticmethod
    def get_trace_dict(trace_file_path):
        trace_dict = {}
        for timestamp, msg_type, trace_msg in Tracer.parse_file(
                trace_file_path):
            if msg_type in Tracer.ignored_msg_types:
                continue
            trace_dict[trace_msg.req.id] = trace_msg
        return trace_dict

    # @staticmethod
    # def get_trace_array(trace_file_path):
    #     trace_array = []
    #     for timestamp, msg_type, trace_msg in Tracer.parse_file(trace_file_path):
    #         if msg_type in Tracer.ignored_msg_types: continue
    #         trace_array.append(trace_msg)
    #     return trace_array

    @staticmethod
    def get_trace_array(trace_file_path):

        arrival_times = {}
        for timestamp, msg_type, trace_msg in Tracer.parse_file(
                trace_file_path):
            if msg_type in Tracer.ignored_msg_types:
                continue
            for time_profile in trace_msg.req.time_profiles:
                arrival_times[time_profile.id] = time_profile.arrival_time

        trace_array = []
        for timestamp, msg_type, trace_msg in Tracer.parse_file(
                trace_file_path):
            if msg_type in Tracer.ignored_msg_types:
                continue
            trace_array.append(trace_msg)

        inter_arrival_times = {}
        for i in range(0, len(trace_array)):
            try:
                req_id = trace_array[i].req.id
                next_req_id = trace_array[i + 1].req.id
                inter_arrival_times[req_id] = utils.elapsed_time_ms(
                    arrival_times[req_id], arrival_times[next_req_id])
            except Exception as e:
                print(
                    "Error: get_trace_array may have failed with exception %s" %
                    e)
                inter_arrival_times[req_id] = 0
        new_trace_array = []
        for i in range(0, len(trace_array)):
            new_trace_array.append(
                [trace_array[i], inter_arrival_times[trace_array[i].req.id]])

        return new_trace_array
