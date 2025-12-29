"""
Client code : gRPC client
"""

import grpc

from proto import nano_modal_pb2, nano_modal_pb2_grpc


def get_channel(server_address="localhost:50051"):
    """
    goal: create and return gRPC channel to server
    """
    return grpc.insecure_channel(server_address)


def invoke(fxn_bytes, args_bytes, server_address="localhost:50051", timeout=30):
    """
    send function to server for execution and return for result
    return : cloudpickled result
    """
    channel = get_channel(server_address)
    stub = nano_modal_pb2_grpc.NanoModalStub(channel)

    # handling errors
    try:
        # step1: send fxn to execute
        request = nano_modal_pb2.InvokeRequest(function_pickle=fxn_bytes, args_pickle=args_bytes)
        response = stub.Invoke(request, timeout=timeout)

        # step2 : get result
        result_request = nano_modal_pb2.GetResultRequest(task_id=response.task_id)
        result_response = stub.GetResult(result_request, timeout=timeout)

        if result_response.error:
            raise Exception(f"server error:{result_response.error}")
        return result_response.result_pickle

    except grpc.RpcError as e:
        raise Exception(f"gRPC error:{e}")
    finally:
        channel.close()
