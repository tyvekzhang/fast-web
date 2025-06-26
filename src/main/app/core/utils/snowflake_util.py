"""Snowflake utils to generate unique id"""

import os
import time
from typing import Generator

API_EPOCH = 1730438845

worker_id_bits = 5
process_id_bits = 5
max_worker_id = -1 ^ (-1 << worker_id_bits)
max_process_id = -1 ^ (-1 << process_id_bits)
sequence_bits = 12
process_id_shift = sequence_bits + worker_id_bits
worker_id_shift = sequence_bits
timestamp_left_shift = sequence_bits + worker_id_bits + process_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)


def generator(
    worker_id: int = 1,
    process_id: int = os.getpid() % 31,
    sleep=lambda x: time.sleep(x),
) -> Generator[int, None, None]:
    """
    Generates unique snowflake IDs.

    :param worker_id: Worker ID (default: 1)
    :param process_id: Process ID (default: current process ID modulo 31)
    :param sleep: Sleep function (default: `time.sleep`)
    :return: Generator of snowflake IDs
    """
    assert 0 <= worker_id <= max_worker_id
    assert 0 <= process_id <= max_process_id

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time())

        if last_timestamp > timestamp:
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp

        yield (
            ((timestamp - API_EPOCH) << timestamp_left_shift)
            | (process_id << process_id_shift)
            | (worker_id << worker_id_shift)
            | sequence
        )


global_generator = generator()


def snowflake_id() -> int:
    """
    Returns a unique snowflake ID.

    :return: Snowflake ID
    """
    return next(global_generator)
