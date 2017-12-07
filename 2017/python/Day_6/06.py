# Advent of Code 2017
# https://adventofcode.com/2017
# Day 6
# https://adventofcode.com/2017/day/6

"""
--- Day 6: Memory Reallocation ---

A debugger program here is having an issue: it is trying to repair a memory reallocation routine, but it keeps getting
stuck in an infinite loop.

In this area, there are sixteen memory banks; each memory bank can hold any number of blocks. The goal of the
 routine is to balance the blocks between the memory banks.

The reallocation routine operates in cycles. In each cycle, it finds the memory bank with the most blocks (ties won by
the lowest-numbered memory bank) and redistributes those blocks among the banks. To do this, it removes all of the
blocks from the selected bank, then moves to the next (by index) memory bank and inserts one of the blocks. It continues
doing this until it runs out of blocks; if it reaches the last memory bank, it wraps around to the first one.

The debugger would like to know how many redistributions can be done before a blocks-in-banks configuration is produced
that has been seen before.

For example, imagine a scenario with only four memory banks:

The banks start with 0, 2, 7, and 0 blocks. The third bank has the most blocks, so it is chosen for redistribution.
Starting with the next bank (the fourth bank) and then continuing to the first bank, the second bank, and so on, the 7
blocks are spread out over the memory banks. The fourth, first, and second banks get two blocks each, and the third bank
gets one back. The final result looks like this: 2 4 1 2.
Next, the second bank is chosen because it contains the most blocks (four). Because there are four memory banks, each
gets one block. The result is: 3 1 2 3.
Now, there is a tie between the first and fourth memory banks, both of which have three blocks. The first bank wins the
tie, and its three blocks are distributed evenly over the other three banks, leaving it with none: 0 2 3 4.
The fourth bank is chosen, and its four blocks are distributed such that each of the four banks receives one: 1 3 4 1.
The third bank is chosen, and the same thing happens: 2 4 1 2.
At this point, we've reached a state we've seen before: 2 4 1 2 was already seen. The infinite loop is detected after
the fifth block redistribution cycle, and so the answer in this example is 5.

Given the initial block counts in your puzzle input, how many redistribution cycles must be completed before a
configuration is produced that has been seen before?

--- Part Two ---

Out of curiosity, the debugger would also like to know the size of the loop: starting from a state that has already been
seen, how many block redistribution cycles must be performed before that same state is seen again?

In the example above, 2 4 1 2 is seen again after four cycles, and so the answer in that example would be 4.

How many cycles are in the infinite loop that arises from the configuration in your puzzle input?

"""

from copy import deepcopy

my_memory = [2, 8, 8, 5, 4, 2, 3, 1, 5, 5, 1, 2, 15, 13, 5, 14]


def count_steps(memory):

    # init variables
    mem_len = len(memory)
    new_memory = deepcopy(memory)
    seen_configs = [deepcopy(new_memory)]

    highest_val = 0
    highest_idx = 0

    steps = 0

    while True:

        # increment step counter
        steps += 1

        # find highest value and reset it to 0 in memory array
        highest_idx, highest_val = find_highest(new_memory)
        new_memory[highest_idx] = 0

        # reallocate memory block
        alloc_idx = highest_idx + 1
        new_memory = reallocate_block(new_memory, highest_val, alloc_idx)

        # conditionally append new memory layout to seen memory configurations
        if new_memory not in seen_configs:
            seen_configs.append(deepcopy(new_memory))
        else:
            break

    return steps


def count_loops(memory):

    # init variables
    mem_len = len(memory)
    new_memory = deepcopy(memory)
    seen_configs = [deepcopy(new_memory)]

    highest_val = 0
    highest_idx = 0

    looping = False
    loops = 0

    while True:

        # increment step counter
        if looping:
            loops += 1

        # find highest value and reset it to 0 in memory array
        highest_idx, highest_val = find_highest(new_memory)
        new_memory[highest_idx] = 0

        # reallocate memory block
        alloc_idx = highest_idx + 1
        new_memory = reallocate_block(new_memory, highest_val, alloc_idx)

        if not looping:
            # conditionally append new memory layout to seen memory configurations
            if new_memory not in seen_configs:
                seen_configs.append(deepcopy(new_memory))
            else:
                first_loop_config = deepcopy(new_memory)
                looping = True
        else:
            # stop looping once we've complete one cycle
            if new_memory == first_loop_config:
                break

    return loops


def find_highest(memory_):

    mem_len = len(memory_)

    search_idx = 0
    search_val = 0

    highest_idx = 0
    highest_val = 0

    # find highest value block in order to reallocate it
    while search_idx < mem_len:

        # iterate over each block storing the index of the largest
        search_val = memory_[search_idx]
        if search_val > highest_val:
            highest_idx = memory_.index(search_val)
            highest_val = memory_[highest_idx]

        search_idx += 1

    return highest_idx, highest_val


def reallocate_block(memory_, value, start_idx):

    mem_len = len(memory_)
    new_memory = memory_

    reamining_block = value
    alloc_idx = start_idx

    # reallocate memory
    while reamining_block > 0:

        if mem_len <= alloc_idx:
            alloc_idx = 0

        new_memory[alloc_idx] += 1
        reamining_block -= 1
        alloc_idx += 1

    return new_memory


if __name__ == '__main__':

    # ------ Part 1 ------ #
    assert count_steps([0, 2, 7, 0]) == 5
    # display my solution
    print('Part 1: ', count_steps(my_memory))

    # ------ Part 2 ------ #
    assert count_loops([0, 2, 7, 0]) == 4
    # display my solution
    print('Part 2: ', count_loops(my_memory))
