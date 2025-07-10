import numpy as np
import matplotlib.pyplot as plt 
import mpmath


from scipy.ndimage import label

def compute_num(S):
    structure = np.array([[0,1,0],
                          [1,1,1],
                          [0,1,0]])
    labeled, num_features = label(S, structure=structure)
    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0
    return sizes.max()


N = 100 #Grid dim ; needs to be at least double of α (max_dist)
mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")
n = 2
end = n + 50000
nums = [n + mpmath.mpf(i) for i in range(int(end - n))]

def collatz_ant(n, *args):
	S = np.zeros((N, N), dtype="int")
	visited = np.zeros((N, N), dtype=bool) 

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
		visited[x, y] = True
		x = (x + dirs[dir_index][0]) % N
		y = (y + dirs[dir_index][1]) % N
		dists.append(np.sqrt((x - N//2)**2 + (y- N//2)**2))

		frames.append(S.copy())
	steps = len(frames) - 1
	max_dist = max(dists)
	space = np.sum(visited) #space(n) func
	num = compute_num(frames[-1])
	return frames[-1], steps, dists[-1], max_dist, space, num

all_res = [collatz_ant(ns) for ns in nums]
frames = [frame[0] for frame in all_res]
steps = [step[1] for step in all_res]
dists = [dist[2] for dist in all_res] #γ	
max_dists = [max_dist[3] for max_dist in all_res] #α
spaces = [space[4] for space in all_res] #space(n)
nums = [num[5] for num in all_res] #num(n)

print(max(max_dists))


Σ = [np.sum(k == 1) for k in frames]
#print(n + np.argwhere(np.array(Σ) == 0)) #for self-cleaning ants
norma_scores = np.array(Σ)/np.array(steps)
norma_dists = np.array(dists)/np.array(max_dists)
norma_spaces = np.array(spaces)/np.array(steps)
norma_nums = np.array(nums)/np.array(steps)

score_spaces_norma = np.array(Σ)/np.array(spaces)
nums = np.array(nums)
Σ = np.array(Σ)
# given num(n) <= Σ(n) can just do this
num_score_norma = np.zeros_like(nums, dtype=float)
valid = (nums != 0) & (Σ != 0)
num_score_norma[valid] = nums[valid] / Σ[valid]

p = plt.scatter(range(len(nums)), norma_spaces, c = norma_dists, s = 0.05, cmap= "coolwarm_r")
plt.colorbar(p, label = "$γ/α$")
plt.ylabel("$space(n)/τ_{n}$")
#plt.gca().set_xticklabels([])
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")