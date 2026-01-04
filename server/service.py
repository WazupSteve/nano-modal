"""
Servicer file:
streaming rpc on the server side
"""

import time

from proto import nano_modal_pb2, nano_modal_pb2_grpc
from server.queue import enqueue_task, get_result


class NanoModalServicer(nano_modal_pb2_grpc.NanoModalServicer):
    # grpc methods take (self, request, context)
    """
    request = proto message object
    context = gRPC connection metadata
    """

    def Invoke(self, request, context):
        image_config = None
        if request.HasField("image_config"):
            image_config = {
                "base_image": request.image_config.base_image,
                "pip_packages": list(request.image_config.pip_packages),
                "commands": list(request.image_config.commands),
            }
        task_id = enqueue_task(
            request.function_pickle, request.args_pickle, image_config=image_config
        )
        return nano_modal_pb2.InvokeResponse(task_id=task_id)

    def InvokeMany(self, request, context):
        image_config = None
        if request.HasField("image_config"):
            image_config = {
                "base_image": request.image_config.base_image,
                "pip_packages": list(request.image_config.pip_packages),
                "commands": list(request.image_config.commands),
            }
        task_ids = []  # list
        for args_bytes in request.args_pickles:
            tid = enqueue_task(request.function_pickle, args_bytes, image_config=image_config)
            task_ids.append(tid)
        return nano_modal_pb2.InvokeManyResponse(task_ids=task_ids)

    def InvokeManyStream(self, request, context):
        """
        Streaming RPC:
        enqueue all the tasks, then yield results as they complete
        InvokeManyStream is a Generator function.
        each "yield" sends a message to the client ( yield instead of return )
        connection stays open untill all results are yielded
        """
        image_config = None
        if request.HasField("image_config"):
            image_config = {
                "base_image": request.image_config.base_image,
                "pip_packages": list(request.image_config.pip_packages),
                "commands": list(request.image_config.commands),
            }
        # step 1: enqueue tasks and track them with index
        pending = {}  # task_id -> index
        for i, args_bytes in enumerate(request.args_pickles):
            task_id = enqueue_task(request.function_pickle, args_bytes, image_config=image_config)
            pending[task_id] = i

        # step 2: poll untill all tasks are done
        timeout_seconds = 120
        start_time = time.time()

        while pending:
            # checking for timeout
            if time.time() - start_time > timeout_seconds:
                # this yields error for remaining tasks
                for task_id, index in pending.items():
                    yield nano_modal_pb2.StreamResult(index=index, error="Task Timed Out")
                return

            # check each pending task
            completed = []
            for task_id, index in pending.items():
                result_bytes = get_result(task_id)
                if result_bytes is not None:
                    # task is completed and we yield the result
                    yield nano_modal_pb2.StreamResult(index=index, result_pickle=result_bytes)
                    completed.append(task_id)

            # remove completed tasks from pending
            for task_id in completed:
                del pending[task_id]

            # small sleep to avoid hammering redis
            if pending:
                time.sleep(0.1)

    def GetResult(self, request, context):
        task_id = request.task_id
        result_bytes = get_result(task_id)
        if result_bytes is None:
            return nano_modal_pb2.GetResultResponse(error="result pending")
        return nano_modal_pb2.GetResultResponse(result_pickle=result_bytes)
