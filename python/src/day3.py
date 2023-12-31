from typing import (
    List,
    Tuple
)

width = 0
height = 0
matrix = []

def get_number(row: int, col: int) -> int:
    global width, height
    
    # First, find start of number
    cur_index = col

    line = matrix[row]
    
    if cur_index > 0:
        while cur_index > 0 and line[cur_index].isdigit():
            cur_index -= 1

            if not line[cur_index].isdigit():
                cur_index += 1
                break

    number_str = ""

    while line[cur_index].isdigit() and cur_index < width:
        number_str += line[cur_index]

        if cur_index + 1 < width:
            cur_index += 1
        else:
            break

    return int(number_str) if number_str else None

def is_symbol(inp: str) -> bool:
    return not inp.isdigit() and inp != '.'

def has_symbol_neighbor(row: int, col: int) -> bool:
    global width, height

    # fn, found neighbor
    fn = False

    if row > 0 and col > 0: # top left
        check = matrix[row - 1][col - 1]
        fn = fn or is_symbol(check)
    if row > 0: # above
        check = matrix[row - 1][col]
        fn = fn or is_symbol(check)
    if row > 0 and col < width - 1: # top right
        check = matrix[row - 1][col + 1]
        fn = fn or is_symbol(check)
    if col > 0: # left
        check = matrix[row][col - 1]
        fn = fn or is_symbol(check)
    if col < width - 1: # right
        check = matrix[row][col + 1]
        fn = fn or is_symbol(check)
    if row < height - 1 and col > 0: # bottom left
        check = matrix[row + 1][col - 1]
        fn = fn or is_symbol(check)
    if row < height - 1: # bottom
        check = matrix[row + 1][col]
        fn = fn or is_symbol(check)
    if row < height - 1 and col < width - 1: # bottom right
        check = matrix[row + 1][col + 1]
        fn = fn or is_symbol(check)

    return fn

def get_symbol_coords() -> List[Tuple[int, int]]:
    result = []

    for i, row in enumerate(matrix):
        for j, col in enumerate(matrix):
            if is_symbol(matrix[i][j]):
                result.append((i, j))

    return result

def get_neighbors(row: int, col: int) -> List[int]:
    neighbors = []

    for i in range(row - 1, row + 2):
        seen_sep = True
        for j in range(col - 1, col + 2):
            if i < 0 or i > width:
                continue
            if j < 0 or j > height:
                continue

            n = get_number(i, j)

            if n is not None and seen_sep:
                seen_sep = False
                neighbors.append(n)

            if n is None and not seen_sep:
                seen_sep = True

    return neighbors
        
def solve():
    global width, height
    
    file = open("data/3/data.txt", "r")

    for i, line in enumerate(file):
        width = len(line.strip())
        matrix.append(line.strip())

    height = i + 1

    result = 0
    for i, row in enumerate(matrix):
        seen_sep = True
        for j, col in enumerate(row):
            fn = get_number(i, j)

            if fn:
                hn = has_symbol_neighbor(i, j)

                if hn and seen_sep:
                    # print(f"Adding {fn} from {i}, {j}")
                    seen_sep = False
                    result += fn
            if not matrix[i][j].isdigit():
                seen_sep = True
            

    print(f"Answer 3A: {result}")

    # 3B:
    # First, find the coordinates of all symbols
    symbol_coords = get_symbol_coords()

    gear_ratios = 0

    # Then, for each symbol coord, get neighbors
    for coords in symbol_coords:
        i, j = coords

        neighbors = get_neighbors(i, j)

        # Finally, if 2 neighbors, we have a gear
        if len(neighbors) == 2:
            gear_ratios += neighbors[0] * neighbors[1]

    print(f"Answer 3B: {gear_ratios}")
