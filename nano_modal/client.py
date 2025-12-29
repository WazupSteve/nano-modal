"""
Client code : gRPC client
1)Dial the server
2)Send the function
3)Wait for result
"""

import grpc

from proto import nano_modal_pb2, nano_modal_pb2_grpc

from .config import get_server_address


def get_channel(server_address=None):
    """
    goal: create and return gRPC channel to server
    """
    # create insecure connection to server_address ( no ssl connection )
    return grpc.insecure_channel(server_address)


def invoke(fxn_bytes, args_bytes, server_address=None, timeout=30):
    """
    send function to server for execution and return for result
    return : cloudpickled result
    """
    if server_address is None:
        server_address = get_server_address()
    channel = get_channel(server_address)
    # this gives us the object which has .Invoke() and .GetResult() methods
    stub = nano_modal_pb2_grpc.NanoModalStub(channel)

    # handling errors
    try:
        # step1: send fxn to execute
        request = nano_modal_pb2.InvokeRequest(function_pickle=fxn_bytes, args_pickle=args_bytes)
        response = stub.Invoke(request, timeout=timeout)

        # step2 : get result
        result_request = nano_modal_pb2.GetResultRequest(task_id=response.task_id)
        result_response = stub.GetResult(result_request, timeout=timeout)

        # server returns error
        if result_response.error:
            raise Exception(f"server error:{result_response.error}")
        return result_response.result_pickle

    # server is down: grpc error
    except grpc.RpcError as e:
        raise Exception(f"gRPC error:{e}")
    # closing the channel
    finally:
        channel.close()
