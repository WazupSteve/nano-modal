import base64
import subprocess


def execute_in_docker(fn_bytes, args_bytes):
    fn_b64 = base64.b64encode(fn_bytes).decode()
    args_b64 = base64.b64encode(args_bytes).decode()

    python_code = f"""import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", "cloudpickle"],
                check=True, capture_output=True)
import cloudpickle
import base64
    
fn = cloudpickle.loads(base64.b64decode('{fn_b64}'))
args, kwargs = cloudpickle.loads(base64.b64decode('{args_b64}'))
result = fn(*args, **kwargs)
print(base64.b64encode(cloudpickle.dumps(result)).decode())
"""
    result = subprocess.run(
        ["podman", "run", "--rm", "python:3.11-slim", "python", "-c", python_code],
        capture_output=True,
        text=True,
    )

    return base64.b64decode(result.stdout.strip())
