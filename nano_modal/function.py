from .serialize import serialize_function, serialize_args, deserialize
from .client import invoke


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
