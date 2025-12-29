"""
Servicer file:
1) Receive function request from client
2) Execute them directly ( todo : redis integration )
3) Store and return result
"""

import uuid

from proto import nano_modal_pb2, nano_modal_pb2_grpc


class NanoModalServicer(nano_modal_pb2_grpc.NanoModalServicer):
    # grpc methods take (self, request, context)
    """
    request = proto message object
    context = gRPC connection metadata
    """

    def __init__(self):
        self.results = {}  # task_id -> result_bytes

    def Invoke(self, request, context):
        task_id = str(uuid.uuid4())  # generate unique id
        try:
            from worker.docker_runner import execute_in_docker

            result_bytes = execute_in_docker(request.function_pickle, request.args_bytes)
            self.results[task_id] = result_bytes
        except Exception:
            self.results[task_id] = None
            # just storing error for now

        # return task id
        return nano_modal_pb2.InvokeResponse(task_id=task_id)

    def GetResult(self, request, context):
        # need to add in memory dictionary for result( REDIS later)
        task_id = request.task_id
        if task_id in self.results:
            result_bytes = self.results[task_id]
            if result_bytes is not None:
                return nano_modal_pb2.GetResultResponse(result_pickle=result_bytes)
            else:
                return nano_modal_pb2.GetResultResponse(error="Function execution has failed")

        else:
            return nano_modal_pb2.GetResultResponse(error="task not found")
