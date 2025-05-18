import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
import mpmath

N = 100
S = np.zeros((N, N), dtype="int")
mpmath.mp.dps = 21
n = mpmath.mpf("1e20") + 92
pause_step     = 496   # max_step mark
pause_repeats  = 100    # how long frame stop

def collatz_ant(n):
    global S
    x = y = N // 2
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_index = 0
    frames, pos = [S.copy()], [(x, y)]
    while n != 1:
        if n % 2 == 0:
            n /= 2; dir_index = (dir_index + 1) % 4
        else:
            n = 3*n + 1; dir_index = (dir_index - 1) % 4
        S[x, y] = 1 - S[x, y]
        x = (x + dirs[dir_index][0]) % N
        y = (y + dirs[dir_index][1]) % N
        frames.append(S.copy())
        pos.append((x, y))
    return frames, pos

frames, pos = collatz_ant(n)

seq = list(range(len(frames)))
if pause_step < len(seq):
    seq = seq[:pause_step] + [pause_step]*pause_repeats + seq[pause_step:]

cmap = ListedColormap(["white", "black", "red"])
fig, ax = plt.subplots()
im = ax.imshow(frames[0], cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
plt.axis("off")

def animate(k):
    i = seq[k]
    grid = frames[i].copy()
    #paint red
    if i == pause_step:
        x, y = pos[i]
        grid[x, y] = 2

    im.set_array(grid)
    return [im]

ani = FuncAnimation(fig, animate, frames=len(seq), blit=True, interval=50)
ani.save("collatz_ant.gif", writer=PillowWriter(fps=30))
