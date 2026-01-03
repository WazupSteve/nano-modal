"""
executor : worker loop that pulls task from redis
execute them inside docker
store results back in redis
"""

import logging
import time

from server.queue import dequeue_task, store_result
from worker.docker_runner import execute_in_docker


def process_task(task):
    task_id = task["task_id"]
    fn_bytes = task["fn_bytes"]
    args_bytes = task["args_bytes"]
    logging.info("worker executing task %s", task_id)
    try:
        result_bytes = execute_in_docker(fn_bytes, args_bytes)
        store_result(task_id, result_bytes)
    except Exception as exc:
        logging.exception("task %s failed %s", task_id, exc)
        store_result(task_id, str(exc).encode())


def run_executor(poll_interval=1, should_stop=lambda: False):
    """
    timeout=5 on brpop : redis blocks upto 5 seconds
    if nothing arrives, we sleep "poll_interval" seconds
    """
    logging.info("worker executor has started")
    while not should_stop():
        task = dequeue_task(timeout=5)
        if task is None:
            time.sleep(poll_interval)  # temporary limit set
            continue
        process_task(task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_executor()
