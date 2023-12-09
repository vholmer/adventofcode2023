import re
import numpy as np

from typing import List
from datetime import datetime

def split(inp: range, chk: range) -> List[range]:
    """
    Cases
    1.
    [inp_start to chk_start - 1] = range(inp.start, chk.start)
    [chk_start to inp_end] = range(chk.start, inp.stop)
    
    | --- inp --- |
       | --- chk --- |

    | ------ inp ------ |
        | --- chk --- |
    
    2.
    [inp_start to chk_end] = range(inp.start, chk.stop)
    [chk_end + 1 to inp_end] = range(chk.stop, inp.stop)
    
         | --- inp --- |
    | --- chk --- |
    
    | ------ inp ------ |
    | --- chk --- |
    
    3.
    [inp_start to inp_end] = range(inp.start, inp.stop)
    
       | - inp - |
    | --- chk --- |
    
    4.
    [inp_start to chk_start - 1] = range(inp.start, chk.start)
    [chk_start to chk_end] = range(chk.start, chk.end)
    [chk_end + 1 to inp_end] = range(chk.end, inp.stop)
    
    | --- inp --- |
     | - chk - |
    
    Summary: We have 4 distinct cases of overlap.
     
    Algorithm:
    1. Find which of case 1-4.
    2. Split into new ranges accordingly, return them from function f
    3. Repeat step 2 for next map, with output from previous step as input
    4. Finally a range of locations will be retrieved. Get the location value
       for the first value in each range, return the minimum
    """
    # Case 1
    if inp.start < chk.start and inp.stop <= chk.stop and chk.start < inp.stop:
        return [range(inp.start, chk.start), range(chk.start, inp.stop)]
    # Case 2
    elif inp.start >= chk.start and inp.stop > chk.stop and chk.stop > inp.start:
        return [range(inp.start, chk.stop), range(chk.stop, inp.stop)]
    # Case 3
    elif inp.start >= chk.start and inp.stop <= chk.stop:
        return [inp]
    # Case 4
    elif inp.start < chk.start and inp.stop > chk.stop:
        return [range(inp.start, chk.start), range(chk.start, chk.stop), range(chk.stop, inp.stop)]

def overlaps(a: range, b: range) -> bool:
    # Case 1
    if a.start < b.start and a.stop <= b.stop and b.start < a.stop:
        return True
    # Case 2
    elif a.start >= b.start and a.stop > b.stop and b.stop > a.start:
        return True
    # Case 3
    elif a.start >= b.start and a.stop <= b.stop:
        return True
    # Case 4
    elif a.start < b.start and a.stop > b.stop:
        return True
    return False
        
class Map:
    name: str
    diffs: List[int]
    source_starts: List[int]
    dest_starts: List[int]
    range_lengths: List[int]

    def __init__(self, name: str, source_starts: List[int], dest_starts: List[int], range_lengths: List[int]):
        self.name = name
        self.source_starts = source_starts
        self.dest_starts = dest_starts
        self.range_lengths = range_lengths
        self.sources = []
        self.dests = []
        self.diffs = []

        for i in range(len(self.source_starts)):
            self.diffs.append(self.dest_starts[i] - self.source_starts[i])
            
        for i in range(len(self.source_starts)):
            self.sources.append(range(self.source_starts[i], self.source_starts[i] + self.range_lengths[i]))
            self.dests.append(range(self.dest_starts[i], self.dest_starts[i] + self.range_lengths[i]))

    def get(self, value: int) -> int:
        for i in range(len(self.sources)):
            if value in self.sources[i]:
                return self.diffs[i] + value
        return value

    def get_split_ranges(self, inp_ranges: List[range]) -> List[range]:
        min_source = min([s.start for s in self.sources])

        result = []

        for inp in inp_ranges:
            for i, src in enumerate(self.sources):
                split_ranges = split(inp, src)

                if split_ranges:
                    for split_range in split_ranges:
                        # Transform to each split range to output range:
                        # 1. find dest - source diff, where source is range(0, 0) if no overlap
                        # 2. add it to split_range
                        if not any([overlaps(split_range, src) for src in self.sources]):
                            dest_range = None
                        elif not overlaps(split_range, src):
                            continue
                        else:
                            dest_range = self.dests[i]

                        diff_start = dest_range.start - src.start if dest_range else 0
                        diff_stop = dest_range.stop - src.stop if dest_range else 0

                        result.append(range(split_range.start + diff_start, split_range.stop + diff_stop))
            if not any([overlaps(inp, src) for src in self.sources]):
                result.append(inp)

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

    return Map(name=name, source_starts=source_list, dest_starts=dest_list, range_lengths=step_list)

def solve():
    file = open("data/5/data.txt")

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
        seed_ranges.append(range(seeds[i], seeds[i] + seeds[i + 1] + 1))
                
    soil_ranges = seed_to_soil.get_split_ranges(seed_ranges)
    fertilizer_ranges = soil_to_fertilizer.get_split_ranges(soil_ranges)
    water_ranges = fertilizer_to_water.get_split_ranges(fertilizer_ranges)
    light_ranges = water_to_light.get_split_ranges(water_ranges)
    temperature_ranges = light_to_temperature.get_split_ranges(light_ranges)
    humidity_ranges = temperature_to_humidity.get_split_ranges(temperature_ranges)
    location_ranges = humidity_to_location.get_split_ranges(humidity_ranges)

    min_location = min([x.start for x in location_ranges])
    
    print(f"Answer 5B: {min_location}")
