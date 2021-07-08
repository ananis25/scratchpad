"""
Work through the CDC protocol suggested in the materialize blog post. 

Frank Mcsherry: https://materialize.com/change-data-capture-part-1/
"""

import heapq
import random
from typing import *
from collections import defaultdict


class Update(NamedTuple):
    record: str
    time: int
    incr: int


class Progress(NamedTuple):
    time: int
    count: int


class Finish(NamedTuple):
    time: int


STREAM_NAIVE = Iterator[Union[Update, Finish]]
STREAM_CDC = Iterator[Union[Update, Progress]]


def gen_naive() -> STREAM_NAIVE:
    """generate naive updates that are not dupl/reorder resilient"""
    rng = random.Random(25)
    records = ["a", "b", "c", "d", None]
    increments = [-1, 1]

    ts = 0
    while True:
        rec = rng.choice(records)
        if rec is None:
            yield Finish(ts)
            ts += 1
        else:
            inc = rng.choice(increments)
            yield Update(rec, ts, inc)


def gen_resilient() -> STREAM_CDC:
    """generate Update tuples"""
    rng = random.Random(25)
    records = ["a", "b", "c", "d"]
    increments = [-2, -1, 0, 1, 2]
    prob_increments = [0.05, 0.1, 0.7, 0.1, 0.05]

    ts = 0
    while True:
        count = 0
        for rec in records:
            inc = rng.choices(increments, weights=prob_increments, k=1)[0]
            if inc != 0:
                count += 1
                yield Update(rec, ts, inc)
        yield Progress(ts, count)
        ts += 1


def naive_to_resilient(input_: STREAM_NAIVE) -> STREAM_CDC:
    """
    Convert a naive update stream to the materialize CDC format. We must assume
    the input stream is an ordered stream, with unique updates.
    """
    frontier: int = -1
    buffer: dict[str, int] = {}

    for rec in input_:
        assert rec.time > frontier, "illegal update"
        if isinstance(rec, Finish):
            count = 0
            for key, inc in buffer.items():
                yield Update(key, rec.time, inc)
                count += 1
            buffer.clear()

            yield Progress(rec.time, count)
            frontier = rec.time
        elif isinstance(rec, Update):
            # we assume all of these have the same timestamp, else we must have missed a Finish message
            buffer[rec.record] = buffer.get(rec.record, 0) + rec.incr


def mangler(input_: Iterator[Any]) -> Iterator[Any]:
    """duplicate or reorder the incoming stream"""
    rng = random.Random(25)
    delay = lambda: rng.choices([0, 1, 2, 3, 4], weights=[10, 4, 3, 2, 1], k=1)[0]
    multi = lambda: rng.choices([1, 2, 3], weights=[8, 2, 1], k=1)[0]
    flush = lambda: rng.choice([True, False])

    queue = []
    counter = 0
    for rec in input_:
        for _ in range(multi()):
            # add multiple copies of the message with diff delays
            heapq.heappush(queue, (rec.time + delay(), counter, rec))
            counter += 1

        # output multiple messages, we dont want to create a backlog
        for _ in range(len(queue)):
            if flush():
                yield heapq.heappop(queue)[2]


def demangler(input_: STREAM_CDC) -> STREAM_CDC:
    """
    Get a CDC stream with possible duplicates and out of order
    messages, and produce a legit stream.

    This still produces output out of order. For ex - if all messages corresponding to t=20
    are received after all the messages for t=21. There is no way you would have know there
    was an outstanding timestamp at 20, when clearing 21. Maybe, the input progress statements
    need to be augments with the value for the previous timestamp too. That will solve this.
    """
    frontier: int = -1
    progress_queue: dict[int, Progress] = {}
    progress_min: int = -1
    update_queue: dict[int, set[Update]] = {}

    for rec in input_:
        ts = rec.time
        if ts <= frontier:
            continue

        if ts not in update_queue:
            update_queue[ts] = set()
        if isinstance(rec, Progress):
            if ts not in progress_queue:
                progress_queue[ts] = rec
                progress_min = min(progress_queue)
        elif isinstance(rec, Update):
            update_queue[ts].add(rec)

        # need to check only if the last message had the smallest pending timestamp
        while len(progress_queue) > 0:
            if progress_queue[progress_min].count == len(update_queue[progress_min]):
                for u in update_queue[progress_min]:
                    yield u
                update_queue.pop(progress_min)

                yield progress_queue[progress_min]
                frontier = progress_min
                print("frontier moved to: ", frontier)

                progress_queue.pop(progress_min)
                if len(progress_queue) > 0:
                    progress_min = min(progress_queue)
            else:
                break


if __name__ == "__main__":
    for x in demangler(mangler(naive_to_resilient(gen_naive()))):
        print(x)
        if x.time > 40:
            break
