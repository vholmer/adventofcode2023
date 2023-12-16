import copy

import numpy as np

from typing import (
    List,
    Tuple,
)

class Walker:
    instr: str
    world: dict
    cur_key: str
    num_steps: int
    pc: int
    pc_z: int
    first_z: str
    in_loop: bool
    z_dists: List[Tuple[str, int]]
    visited: set

    def __init__(self, instr: str, world: dict) -> None:
        self.instr = instr
        self.world = world
        self.cur_key = "AAA"
        self.num_steps = 0
        self.first_z = None
        self.pc = 0
        self.pc_z = None
        self.in_loop = False
        self.z_dists = set()
        self.visited = set()

    def walk(self, verbose = False) -> None:
        while self.cur_key != "ZZZ":
            self.step(verbose)

        if verbose:
            print(f"Reached ZZZ in {self.num_steps} steps.")

    def step(self, verbose = False) -> None:
        direction = self.instr[self.pc]

        left_key = self.world[self.cur_key][0]
        right_key = self.world[self.cur_key][1]

        if direction == "L":
            if left_key in self.visited:
                self.in_loop = True
            if verbose:
                print(f"Step {self.num_steps}: At {self.cur_key} going L to {self.world[self.cur_key][0]}")
            self.cur_key = left_key
        elif direction == "R":
            if right_key in self.visited:
                self.in_loop = True
            if verbose:
                print(f"Step {self.num_steps}: At {self.cur_key} going R to {self.world[self.cur_key][1]}")
            self.cur_key = right_key

        self.visited.add(self.cur_key)

        self.pc = (self.pc + 1) % len(self.instr)
        self.num_steps += 1

        self.check_loop()

    def check_loop(self) -> None:
        direction = self.instr[self.pc]

        left_key = self.world[self.cur_key][0]
        right_key = self.world[self.cur_key][1]

        if direction == "L":
             if left_key in self.visited:
                self.in_loop = True
        elif direction == "R":
            if right_key in self.visited:
                self.in_loop = True

    def walk_to_z(self) -> int:
        steps_to_z = 0
    
        while True:
            self.step()
            steps_to_z += 1

            if self.cur_key.endswith("Z"):
                break

        if not self.first_z and not self.pc_z:
            self.first_z = self.cur_key
            self.pc_z = self.pc

        return steps_to_z

    def walk_z(self) -> None:
        """Walk normally until Z-key loop"""
        # While not in first Z-key, walk to next Z-key and build list
        # if not self.z_dists:
        while True:
            steps_to_z = self.walk_to_z()
        
            if not self.in_loop:
                continue
            
            from_key = self.cur_key

            in_first_z = self.cur_key == self.first_z and self.pc == self.pc_z

            self.z_dists.add((from_key, steps_to_z))

            if in_first_z:
                break
        # Walk to next Z

def solve():
    file = open("data/8/data.txt")

    world = {}

    for i, line in enumerate(file):
        if i == 0:
            instr = line.strip()
            continue
        elif i == 1 or line == "\n":
            continue

        key = line.split("=")[0].strip()

        tuple_first = line.split("(")[1].split(",")[0].strip()
        tuple_second = line.split("(")[1].split(",")[1][:-2].strip()

        world[key] = (tuple_first, tuple_second)

    walker = Walker(instr, world)

    walker.walk()

    print(f"Answer 8A: {walker.num_steps}")

    starting_points = [x for x in world.keys() if x.endswith("A")]

    walkers = []

    for starting_point in starting_points:
        new_walker = Walker(instr, world)

        new_walker.cur_key = starting_point
        new_walker.visited.add(starting_point)
        
        walkers.append(new_walker)

    for walker in walkers:
        walker.walk_z()

    steps = []

    for walker in walkers:
        for z_dist in walker.z_dists:
            steps.append(z_dist[1])

    answer = np.lcm.reduce(steps)

    print(f"Answer 8B: {answer}")
