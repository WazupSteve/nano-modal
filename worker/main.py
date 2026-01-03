import logging
import signal

from worker.executor import run_executor

shutdown = False


def handle_signal(signum, frame):
    global shutdown
    logging.info("signal %s received, shutting down", signum)
    shutdown = True


def main():
    logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    while not shutdown:
        run_executor()
