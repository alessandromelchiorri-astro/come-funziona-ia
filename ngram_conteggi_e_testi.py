"""Capitoli 1 e 5: conteggi di coppie e testi generati con modelli sempre più ricchi.
Usa tutte e dieci le sedute in italiano."""
import collections
import random
import re
from comune import file_lingua, leggi, parole_ngram

testo = "".join(leggi(f) + "\n" for f in file_lingua("italian"))
toks = parole_ngram(testo)
uni = collections.Counter(toks)
big = collections.defaultdict(collections.Counter)
tri = collections.defaultdict(collections.Counter)
for a, b in zip(toks, toks[1:]):
    big[a][b] += 1
for a, b, c in zip(toks, toks[1:], toks[2:]):
    tri[(a, b)][c] += 1
print("parole (token):", len(toks), "diverse:", len(uni))

# Riquadro del capitolo 5: che cosa viene dopo una parola
for ctx in ["Signor", "Unione", "diritti"]:
    c = big[ctx]
    s = sum(c.values())
    print(ctx, "->", [(w, round(100 * n / s, 1)) for w, n in c.most_common(4)])


def genera(ordine, n, seme):
    rnd = random.Random(seme)
    if ordine == 0:  # parole a caso, tutte con la stessa probabilità
        voc = list(uni)
        return " ".join(rnd.choice(voc) for _ in range(n))
    if ordine == 1:  # parole a caso, con la loro frequenza
        ws, cs = zip(*uni.items())
        return " ".join(rnd.choices(ws, cs, k=n))
    # coppie (ordine 2) o triple (ordine 3, con ritorno alla coppia se la tripla è nuova)
    inizi = [b for a, b in zip(toks, toks[1:]) if a == "."][:5000]
    cur = rnd.choice(inizi)
    out, prev = [cur], None
    while len(out) < n:
        c = big[cur] if (ordine == 2 or prev is None) else (tri[(prev, cur)] or big[cur])
        ws, cs = zip(*c.items())
        nxt = rnd.choices(ws, cs)[0]
        out.append(nxt)
        prev, cur = cur, nxt
    return " ".join(out)


# Riquadro del capitolo 1: testi generati
for ordine in (0, 1, 2, 3):
    for seme in (1, 2, 3):
        s = re.sub(r" ([.,;:!?])", r"\1", genera(ordine, 22, seme))
        print(ordine, seme, s)
