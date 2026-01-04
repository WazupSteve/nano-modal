from .client import invoke, invoke_many_stream
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

    def map(self, inputs, ordered=True):
        """
        Execute function in parallel over list of inputs.

        Args:
            inputs: List of inputs to process
            ordered: If True, yield results in input order.
                    If False, yield results as they complete.
        """
        fn_bytes = serialize_function(self.func)
        args_pickles = [serialize_args(i) for i in inputs]
        num_inputs = len(args_pickles)

        if not ordered:
            # Yield immediately as results arrive (out of order)
            for index, result_bytes, error in invoke_many_stream(fn_bytes, args_pickles):
                if error:
                    raise Exception(f"Task {index} failed: {error}")
                yield deserialize(result_bytes)
        else:
            # Collect all, then yield in order
            results = [None] * num_inputs
            for index, result_bytes, error in invoke_many_stream(fn_bytes, args_pickles):
                if error:
                    raise Exception(f"Task {index} failed: {error}")
                results[index] = deserialize(result_bytes)
            for result in results:
                yield result
