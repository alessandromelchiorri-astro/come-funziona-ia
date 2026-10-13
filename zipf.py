"""Capitolo 10: la legge di Zipf sulle dieci sedute in italiano (parole in minuscolo)."""
import collections
import re
import sys
from comune import file_lingua, leggi, parole_ngram

parole = []
for f in file_lingua("italian"):
    parole += [w.lower() for w in parole_ngram(leggi(f)) if re.match(r"[^\W\d_]", w)]
c = collections.Counter(parole).most_common()
N = len(parole)
print("parole:", N, "diverse:", len(c), "usate una sola volta: %.0f%%" % (100 * sum(1 for _, n in c if n == 1) / len(c)))
for k in (10, 100, 1000):
    print("le prime %d parole coprono il %.1f%% del testo" % (k, 100 * sum(n for _, n in c[:k]) / N))
print("rango 1, 10, 100, 1000, 10000:", [(r, c[r - 1]) for r in (1, 10, 100, 1000, 10000)])
if "--figura" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.65, 2.9), dpi=300)
    ax.loglog(range(1, len(c) + 1), [n for _, n in c], color="#1f3a6b")
    ax.loglog([1, len(c)], [c[0][1], c[0][1] / len(c)], color="#9a9a9a", ls="--")
    ax.set_xlabel("Posizione nella classifica (rango)")
    ax.set_ylabel("Numero di occorrenze")
    fig.tight_layout()
    fig.savefig("zipf.png")
