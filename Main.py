import itertools
import time
from datetime import datetime


def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


def day1():
    print('First part:')
    with open('Day1', 'r') as f:
        changes = f.readlines()
    current_frequency = 0
    for change in changes:
        current_frequency += int(change)
    print(f'The resulting frequency is {current_frequency}')

    print('Second part:')
    current_frequency = 0
    reached_frequencies = {[0]}
    for change in itertools.cycle(changes):
        current_frequency += int(change)
        if current_frequency in reached_frequencies:
            print(f'Repeated frequency twice is {current_frequency}')
            return
        reached_frequencies.add(current_frequency)


def day2():
    print('First part:')
    appears_twice = 0
    appears_thrice = 0
    with open('Day2', 'r') as f:
        boxes = f.readlines()

    for line in boxes:
        counter = {}
        for letter in line:
            if letter not in counter:
                counter[letter] = 0
            counter[letter] += 1
        was_twice = False
        was_thrice = False
        for value in counter.values():
            if not was_twice and value == 2:
                appears_twice += 1
                was_twice = True
            elif not was_thrice and value == 3:
                appears_thrice += 1
                was_thrice = True

            if was_twice and was_thrice:
                break
    print(f'Checksum = {appears_twice * appears_thrice}')

    print('Second part:')

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):

            diff = 0
            where = 0
            for count in range(len(boxes[i])):
                if boxes[i][count] is not boxes[j][count]:
                    diff += 1
                    where = count
                    if diff > 1:
                        break

            if diff == 1:
                string = ''
                for count in range(len(boxes[i])):
                    if count is not where:
                        string += (boxes[i][count])
                print(string)
                return


def day3():
    print('First part:')
    with open('Day3', 'r') as f:
        fabrics = f.readlines()

    used = {}
    for fabric in fabrics:
        parts = fabric.strip().split(' ')
        coordinates = parts[2][:-1].split(',')
        coordinates = [int(i) for i in coordinates]
        lengths = parts[3].split('x')
        lengths = [int(i) for i in lengths]

        for x in range(coordinates[0], coordinates[0] + lengths[0]):
            for y in range(coordinates[1], coordinates[1] + lengths[1]):
                if (x, y) not in used:
                    used[(x, y)] = 1
                else:
                    used[(x, y)] += 1

    overlapping = 0
    for i in used.values():
        if i > 1:
            overlapping += 1
    print(overlapping)

    print('Part 2:')
    which_part = {}
    numbers = []
    for fabric in fabrics:
        parts = fabric.strip().split(' ')
        number = parts[0][1:]
        numbers.append(number)
        coordinates = parts[2][:-1].split(',')
        coordinates = [int(i) for i in coordinates]
        lengths = parts[3].split('x')
        lengths = [int(i) for i in lengths]
        # print(coordinates)
        # print(lengths)

        for x in range(coordinates[0], coordinates[0] + lengths[0]):
            for y in range(coordinates[1], coordinates[1] + lengths[1]):
                if (x, y) not in which_part:
                    which_part[(x, y)] = number
                else:
                    if number in numbers:
                        numbers.remove(number)
                    if which_part[(x, y)] in numbers:
                        numbers.remove(which_part[(x, y)])

    # overlapping = len([k for (k, v) in used.values() if v > 1])
    print(numbers)


