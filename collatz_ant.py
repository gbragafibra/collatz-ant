import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation, PillowWriter
import mpmath


N = 100 #Grid dim
S = np.zeros((N, N), dtype = "int")
mpmath.mp.dps = 201
n = mpmath.mpf("1e200")
#n = 1e3

def collatz_ant(n, *args):
	global S
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

frames = collatz_ant(n)

fig, ax = plt.subplots()
im = ax.imshow(S, cmap="binary", interpolation="nearest")
plt.title(f"n = {float(n):.2e}")
plt.axis("off")

def animate(i):
    im.set_array(frames[i])
    return [im]

ani = FuncAnimation(fig, animate, frames=len(frames), blit=True, interval=50)
writer = PillowWriter(fps=30)
ani.save(f"collatz_ant.gif", writer=writer)
#ani.save(f"collatz_ant{n}.gif", writer=writer)