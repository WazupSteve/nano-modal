"""
redis queue acts as a buffer between client and workers
client -> server -> redis_queue -> worker -> docker -> result

redis data structures
- list ( task queue ) LPUSH and RPOP
- hash ( result storage ) HSET and HGET
"""

import json
import uuid

import redis

from nano_modal.config import get_redis_url

# connect to rerdis
redis_client = redis.from_url(get_redis_url())


def enqueue_task(fn_bytes, args_bytes):
    """
    store in redis queue
    redis list for task queue
    client -> server -> redis queue
    """
    task_id = str(uuid.uuid4())

    task = {"task_id": task_id, "fn_bytes": fn_bytes.hex(), "args_bytes": args_bytes.hex()}
    # convert to json string for redis storage
    task_json = json.dumps(task)
    redis_client.lpush("nano_modal:queue", task_json)
    return task_id


def dequeue_task(timeout=5):
    """
    pull the task from the queue
    redis_queue -> worker
    """
    result = redis_client.brpop("nano_modal:queue", timeout=timeout)
    if result is None:
        return None
    _, task_json = result  # brpop returns (queue_name, data)
    task = json.loads(task_json)  # task_json is bytes, json.loads handles that
    task["fn_bytes"] = bytes.fromhex(task["fn_bytes"])
    task["args_bytes"] = bytes.fromhex(task["args_bytes"])
    return task


def store_result(task_id, result_bytes):
    """
    save the execution result
    redis hash data structure for storing result (task_id->result)
    worker-> redis results
    """
    redis_client.hset("nano_modal:results", task_id, result_bytes.hex())


def get_result(task_id):
    """
    retreive result
    redis result -> server -> client
    """
    result_hex = redis_client.hget("nano_modal:results", task_id)
    if result_hex is None:
        return None
    return bytes.fromhex(result_hex.decode())
