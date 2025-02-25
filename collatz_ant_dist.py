import numpy as np
import matplotlib.pyplot as plt
import mpmath

mpmath.mp.dps = 152
num = mpmath.mpf("1e150")

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

    dists = [] #euclidean distances

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

    return dists

dists = collatz_ant(num)
plt.plot(np.arange(len(dists)), dists, "k.")
plt.xlabel("Step")
plt.ylabel("$\|x\|_{2}$")
plt.savefig(out_file, bbox_inches="tight")
plt.close()
#plt.show()

if __name__ == "__main__":
    """
    To get an idea of what max euclidean distance
    is reached for a given n in interval ∈ [start, end],
    and the corresponding step/total_step ratio at which
    such max_dist is first reached
    """
    mpmath.mp.dps = 152
    start = mpmath.mpf("1e150")
    #start = 2
    end = start + 1000
    nums = [start + mpmath.mpf(i) for i in range(int(end - start))]
    dists = [collatz_ant(num) for num in nums]
    maxs = [max(dist) for dist in dists]
    plt.plot(np.arange(len(nums)), maxs, "k.")
    plt.ylabel("Max distance")
    #max_step_ratio = [np.argmax(dist)/len(dist) for dist in dists] #step at which max dist is first reached
    #plt.plot(np.arange(len(nums)), max_step_ratio, "k.")
    plt.show()