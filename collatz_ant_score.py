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
	steps = len(frames) - 1 #don't want to count the initial empty frame
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
#print(n + np.argwhere(np.array(Σ) == 0)) #for self-cleaning ants
norma_scores = np.array(Σ)/np.array(steps)
norma_dists = np.array(dists)/np.array(max_dists)

"""
μ = np.mean(norma_scores)
σ = np.std(norma_scores)
plt.figure(figsize=(6, 4))
plt.hist(norma_scores, bins=100, color="skyblue", edgecolor="black")

plt.axvline(μ, color="red", linestyle="--", linewidth=1.5, label=f"$μ$")
plt.axvline(μ - σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvline(μ + σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvline(μ - 2*σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvline(μ + 2*σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvline(μ - 3*σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvline(μ + 3*σ, color="gray", linestyle=":", linewidth=1.2)
plt.axvspan(μ - σ, μ + σ, color='gray', alpha=0.2, label=r"$\mu \pm \sigma$")


plt.xlabel("$Σ(n)/τ_{n}$", fontsize=12)
plt.ylabel("Counts", fontsize=12)
#plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("norma_score_histogram.png", dpi=300)
plt.show()

plt.figure(figsize=(6, 5))

hb = plt.hist2d(norma_scores, norma_dists, bins=100, cmap="coolwarm", cmin = 1)

cb = plt.colorbar(hb[3])
cb.set_label("Counts")

plt.xlabel(r"$\Sigma(n)/\tau_{n}$", fontsize=12)
plt.ylabel(r"$\gamma/\alpha$", fontsize=12)

plt.tight_layout()
plt.savefig("norma_score_2dhist.png", dpi=300)
plt.show()
"""

p = plt.scatter(range(len(nums)), norma_scores, c = norma_dists, s = 0.05, cmap= "coolwarm_r")
plt.colorbar(p, label = "$γ/α$")
plt.ylabel("$Σ(n)/τ_{n}$")
#plt.gca().set_xticklabels([])
plt.xlabel("$n$")
plt.savefig("norma_score.png", dpi=300, bbox_inches="tight")

"""
if __name__ == "__main__":
	n = 500
	frames, steps, dist, max_dist = collatz_ant(n)
	Σ = np.sum(frames == 1)
	norma_scores = Σ/steps
	print(dist/max_dist) #γ/α
	print(norma_scores)
	print(Σ)
	print(steps)
"""

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

