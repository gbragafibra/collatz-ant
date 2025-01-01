import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import mpmath

N = 100  # Grid dim
mpmath.mp.dps = 22
start = mpmath.mpf("1e20")
end = start + 20
nums = [start + mpmath.mpf(i) for i in range(int(end - start))]
#gif
rows = 5
cols = 4
out_file = "collatz_ant_grid_attractors.png"
S = np.zeros((N, N), dtype = "int")

def collatz_ant(n):
    global S
    S = np.zeros((N, N), dtype = "int")
    #init pos
    x = y = N // 2

    # up, right, down, left
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    dir_index = 0
    frames = [S.copy()]

    while n != 1:
        if n % 2 == 0:
            n /= 2
            dir_index = (dir_index + 1) % 4 #clockwise
        else:
            n = 3*n + 1
            dir_index = (dir_index - 1) % 4 #counter-clockwise

        S[x, y] += 1
        x = (x + dirs[dir_index][0]) % N
        y = (y + dirs[dir_index][1]) % N

        frames.append(S.copy())
    return frames

# frames of all trajectories
all_frames = [collatz_ant(n) for n in nums]


fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
axes = axes.flatten()
ims = []
for i, ax in enumerate(axes):
    ax.axis("off")
    ims.append(ax.imshow(all_frames[i][-1], cmap="hot", interpolation="nearest"))


plt.savefig(out_file)
plt.close(fig)

print(f"Saved: {out_file}")
