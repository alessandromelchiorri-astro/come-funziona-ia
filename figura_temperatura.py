"""Capitolo 8: la stessa distribuzione a quattro temperature (punteggi inventati)."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parole = ["tetto", "divano", "mobile", "tavolo", "frigorifero"]
logit = [3, 2.5, 2, 1.5, 0]
temperature = [1.5, 1, 0.5, 0.1]


def softmax(t):
    e = [math.exp(u / t) for u in logit]
    s = sum(e)
    return [x / s for x in e]


fig, assi = plt.subplots(1, 4, figsize=(4.65, 2.2), dpi=300, sharey=True)
for ax, t in zip(assi, temperature):
    p = softmax(t)
    print("tau =", t, [round(100 * x, 1) for x in p])
    ax.bar(range(5), [100 * x for x in p], color="#1f3a6b")
    ax.set_title("τ = %s" % str(t).replace(".", ","))
    ax.set_xticks(range(5))
    ax.set_xticklabels(parole, rotation=90)
    ax.set_ylim(0, 100)
fig.tight_layout()
fig.savefig("temperatura.png")
