import pytest
from nano_modal.serialize import serialize_function, deserialize, serialize_args

def test_serial_deserial_workflow():
    # test function
    def compute(x,y):
        return x**2 + y**3 

    # serializing the function
    fxn_bytes = serialize_function(compute)

    # args,kwargs serializing 
    args_bytes = serialize_args(4,y=3)

    # deserialize
    fxn_new = deserialize(fxn_bytes)
    args_new_tuple = deserialize(args_bytes)

    #unpacking tuple
    args_new, kwargs_new = args_new_tuple

    #execute the new function with the new args
    result = fxn_new(*args_new,**kwargs_new)

    assert result == compute(4,3)