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
    python_code = f"""
import base64
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "cloudpickle"])

import cloudpickle

fn = cloudpickle.loads(base64.b64decode('{fn_b64}'))
args, kwargs = cloudpickle.loads(base64.b64decode('{args_b64}'))
result = fn(*args, **kwargs)
print(base64.b64encode(cloudpickle.dumps(result)).decode())
"""

    result = client.containers.run(
        "python:3.11-slim", command=["python", "-c", python_code], remove=True
    )

    # decode the result back to bytes from string
    return base64.b64decode(result.strip())
