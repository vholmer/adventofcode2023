import re
import numpy as np

from typing import List
from datetime import datetime

class Map:
    diffs: List[int]
    source_starts: List[int]
    dest_starts: List[int]
    range_lengths: List[int]

    def __init__(self, source_starts: List[int], dest_starts: List[int], range_lengths: List[int]):
        self.source_starts = source_starts
        self.dest_starts = dest_starts
        self.range_lengths = range_lengths
        self.diffs = []
        self.sources = []
        self.dests = []

        for i in range(len(self.source_starts)):
            self.sources.append(range(self.source_starts[i], self.source_starts[i] + self.range_lengths[i]))
            self.dests.append(range(self.dest_starts[i], self.dest_starts[i] + self.range_lengths[i]))
    
        for i in range(len(self.source_starts)):
            self.diffs.append(self.dest_starts[i] - self.source_starts[i])

    def get(self, value: int) -> int:
        for i in range(len(self.sources)):
            if value in self.sources[i]:
                return self.diffs[i] + value
        return value


    def get_test_starts(self, seed_range: range) -> List[int]:
        result = []

        breakpoint()

        #TODO: Refactor this to use ranges! I'm sure we can fix it with ranges :)

        seed_end = seed_start + seed_range - 1

        for i in range(len(self.source_starts)):
            source_start = self.source_starts[i]
            source_end = source_start + self.range_lengths[i] - 1

            if seed_start >= source_start and seed_end <= source_end:
                result.append(seed_start)
            elif seed_start > source_start and seed_end > source_end and seed_start < source_end:
                result.append(seed_start)
                result.append(source_end + 1)
            elif seed_start < source_start and seed_end < source_end and seed_end > source_start:
                result.append(source_start)
                result.append(seed_end + 1)
            else:
                result.append(seed_start)
                
        return list(set(result))

def get_map(name: str, data: str) -> Map:
    map_matches = re.findall(f'{name} map:\s+((?:\d+\s+)+\d+)', data)
    map_ranges_str = map_matches[0].strip().split('\n')
    map_ranges = [[int(y) for y in x.split()] for x in map_ranges_str]

    dest_list = []
    source_list = []
    step_list = []
    
    for map_range in map_ranges:
        dest, source, steps = map_range

        dest_list.append(dest)
        source_list.append(source)
        step_list.append(steps)

    return Map(source_starts=source_list, dest_starts=dest_list, range_lengths=step_list)

def solve():
    file = open("data/5/test.txt")

    file_str = file.read()
    
    seed_matches = re.findall('seeds: ((?:\d+\s+)+)', file_str)

    seeds = [int(x) for x in seed_matches[0].strip().split()]

    seed_to_soil = get_map(name='seed-to-soil', data=file_str)
    soil_to_fertilizer = get_map(name='soil-to-fertilizer', data=file_str)
    fertilizer_to_water = get_map(name='fertilizer-to-water', data=file_str)
    water_to_light = get_map(name='water-to-light', data=file_str)
    light_to_temperature = get_map(name='light-to-temperature', data=file_str)
    temperature_to_humidity = get_map(name='temperature-to-humidity', data=file_str)
    humidity_to_location = get_map(name='humidity-to-location', data=file_str)

    locations = []

    def get_location(seed: int) -> int:
        soil = seed_to_soil.get(seed)
        fertilizer = soil_to_fertilizer.get(soil)
        water = fertilizer_to_water.get(fertilizer)
        light = water_to_light.get(water)
        temperature = light_to_temperature.get(light)
        humidity = temperature_to_humidity.get(temperature)
        location = humidity_to_location.get(humidity)

        return location

    for seed in seeds:
        location = get_location(seed)

        locations.append(location)

    print(f"Answer 5A: {min(locations)}")

    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append(range(seeds[i], seeds[i] + seeds[i + 1]))

    min_location = None

    """ # Brute force solution below. Too slow!
    for seed_range in seed_ranges:
        print(f"{datetime.now()} - {seed_range}, {min_location}")
        for i in seed_range:
            location = get_location(i)

            if not min_location:
                min_location = location
            elif location < min_location:
                min_location = location
    """

    for seed_range in seed_ranges:
        seed_to_soil.get_test_starts(seed_range)
    
    
    print(f"Answer 5B: {min_location}")
