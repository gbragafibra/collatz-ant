import numpy as np
import matplotlib.pyplot as plt 
import mpmath
import matplotlib.animation as animation


def collatz_tape(n, machine =False, max_steps=100000, return_frames=False):
    S = np.zeros(N, dtype="int")
    x = N // 2
    dirs = [1, -1]
    frames = [S.copy()]
    dists = []
    ns_at_step = [n] 
    steps = 0
    halted = False

    while n != 1 and steps < max_steps:
        par = int(n % 2)
        if par == 0:
            n /= 2
        else:
            n = 3 * n + 1

        if n != 1 and machine and S[x] == 1:
            n += 1

        S[x] = 1 - S[x]
        x = (x + dirs[par]) % N
        dists.append(abs(x - N // 2))

        frames.append(S.copy())
        ns_at_step.append(n)  
        steps += 1

    if n == 1:
        halted = True

    status = "Halted" if halted else "Possible non-halting"
    max_dist = max(dists) if dists else 0
    Σ = np.sum(frames[-1] == 1)

    if return_frames:
        if not halted:
            frames = frames[:501] #first k steps
            ns_at_step = ns_at_step[:501] 
        return status, steps, max_dist, Σ, frames, ns_at_step
    return status, steps, max_dist, Σ

def visualize_frames(frames, ns_at_step, title = None): #tape developing downwards
    fig, ax = plt.subplots(figsize=(12, len(frames) * 0.15))
    tape_matrix = np.array(frames)
    ax.imshow(tape_matrix, cmap="Greys", interpolation="none")

    #ax.set_ylabel("$n$")
    ax.set_xticks([])

    ax.set_yticks(np.arange(len(ns_at_step)))
    ax.set_yticklabels(ns_at_step, fontsize=5)
    ax.set_yticks([]) 

    for spine in ax.spines.values():
        spine.set_visible(False)
     

    #ax.set_title(title)
    plt.tight_layout()
    plt.savefig("developed_collatz_tape.png", dpi=300, bbox_inches="tight")

def visualize_frames2(frames, ns_at_step, title=None): #tape develop as gif
    tape_length = len(frames[0])
    fig, ax = plt.subplots(figsize=(tape_length * 0.1, 1))
    
    data = np.expand_dims(frames[0], axis=0)
    im = ax.imshow(data, cmap="Greys", interpolation="none", vmin=0, vmax=1)
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    def update(i):
        data = np.expand_dims(frames[i], axis=0)
        im.set_data(data)
        return [im]

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(frames),
        interval=200,
        blit=False,
    )

    ani.save("collatz_tape.gif", writer="pillow", fps=10)
    plt.close(fig)

if __name__ == "__main__":
    N = 100
    mpmath.mp.dps = 101
    n = 19
    status, steps, max_dist, Σ, frames, ns_at_step = collatz_tape(n, machine=True, return_frames=True)
    print(f"n={n}: {status}, τ = {steps}, α = {max_dist}, Σ = {Σ}")
    visualize_frames(frames, ns_at_step, title=f"$n = {n}$ ({status})")
    visualize_frames2(frames, ns_at_step, title=f"$n = {n}$ ({status})")
