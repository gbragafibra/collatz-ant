import numpy as np
import matplotlib.pyplot as plt
import mpmath

mpmath.mp.dps = 21
num = mpmath.mpf("1e20") + 99

out_file = "collatz_ant_dists.png"

def collatz_ant(n):
    """
    No limitation of having to initiate a matrix
    pre-stating (N, N) shape to keep track of state
    of collatz_ant.
    Can merely keep track of position index without
    care wrt the state representation.
    """

    #init pos
    x = y = 0

    dists, angles = [], [] #euclidean distances, angles

    # up, right, down, left
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_index = 0
    while n != 1:
        if n % 2 == 0:
            n /= 2
            dir_index = (dir_index + 1) % 4 #clockwise
        else:
            n = 3*n + 1
            dir_index = (dir_index - 1) % 4 #counter-clockwise

        x = (x + dirs[dir_index][0])
        y = (y + dirs[dir_index][1])
        dist = np.sqrt(x**2 + y**2) #wrt origin (0, 0)
        dists.append(dist)
        angles.append(np.arctan2(y, x)) #in radians

    return dists, angles

dists, angles = collatz_ant(num)
steps = np.arange(len(dists))

fig, (ax_r, ax_theta) = plt.subplots(1, 2, sharex=True, figsize=(8, 5))

ax_r.plot(steps, dists, "k-")
ax_r.set_ylabel(r"$\|x\|_{2}$")

ax_theta.plot(steps, angles, "r-")
ax_theta.set_xlabel("Step")
ax_theta.set_ylabel(r"$\theta$ (rad)")

pi = np.pi
yticks = [-pi, -0.5*pi, 0, 0.5*pi, pi]
ax_theta.set_yticks(yticks)
ax_theta.set_yticklabels([r"$-\pi$", r"$-\frac{\pi}{2}$",
                          r"$0$",    r"$\frac{\pi}{2}$", r"$\pi$"])

fig.tight_layout()
plt.show()