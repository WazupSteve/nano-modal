import base64

import docker


def execute_in_docker(fn_bytes, args_bytes):
    """
    cloudpickled function and arguments
    return: result_bytes : cloudpickled result
    """
    # encode the data base64
    fn_b64 = base64.b64encode(fn_bytes).decode()
    args_b64 = base64.b64encode(args_bytes).decode()

    # create docker client
    client = docker.from_env()
    
    # Python code to run inside container
    # First install cloudpickle, then execute the function
    python_code = f"""
import subprocess
import sys

# Install cloudpickle (suppress output)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'cloudpickle'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import cloudpickle
import base64

# Decode function and arguments
fn = cloudpickle.loads(base64.b64decode('{fn_b64}'))
args, kwargs = cloudpickle.loads(base64.b64decode('{args_b64}'))

# Execute function
result = fn(*args, **kwargs)

# Encode and print result
print(base64.b64encode(cloudpickle.dumps(result)).decode())
"""

    result = client.containers.run(
        "python:3.11-slim",
        command=["python", "-c", python_code],
        remove=True,
    )

    # decode the result back to bytes from string
    return base64.b64decode(result.strip())
