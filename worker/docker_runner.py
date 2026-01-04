import base64
import subprocess
from typing import Optional


def execute_in_docker(
    fn_bytes: bytes, args_bytes: bytes, image_config: Optional[dict] = None
) -> bytes:
    fn_b64 = base64.b64encode(fn_bytes).decode()
    args_b64 = base64.b64encode(args_bytes).decode()

    # user provided image config else default
    if image_config is None:
        image_config = {}

    base_image = image_config.get("base_image", "python:3.11-slim")
    pip_packages = image_config.get("pip_packages", [])
    commands = image_config.get("commands", [])

    all_packages = ["cloudpickle"] + list(pip_packages)
    packages_str = " ".join(all_packages)

    # setup commands
    setup_section = " "
    if commands:
        setup_section = "\n".join([f"import os; os.system({repr(cmd)})" for cmd in commands])
        setup_section += "\n"

    python_code = f"""{setup_section}import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", {repr(packages_str).replace("'", '"')}],
                check=True, 
                capture_output=True)
import cloudpickle
import base64
    
fn = cloudpickle.loads(base64.b64decode('{fn_b64}'))
args, kwargs = cloudpickle.loads(base64.b64decode('{args_b64}'))
result = fn(*args, **kwargs)
print(base64.b64encode(cloudpickle.dumps(result)).decode())
"""
    result = subprocess.run(
        ["podman", "run", "--rm", base_image, "python", "-c", python_code],
        capture_output=True,
        text=True,
    )

    # handling errors
    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "unknown container error during execution"
        raise RuntimeError(f"container execution has failed:{error_msg}")

    return base64.b64decode(result.stdout.strip())
