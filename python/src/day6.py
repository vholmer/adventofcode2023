import re

from typing import List

def simulate_race(times: List[int], distances: List[int]) -> int:
    results = []
    
    for i in range(len(times)):
        cur_time = times[i]
        cur_dist = distances[i]

        elapsed = 0
        ways_of_winning = 0
        for ms in range(cur_time + 1):
            if elapsed * (cur_time - elapsed) > cur_dist:
                ways_of_winning += 1
            elapsed += 1
        results.append(ways_of_winning)

    answer = 1
    for result in results:
        answer *= result

    return answer

def solve():
    file = open("data/6/data.txt")

    for line in file:
        integers = [int(x) for x in re.findall("\d+", line)]
        if "Time" in line:
            times = integers
        elif "Distance" in line:
            distances = integers

    answer = simulate_race(times, distances)
    
    print(f"Answer 6A: {answer}")

    string = ""
    for time in times:
        string += str(time)

    time = int(string)

    string = ""
    for distance in distances:
        string += str(distance)

    distance = int(string)

    answer = simulate_race([time], [distance])

    print(f"Answer 6B: {answer}")
