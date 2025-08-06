import random
import time


def sleep():
    """Random sleep 0-1 sec"""
    sleep_time = random.uniform(0, 1)
    time.sleep(sleep_time)
