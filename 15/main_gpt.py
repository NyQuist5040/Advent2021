from operator import pos
import numpy as np

with open("15/input.txt") as f:
    input_string = f.read()


# Parse the input
risk_map = np.array([[int(c) for c in line] for line in input_string.strip().split('\n')])

def minimum_risk_naive(risk_map):
    # Initialize the minimum risk array with the risk levels of the first row and the first column
    min_risk = np.zeros_like(risk_map)
    min_risk[-1, :] = [sum(risk_map[-1, i:]) for i in range(1, risk_map.shape[1]+1)]
    min_risk[:, -1] = [sum(risk_map[i:, -1]) for i in range(1, risk_map.shape[0]+1)]

    # Compute the minimum risk of reaching each position by taking the minimum of the two possible paths to that position
    for i in reversed(range(risk_map.shape[0] - 1)):
        for j in reversed(range(risk_map.shape[1] - 1)):
            min_risk[i, j] = min(min_risk[i+1, j] + risk_map[i+1, j], min_risk[i, j+1] + risk_map[i, j+1])

    return min_risk


def explore_map(risk_map, i, j, acceptable_danger, known_bests, already_explored=[]):
    # Returns the danger score of the path with minimal danger from i,j to -1,-1.
    # Explores all possible paths recursively.
    # acceptable_danger represents the maximum total danger that is acceptable,
    #     because we know that a better path would exist.
    max_i, max_j = risk_map.shape

    # Ensure we still have some acceptable danger
    if acceptable_danger < 0:
        return np.inf

    # We know exactly what the best path is from here (from previous computations)
    if known_bests[i, j] >= 0:
        return known_bests[i, j]

    # Check if we found the end
    if i == max_i - 1 and j == max_j - 1:
        return 0

    if (i, j) in already_explored:
        return np.inf

    possible_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dir_min_danger = []
    for dir in possible_dirs:
        new_i, new_j = i + dir[0], j + dir[1]

        # Check that the new position is within bounds
        if 0 <= new_i < max_i and 0 <= new_j < max_j :

            min_risk_in_dir = explore_map(risk_map, new_i, new_j, acceptable_danger - risk_map[new_i, new_j], known_bests, already_explored+[(i, j)])
            dir_min_danger.append(min_risk_in_dir + risk_map[new_i, new_j])

    return min(dir_min_danger)


def minimum_risk(risk_map):

    # Start with the naive approach
    naive_minimas = minimum_risk_naive(risk_map)

    # Array to store the points from which we knowe the absolute best path
    known_bests = np.ones_like(risk_map) * -1

    # find the order in which to explore the array, by sorting by minimum naive path
    explore_i, explore_j = np.unravel_index(np.argsort(naive_minimas, axis=None), naive_minimas.shape)
    print(explore_i, explore_j)

    # Explore in reverse order because the last ones are faster.
    for i, j in zip(explore_i, explore_j):
        exploration_result = explore_map(risk_map, i, j, naive_minimas[i,j], known_bests) # can be np.inf
        known_bests[i, j] = min(naive_minimas[i, j], exploration_result)

        print(str(known_bests) + '\n')

    return known_bests

def min_danger_from_neighbours(i, j, risk_map, known_minimas):
    # returns the minimum danger at i,j if a neighbour is already known, None instead

    max_i, max_j = risk_map.shape

    possible_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    possible_danger_values = []
    for dir in possible_dirs:
        new_i, new_j = i + dir[0], j + dir[1]
        # Check that the new position is within bounds
        if 0 <= new_i < max_i and 0 <= new_j < max_j :
            if not np.isnan(known_minimas[new_i, new_j]):
                possible_danger_values.append(known_minimas[new_i, new_j] + risk_map[new_i, new_j])
    if len(possible_danger_values) == 0:
        return None
    else:
        return min(possible_danger_values)


def iterative_true_minimum(risk_map):
    max_i, max_j = risk_map.shape

    minimas = np.zeros_like(risk_map) * np.nan
    minimas[-1, -1] = 0

    while True:
        if not np.any(np.isnan(minimas)):
            return minimas

        # Edit all i,j that have a neighbour with a known minimum path
        for i in range(max_i):
            for j in range(max_j):
                new_min_danger = min_danger_from_neighbours(i, j, risk_map, minimas)
                if new_min_danger is not None:
                    minimas[i, j] = new_min_danger



# Question 1
print(iterative_true_minimum(risk_map)[0, 0])


def increment_tile(tile: np.ndarray):
    new_tile = ( tile % 9 ) + 1
    return new_tile

### Build the larger map
h_tiles = [risk_map]
for _ in range(4):
    h_tiles.append(increment_tile(h_tiles[-1]))

first_row = np.concatenate(h_tiles, axis=1)

v_tiles = [first_row]
for _ in range(4):
    v_tiles.append(increment_tile(v_tiles[-1]))

large_map = np.concatenate(v_tiles, axis=0)


# Question 2
print(iterative_true_minimum(large_map)[0, 0])
