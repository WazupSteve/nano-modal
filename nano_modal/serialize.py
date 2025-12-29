import cloudpickle


# serialize the user functions for sending
def serialize_function(fxn):
    """
    fxn: User defined function to be run
    return : bytes
    """
    serialize = cloudpickle.dumps(fxn)
    return serialize


# serialize the user functions args for sending
def serialize_args(*args, **kwargs):
    """
    *args,**kwargs
    return : bytes
    """
    # we must not send args and kwargs seperately, we need to send as one packet of data
    packet = (args, kwargs)
    serialize_args = cloudpickle.dumps(packet)
    return serialize_args


# deserialize to obtain the result
def deserialize(data):
    """
    data: data to be deserialized to return output of the function to the user
    return : object
    """
    result = cloudpickle.loads(data)
    return result
