import numpy as np

with open("15/input.txt") as f:
    input_string = f.read()

# Parse the input
risk_map = np.array([[int(c) for c in line] for line in input_string.strip().split('\n')])

# Initialize the minimum risk array with the risk levels of the first row and the first column
min_risk = np.zeros_like(risk_map)
min_risk[0, :] = [sum(risk_map[0, :i]) for i in range(1, risk_map.shape[1]+1)]
min_risk[:, 0] = [sum(risk_map[:i, 0]) for i in range(1, risk_map.shape[0]+1)]

# Compute the minimum risk of reaching each position by taking the minimum of the two possible paths to that position
for i in range(1, risk_map.shape[0]):
    for j in range(1, risk_map.shape[1]):
        min_risk[i, j] = min(min_risk[i-1, j], min_risk[i, j-1]) + risk_map[i, j]

# The minimum risk of reaching the destination position is the bottom right element in the minimum risk array
# We also remove the risk of the first element because it is never entered.
min_risk_destination = min_risk[-1, -1] - min_risk[0, 0]

print(min_risk_destination)