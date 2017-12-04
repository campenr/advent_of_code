# Advent of Code 2017
# https://adventofcode.com/2017
# Day 3
# https://adventofcode.com/2017/day/3

"""
You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while
spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the
location of the only access port for this memory system) by programs that can only move up, down, left, or right. They
always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access
port?

"""

from math import sqrt
from itertools import repeat


my_port = 361527


def calculate_steps(start):

    # central point is 1, where distance is 0
    if start == 1:
        return 0

    num = 1
    area = 1  # area of the table

    # calculate area of table required to contain the start number.
    # tables have even sizes and are the square of odd numbers
    while True:
        if start <= area:
            break
        num += 2
        area = num ** 2

    # calculate basic descriptive properties of the data array, and the values at the edge
    length = int(sqrt(area))
    circumference = int((4 * (length - 2)) + 4)
    radius = int((num - 1) / 2)  # does not include the middle value as tables are odd numbered
    edge_vals = [i + 1 for i in list(range(area))[(area - circumference):]]

    # calculate the distance each edge value is from the middle of the edge
    length_dists = [int(sqrt((i - radius) ** 2)) for i in range(length)][:-1]
    edge_dists = [i for j in repeat(length_dists, circumference // 2) for i in j]
    first_edge = edge_dists.pop(0)
    edge_dists.append(first_edge)

    # get Manhattan distance from the start value to the center
    start_idx = edge_vals.index(start)
    start_edge_dist = edge_dists[start_idx]
    start_dist = start_edge_dist + radius

    return start_dist


if __name__ == '__main__':
    assert calculate_steps(1) == 0
    assert calculate_steps(12) == 3
    assert calculate_steps(23) == 2
    assert calculate_steps(1024) == 31

    # display my solution
    print('My Steps: ', calculate_steps(my_port))



