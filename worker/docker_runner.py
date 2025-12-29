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
        network_mode="none",
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=100000,  # CPU quota (1 core)
        read_only=True,
        user="nobody",
    )

    # decode the result back to bytes from string
    return base64.b64decode(result.strip())
