import numpy as np
import matplotlib.pyplot as plt 
import mpmath

"""
Want to check for ns with Σ(n) == 0
at the end of the landscape.
Thus "self-cleaning" ants.
"""

N = 150 #Grid dim ; needs to be at least double of α (max_dist)
#if bigger ns needed
#mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")

def collatz_ant(n, *args):
	S = np.zeros((N, N), dtype="int")
	#init pos
	x = y = N // 2

	# up, right, down, left
	dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

	dir_index = 0
	frames = [S.copy()]
	dists = []

	while n != 1:
		if n % 2 == 0:
			n /= 2
			dir_index = (dir_index + 1) % 4 #clockwise
		else:
			n = 3*n + 1
			dir_index = (dir_index - 1) % 4 #counter-clockwise

		S[x, y] = 1 - S[x, y] #flip
		x = (x + dirs[dir_index][0]) % N
		y = (y + dirs[dir_index][1]) % N
		dists.append(np.sqrt((x - N//2)**2 + (y- N//2)**2))

		frames.append(S.copy())
	steps = len(frames)
	max_dist = max(dists)
	return frames[-1], steps, dists[-1], max_dist

def check_self_cleaning_ants(n_i, n_f):

	#for self cleaning ants
	ns = []
	τs = []

	"""
	checking if α goes over N
	for self cleaning ants purpose
	doesn't matter, as it is very unlikely
	these will go very far from origin
	"""
	αs = []
	for n in range(n_i, n_f + 1):
		last_frame, τ, γ, α = collatz_ant(n)
		αs.append(α)
		Σ = np.sum(last_frame == 1)
		if Σ == 0:
			ns.append(n)
			τs.append(τ)
		if n % 50000 == 0:
			print(f"Progress: {(n/n_f) * 100:.2f}%")
	print(max(αs)) #checking N validity
	return ns, τs

if __name__ == "__main__":
	n_i = 2
	n_f = 1000000
	ns, τs = check_self_cleaning_ants(n_i, n_f)
	with open("sc_ants.txt", "w") as f:
		for n, τ in zip(ns, τs):
			line = f"{n}, {τ}"
			f.write(line + "\n")