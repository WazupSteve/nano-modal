"""
Servicer file:
"""

from proto import nano_modal_pb2, nano_modal_pb2_grpc
from server.queue import enqueue_task, get_result


class NanoModalServicer(nano_modal_pb2_grpc.NanoModalServicer):
    # grpc methods take (self, request, context)
    """
    request = proto message object
    context = gRPC connection metadata
    """

    def Invoke(self, request, context):
        task_id = enqueue_task(request.function_pickle, request.args_pickle)
        return nano_modal_pb2.InvokeResponse(task_id=task_id)

    def GetResult(self, request, context):
        task_id = request.task_id
        result_bytes = get_result(task_id)
        if result_bytes is None:
            return nano_modal_pb2.GetResultResponse(error="result pending")
        return nano_modal_pb2.GetResultResponse(result_pickle=result_bytes)