def day4():
    with open('Day4', 'r') as f:
        guard_list = f.readlines()
        guard_list.sort()

    print('Part 1:')
    sleeping_guards = {}
    started_sleeping = None
    guard_id = None
    starting_minute = None
    for line in guard_list:
        splitted = line.split()

        if splitted[2] == 'Guard':
            guard_id = splitted[3][1:]
        elif splitted[2] == 'falls':
            starting_minute = int(splitted[1][3:5])
            started_sleeping = datetime.strptime(f'{splitted[0]} {splitted[1]}', '[%Y-%m-%d %H:%M]')
        elif splitted[2] == 'wakes':
            wakeup_time = datetime.strptime(f'{splitted[0]} {splitted[1]}', '[%Y-%m-%d %H:%M]')
            time = wakeup_time - started_sleeping
            if guard_id not in sleeping_guards:
                sleeping_guards[guard_id] = [0] * 60
            for _ in range(0, int(time.seconds / 60)):
                sleeping_guards[guard_id][starting_minute] += 1
                starting_minute = (starting_minute + 1) % 60

    maximum = -1
    sleepy_guard = None
    for k, v in sleeping_guards.items():
        if maximum < sum(v):
            maximum = sum(v)
            sleepy_guard = k

    most_asleep_minute = sleeping_guards[sleepy_guard].index(max(sleeping_guards[sleepy_guard]))
    print(f'Most sleepy guard is {sleepy_guard}, and the answer is {int(sleepy_guard) * most_asleep_minute }')

    print('Part 2:')
    asleep = [[-1] * 60 for _ in range(2)]
    for key, array in sleeping_guards.items():
        for i in range(0, 60):

            if array[i] > asleep[1][i]:
                asleep[0][i] = key
                asleep[1][i] = array[i]
            elif array[i] == asleep[1][i]:
                asleep[0][i] = -1

    maximum = -1
    guard_id = None
    minute = 0
    for i in range(60):
        if asleep[0][i] is not -1 and maximum < asleep[1][i]:
            maximum = asleep[1][i]
            guard_id = asleep[0][i]
            minute = i

    print(f'Guard {guard_id} spent sleeping minute {minute} asleep mostly, answer is {int(guard_id) * minute}')


def day5():
    def react(polymer):
        i = 0
        while i + 1 < len(polymer):
            first_letter = str(polymer[i])
            second_letter = str(polymer[i + 1])

            if (first_letter.upper() == second_letter and first_letter == second_letter.lower()) or (
                    first_letter.lower() == second_letter and first_letter == second_letter.upper()):
                # they destroy each other
                del polymer[i:i + 2]
                i -= 2
            i += 1
            if i == -1:
                i = 0
        return polymer

    print('Part 1')
    with open('Day5', 'r') as f:
        polymer = (f.readline().strip())

    reacted_polymer = react(list(polymer))
    print(f'Length of a polymer after reaction is {len(reacted_polymer)}')

    print('Part 2')
    start = time.time()
    # i can use the already evaluated polymer
    letters = [letter for letter in set(reacted_polymer) if str(letter).isupper()]

    max_length = float('inf')

    for letter in letters:
        # print(f'Removed letter {letter}')
        removed = [letter, str(letter).lower()]
        shorter_polymer = [c for c in reacted_polymer if c not in removed]
        length = len(react(shorter_polymer))
        # print(length)
        if length < max_length:
            max_length = length

    print(f'Shortest polymer has a length of {max_length}')
    end = time.time()
    print(f'It took me {end - start} to get part 2')


def day6():
    with open('Day6', 'r') as f:
        points = []
        for line in f.readlines():
            splitted = line.split(',')
            points.append((int(splitted[0]), int(splitted[1])))

    hull = convex_hull(points)
    min_x = min(points, key=lambda t: t[0])
    max_x = max(points, key=lambda t: t[0])
    min_y = min(points, key=lambda t: t[1])
    max_y = max(points, key=lambda t: t[1])

    print(hull)


def day7():
    pass


def day8():
    pass


def day9():
    pass


def day10():
    pass


def day11():
    pass


while True:
    result = input("Which day do you want to see?\n")
    try:
        day = int(result)
        break
    except ValueError:
        print(f'Input an integer, {result} is not an integer :)\n')

if day == 1:
    day1()
elif day == 2:
    day2()
elif day == 3:
    day3()
elif day == 4:
    day4()
elif day == 5:
    day5()
elif day == 6:
    day6()
elif day == 7:
    day7()
elif day == 8:
    day8()
elif day == 9:
    day9()
elif day == 10:
    day10()
elif day == 11:
    day11()
