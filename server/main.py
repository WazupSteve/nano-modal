"""
1) Create gRPC server
2) add your servicer
3) bind to port
4) start serving
"""

from concurrent import futures

import grpc

from proto import nano_modal_pb2_grpc

from .service import NanoModalServicer


def serve():
    # create a server that can handle multiple requests at once
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # add servicer
    #
    nano_modal_pb2_grpc.add_NanoModalServicer_to_server(NanoModalServicer(), server)

    # binding to port
    # listen on all network interfaces (insecure port= no SSL/TLS)
    server.add_insecure_port("[::]:50051")
    print("server starting on port 50051..")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
