import numpy as np
import matplotlib.pyplot as plt 
import mpmath

N = 200 #Tape dim ; needs to be at least double of α (max_dist)
mpmath.mp.dps = 101
#n = mpmath.mpf("1e100")
n = 2
end = n + 100
nums = [n + mpmath.mpf(i) for i in range(int(end - n))]

def collatz_tape(n, machine = False, max_steps = 100000, *args):
    S = np.zeros(N, dtype="int")
    x = N // 2
    dirs = [1, -1]
    frames = [S.copy()]
    dists = []

    steps = 0

    while n != 1 and steps < max_steps:
        par = int(n % 2)
        if par == 0:
            n /= 2
        else:
            n = 3 * n + 1

        if n != 1: #Option for state to affect dynamics
            if machine and S[x] == 1:
                n += 1

        S[x] = 1 - S[x]
        x = (x + dirs[par]) % N
        dists.append(abs(x - N // 2))

        frames.append(S.copy())
        steps += 1

    if steps >= max_steps:
        return "Max steps exceeded (possible non-halting)", steps, max(dists), np.sum(S == 1), False

    return "Halted", steps, max(dists), np.sum(S == 1), True

if __name__ == "__main__":
    n_i = 2
    n_f = n_i + 20
    halt_count = 0
    halt_ratios = []
    ns = []

    Σ_τ_ratios = []

    for n in range(n_i, n_f + 1):
        result = collatz_tape(n, machine=True, max_steps=100000)
        status, steps, max_dist, Σ, halted = result
        if halted:
            halt_count += 1
            Σ_τ_ratios.append(Σ / steps)
        total = n - n_i + 1
        ratio = halt_count / total
        halt_ratios.append(ratio)
        ns.append(n)
        print(f"n={n}: {status}, steps={steps}, max_dist={max_dist}, Σ={Σ}, halted={halted}")

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    axs[0].plot(ns, halt_ratios, "b")
    axs[0].set_xlabel("$n$")
    axs[0].set_ylabel("Halt Count / Total")

    axs[1].hist(Σ_τ_ratios, bins=100, color="blue", edgecolor="black")
    axs[1].set_xlabel("$Σ(n)/τ_{n}$")
    axs[1].set_ylabel("Count")

    plt.tight_layout()
    plt.savefig("halt_tape_counts.png", dpi=300, bbox_inches="tight")