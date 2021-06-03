from datetime import datetime

import os

import niraapad.protos.n9_pb2 as n9_pb2
import niraapad.protos.n9_pb2_grpc as n9_pb2_grpc

class Tracer:

    def __init__(self, trace_path=None):
        self.tracing = True
        self.trace_file = Tracer.get_trace_file(trace_path)
        self.logf = open(self.trace_file, "ab+")

    def write_to_file(self, trace_msg):
        if self.tracing == False: return

        now = datetime.now()
        trace_msg_str = trace_msg.SerializeToString()
        trace_msg_type = (str(type(trace_msg))).split("'")[1].split(".")[-1]

        trace_metadata = n9_pb2.TraceMetadata(
            timestamp=now.strftime("%Y:%m:%d:%H:%M:%S.%f"),
            trace_msg_type=trace_msg_type,
            trace_msg_size=len(trace_msg_str))
        trace_metadata_str = trace_metadata.SerializeToString()

        trace_header = n9_pb2.TraceHeader(
            metadata_size=len(trace_metadata_str))
        trace_header_str = trace_header.SerializeToString()

        self.logf.write(trace_header_str)
        self.logf.write(trace_metadata_str)
        self.logf.write(trace_msg_str)

    def stop_tracing(self):
        self.tracing = False
        self.logf.close()

    @staticmethod
    def get_trace_file(trace_path=None):
        if trace_path == None:
            file_path = os.path.dirname(os.path.abspath(__file__))
            trace_path = file_path + "/../traces/"
        os.makedirs(trace_path, exist_ok=True)
        return trace_path + ("%s.log" % (datetime.now().strftime("%Y%m%d%H%M%S")))



    @staticmethod
    def get_trace_header_str_length():
        trace_header = n9_pb2.TraceHeader(metadata_size=100)
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
                if f.tell() + trace_header_str_length > file_size: break
                trace_header = n9_pb2.TraceHeader()
                trace_header.ParseFromString(f.read(trace_header_str_length))

                # Read the trace metadata next
                trace_metadata_str_length = trace_header.metadata_size
                if f.tell() + trace_metadata_str_length > file_size: break
                trace_metadata = n9_pb2.TraceMetadata()
                trace_metadata.ParseFromString(f.read(trace_metadata_str_length))

                # Read the trace message next
                trace_msg_str_length = trace_metadata.trace_msg_size
                if f.tell() + trace_msg_str_length > file_size: break
                trace_msg = getattr(n9_pb2, trace_metadata.trace_msg_type)()
                trace_msg.ParseFromString(f.read(trace_msg_str_length))

                # Return msg type and msg for this iteration
                yield trace_metadata.trace_msg_type, trace_msg

        except Exception as e:
            print("Exception:", e)

        f.close()


