"""
Configuration file
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_server_address():
    return os.getenv("NANO_MODAL_SERVER", "localhost:50051")  # (env_var,default)


def get_redis_url():
    return os.getenv("NANO_MODAL_REDIS", "redis://localhost:6379")  # (env_var,default)
