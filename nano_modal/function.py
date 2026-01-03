from .client import invoke, invoke_many, wait_for_result
from .serialize import deserialize, serialize_args, serialize_function


class Function:
    def __init__(self, func):
        self.func = func

    def local(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.local(*args, **kwargs)

    def remote(self, *args, **kwargs):
        """Execute function remotely on the server via gRPC"""
        # Serialize function and arguments
        fn_bytes = serialize_function(self.func)
        args_bytes = serialize_args(*args, **kwargs)

        # Call server and get result
        result_bytes = invoke(fn_bytes, args_bytes)

        # Deserialize and return result
        return deserialize(result_bytes)

    def map(self, inputs):
        """execute fxn in parallel over list of inputs"""
        # serialize function once
        fn_bytes = serialize_function(self.func)
        # serialize every item in input list
        args_pickles = [serialize_args(i) for i in inputs]
        # call our new client function
        task_ids = invoke_many(fn_bytes, args_pickles)

        for tid in task_ids:
            result_bytes = wait_for_result(tid)
            yield deserialize(result_bytes)
