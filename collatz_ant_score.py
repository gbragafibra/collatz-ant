import numpy as np
import matplotlib.pyplot as plt 
import mpmath

N = 100 #Grid dim ; needs to be at least double of α (max_dist)
mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")
n = 2
end = n + 1000
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
 #collective
all_res = [collatz_ant(ns) for ns in nums]
frames = [frame[0] for frame in all_res]
steps = [step[1] for step in all_res]
dists = [dist[2] for dist in all_res] #γ	
max_dists = [max_dist[3] for max_dist in all_res] #α
print(max(max_dists))

Σ = [np.sum(k == 1) for k in frames]
norma_scores = np.array(Σ)/np.array(steps)
norma_dists = np.array(dists)/np.array(max_dists)
p = plt.scatter(range(len(nums)), norma_scores, c = norma_dists, s = 0.05, cmap= "coolwarm_r")
plt.colorbar(p, label = "$γ/α$")
plt.ylabel("$Σ(n)/τ_{n}$")
#plt.gca().set_xticklabels([])
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
	n = 500
	frames, steps, dist, max_dist = collatz_ant(n)
	Σ = np.sum(frames == 1)
	norma_scores = Σ/steps
	print(dist/max_dist) #γ/α
	print(norma_scores)
	print(Σ)
	print(steps)


""" #Tracking Σ(n) over iterations
 #individual (same landscapes)
n1 = mpmath.mpf("1e10") + 1
n2 = mpmath.mpf("1e10") + 3
frames1 = collatz_ant(n1)
Σ1 = [np.sum(frame == 1) for frame in frames1]

frames2 = collatz_ant(n2)
Σ2 = [np.sum(frame == 1) for frame in frames2]

plt.plot(range(len(frames1)), Σ1, "k-", label = "$n = 10^{10} + 93$")
plt.plot(range(len(frames2)), Σ2, "r-", label = "$n = 10^{10} + 94$")
plt.legend()
plt.ylabel("$Σ(n_{τ})$")
plt.xlabel("Step $τ$")
plt.show()
"""

