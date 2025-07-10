import numpy as np
import matplotlib.pyplot as plt 
import mpmath

N = 100 #Grid dim ; needs to be at least double of α (max_dist)
mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")
n = 2
end = n + 50000
nums = [n + mpmath.mpf(i) for i in range(int(end - n))]

def collatz_ant(n, *args):
	S = np.zeros((N, N), dtype="int")
	#init pos
	x = y = N // 2

	# up, right, down, left
	dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

	dir_index = 0
	frames = [S.copy()]
	dists = []
	counter = 0
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
		if x == y == N // 2:
			counter += 1
		dists.append(np.sqrt((x - N//2)**2 + (y- N//2)**2))

		frames.append(S.copy())
	steps = len(frames) - 1
	max_dist = max(dists)
	return frames[-1], steps, dists[-1], max_dist, counter
 #collective
all_res = [collatz_ant(ns) for ns in nums]
frames = [frame[0] for frame in all_res]
steps = [step[1] for step in all_res]
dists = [dist[2] for dist in all_res] #γ	
max_dists = [max_dist[3] for max_dist in all_res] #α
counters = [counter[4] for counter in all_res] #Ω
print(max(max_dists))

Σ = [np.sum(k == 1) for k in frames]
#print(n + np.argwhere(np.array(Σ) == 0)) #for self-cleaning ants
norma_scores = np.array(Σ)/np.array(steps)
norma_dists = np.array(dists)/np.array(max_dists)
norma_counter = np.array(counters)/np.array(steps)

"""
plt.plot(range(len(nums)), norma_counter, "k.")
plt.ylabel("$\Omega_{n}/ τ_{n}$")
plt.xlabel("$n$")
plt.savefig("norma_counter.png", dpi=300, bbox_inches="tight")
"""

plt.figure(figsize=(6, 5))

hb = plt.hist2d(norma_scores, norma_counter, bins=100, cmap="coolwarm", cmin = 1)

cb = plt.colorbar(hb[3])
cb.set_label("Counts")

plt.xlabel(r"$\Sigma(n)/\tau_{n}$", fontsize=12)
plt.ylabel(r"$\Omega_{n}/\tau_{n}$", fontsize=12)

plt.tight_layout()
plt.savefig("norma_score_counter_2dhist.png", dpi=300)
plt.show()
