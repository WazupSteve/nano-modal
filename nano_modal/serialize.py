import cloudpickle

# serialize the user functions for sending
def serialize_function(fxn):
    '''
    fxn: User defined function to be run 
    return : bytes
    '''

# serialize the user functions args for sending 
def serialize_args(*args,**kwargs):
    '''
    *args,**kwargs
    return : bytes
    '''

def deserialize(data):
    '''
    data: data to be deserialized to return output of the function to the user
    return : object
    '''
