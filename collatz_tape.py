import numpy as np
import matplotlib.pyplot as plt 
import mpmath

N = 100 #Tape dim ; needs to be at least double of α (max_dist)
mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")
n = 2
end = n + 50000
nums = [n + mpmath.mpf(i) for i in range(int(end - n))]


def collatz_tape(n, *args):
	S = np.zeros(N, dtype="int")
	visited = np.zeros(N, dtype=bool)
	#init pos
	x = N // 2

	#right, left
	dirs = [1, -1]
	frames = [S.copy()]
	dists = []

	# even (move right); odd (move left)
	while n != 1:
		par = int(n % 2) #parity
		if par == 0:
			n /= 2
		else:
			n = 3*n + 1

		S[x] = 1 - S[x] #flip
		visited[x] = True
		x = (x + dirs[par]) % N
		dists.append(abs(x - N // 2))

		frames.append(S.copy())
	steps = len(frames) - 1 #don't want to count the initial empty frame
	max_dist = max(dists) # == dists[-1] -> 1D case
	Σ = np.sum(frames[-1] == 1)
	space = np.sum(visited) #space(n) func
	return steps, max_dist, Σ, space

all_res = [collatz_tape(ns) for ns in nums]
τs = [res[0] for res in all_res]
αs = [res[1] for res in all_res]
Σs = [res[2] for res in all_res]
spaces = [res[3] for res in all_res]
print(max(αs)) # to acess if N is valid
norma_scores = np.array(Σs)/np.array(τs)
norma_spaces = np.array(spaces)/np.array(τs)
norma_dists = np.array(αs)/np.array(τs)

#print(n + np.argwhere(np.array(norma_scores) == 1)) #2^k

p = plt.scatter(range(len(nums)), norma_scores, c = norma_dists, s = 0.05, cmap= "coolwarm_r")
plt.colorbar(p, label = "$α/τ_{n}$")
plt.ylabel("$Σ(n)/τ_{n}$")
#plt.gca().set_xticklabels([])
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")
