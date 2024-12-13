### For multiple ns

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import mpmath
import os


N = 100 #Grid dim
S = np.zeros((N, N), dtype = "int")
mpmath.mp.dps = 32
start = mpmath.mpf("1e30")
end = start + 20
nums = [start + mpmath.mpf(i) for i in range(int(end - start))]
out_folder = "more_examples"

def collatz_ant(n, *args):
	global S
	S = np.zeros((N, N), dtype = "int") #reset
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

		S[x, y] = 1 - S[x, y] #flip
		x = (x + dirs[dir_index][0]) % N
		y = (y + dirs[dir_index][1]) % N

		frames.append(S.copy())
	return frames



def animate(i):
    im.set_array(frames[i])
    return [im]


for i, n in enumerate(nums):
	frames = collatz_ant(n)
	fig, ax = plt.subplots()
	im = ax.imshow(S, cmap="binary", interpolation="nearest")
	plt.title(f"n = {float(n):.2e}")
	plt.axis("off")

	ani = FuncAnimation(fig, animate, frames=len(frames), blit=True, interval=50)
	writer = PillowWriter(fps=30)
	out_name = os.path.join(out_folder, f"collatz_ant{i + 1}.gif")
	ani.save(out_name, writer=writer)
	plt.close(fig)
	print(f"Saved: {out_name}")

