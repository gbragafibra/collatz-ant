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
	ns = [n]
	dists = []
	while n != 1:
		if n % 2 == 0:
			n /= 2
			dir_index = (dir_index + 1) % 4 #clockwise
			ns.append(n)
		else:
			n = 3*n + 1
			dir_index = (dir_index - 1) % 4 #counter-clockwise
			ns.append(n)

		S[x, y] = 1 - S[x, y] #flip
		x = (x + dirs[dir_index][0]) % N
		y = (y + dirs[dir_index][1]) % N
		dists.append(np.sqrt((x - N//2)**2 + (y- N//2)**2))

		frames.append(S.copy())
	steps = len(frames) - 1
	Σ = [np.sum(frame == 1) for frame in frames]
	Σ_max_idx = np.argmax(Σ)
	α_idx = np.argmax(dists)
	Σ_max = max(Σ)
	n_Σ_max = ns[Σ_max_idx]
	n_α = ns[α_idx]
	n_max = max(ns)
	max_dist = max(dists) #α
	return steps, Σ_max, n_Σ_max, Σ[-1], n_max, Σ_max_idx, max_dist, dists[-1], α_idx, n_α

all_res = [collatz_ant(ns) for ns in nums]
steps = [res[0] for res in all_res]
Σ_maxs = [res[1] for res in all_res]
n_Σ_maxs = [res[2] for res in all_res]
last_Σ = [res[3] for res in all_res]
n_max = [res[4] for res in all_res]
Σ_max_idxs = [res[5] for res in all_res]
αs = [res[6] for res in all_res]
γs = [res[7] for res in all_res]
α_idxs = [res[8] for res in all_res]
n_αs = [res[9] for res in all_res]


norma_scores = np.array(last_Σ)/np.array(Σ_maxs)
norma_ns = np.array(n_Σ_maxs)/np.array(n_max)
norma_ns_idxs = np.array(Σ_max_idxs)/np.array(steps)
norma_score_dist_idxs = np.array(α_idxs)/np.array(Σ_max_idxs)
norma_ns_score_dist = np.array(n_Σ_maxs)/np.array(n_αs)
norma_max_dist_score = np.array(αs)/np.array(Σ_maxs)
norma_score_dist_last = np.array(last_Σ)/np.array(γs)
norma_dist_idxs = np.array(α_idxs)/np.array(steps)


#print(n + np.argwhere(np.array(norma_ns) == 1))

p = plt.scatter(range(len(nums)), norma_dist_idxs, c = norma_scores, s = 0.05, cmap= "coolwarm_r")
plt.colorbar(p, label = "$Σ(n)^{last}/Σ(n)^{max}$")
plt.ylabel(r"$τ_{α}/τ$")
#plt.gca().set_xticklabels([])
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")

"""
plt.plot(range(len(nums)), norma_scores, "k.")
plt.ylabel("$Σ(n)^{last}/Σ(n)^{max}$")
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")
"""