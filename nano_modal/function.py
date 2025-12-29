class Function:
    def __init__(self, func):
        self.func = func

    def local(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.local(*args, **kwargs)

    def remote(self, *args, **kwargs):
        # serialize, invoke server, deserialize result
        from .client import invoke
        from .serialize import deserialize, serialize_args, serialize_function

        fn_bytes = serialize_function(self.func)
        args_bytes = serialize_args(*args, **kwargs)
        result_bytes = invoke(fn_bytes, args_bytes)
        return deserialize(result_bytes)
