"""
Client code : gRPC client
1)Dial the server
2)Send the function
3)Wait for result
"""

import time

import grpc

from proto import nano_modal_pb2, nano_modal_pb2_grpc

from .config import get_server_address


def get_channel(server_address=None):
    """
    goal: create and return gRPC channel to server
    """
    # create insecure connection to server_address ( no ssl connection )
    return grpc.insecure_channel(server_address)


def invoke(fxn_bytes, args_bytes, server_address=None, timeout=120):
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

        # step2 : get result (with polling)
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise Exception("Task timed out")

            result_request = nano_modal_pb2.GetResultRequest(task_id=response.task_id)
            # short timeout for individual gRPC call
            result_response = stub.GetResult(result_request, timeout=10)

            # server returns error
            if result_response.error:
                if result_response.error == "result pending":
                    time.sleep(0.5)  # Wait before polling again
                    continue
                raise Exception(f"server error: {result_response.error}")

            return result_response.result_pickle

    # server is down: grpc error
    except grpc.RpcError as e:
        raise Exception(f"gRPC error: {e}")
    # closing the channel
    finally:
        channel.close()


def wait_for_result(task_id, server_address=None, timeout=120):
    """Goal: Poll the server until a specific task_id has a result."""
    if server_address is None:
        server_address = get_server_address()
    channel = get_channel(server_address)
    stub = nano_modal_pb2_grpc.NanoModalStub(channel)

    try:
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise Exception("Task timed out")
            result_request = nano_modal_pb2.GetResultRequest(task_id=task_id)
            result_response = stub.GetResult(result_request, timeout=10)
            if result_response.error:
                if result_response.error == "result pending":
                    time.sleep(0.5)  # Wait before asking again
                    continue
                raise Exception(f"server error: {result_response.error}")
            return result_response.result_pickle
    finally:
        channel.close()


def invoke_many(fn_bytes, args_pickles, server_address=None):
    """goal: send multiple args to server at once"""
    if server_address is None:
        server_address = get_server_address()
    channel = get_channel(server_address)
    stub = nano_modal_pb2_grpc.NanoModalStub(channel)
    try:
        request = nano_modal_pb2.InvokeManyRequest(
            function_pickle=fn_bytes, args_pickles=args_pickles
        )
        response = stub.InvokeMany(request)
        return response.task_ids
    finally:
        channel.close()
