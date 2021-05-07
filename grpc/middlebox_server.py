mport grpc
import middlebox_pb2
import middlebox_pb2_grpc

DeviceWriteHandler = Callable[[int, 'Device'], None]

class MiddleboxServicer(middlebox_pb2_grpc.MiddleboxServicer):
    """Provides methods that implement functionality of middlebox server."""

    def __init__(self):
        pass

    def ListDevices(self, request, context):
        # TODO
        return response

    def ListDevicePorts(self, request, context):
        # TODO
        return response

    def ListDeviceSerials(self, request, context):
        # TODO
        return response

    def Initialize(self, request, context):
        # TODO
        return response

    def Connect(self, request, context):
        # TODO
        return response

    def Disconnect(self, request, context):
        # TODO
        return response

    def SetParameters(self, request, context):
        # TODO
        return response

    def UpdateTimeouts(self, request, context):
        # TODO
        return response

    def Info(self, request, context):
        # TODO
        return response

    def SerialNumber(self, request, context):
        # TODO
        return response

    def Read(self, request, context):
        # TODO
        return response

    def ReadLine(self, request, context):
        # TODO
        return response

    def Write(self, request, context):
        # TODO
        return response

    def Request(self, request, context):
        # TODO
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    middlebox_pb2_grpc.add_MiddleboxServicer_to_server(MiddleboxServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == ' __main__':
    serve()
