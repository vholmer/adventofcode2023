class Walker:
    instr: str
    world: dict
    cur_key: str
    num_steps: int
    pc: str
    in_loop: bool
    dist_to_z: int
    visited: set

    def __init__(self, instr: str, world: dict) -> None:
        self.instr = instr
        self.world = world
        self.cur_key = "AAA"
        self.num_steps = 0
        self.pc = 0
        self.in_loop = False
        self.dist_to_z = None
        self.visited = set()

    def walk(self, verbose = False) -> None:
        while self.cur_key != "ZZZ":
            self.step(verbose)

        if verbose:
            print(f"Reached ZZZ in {self.num_steps} steps.")

    def step(self, verbose = False) -> None:
        self.visited.add(self.cur_key)
        
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

        self.pc = (self.pc + 1) % len(self.instr)
        self.num_steps += 1

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
        
        walkers.append(new_walker)

    while any([x for x in walkers if not x.cur_key.endswith("Z")]):
        for walker in walkers:
            walker.step()

    print(f"Answer 8B: {walkers[0].num_steps}")
