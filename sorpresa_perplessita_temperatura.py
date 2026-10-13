"""Capitoli 8, 9, 11 e 12: modello a triple con interpolazione.
Addestrato su nove sedute; la seduta del 14 febbraio 2000 è tenuta da parte."""
import collections
import math
import os
import random
import re
from comune import QUI, SEDUTA_DI_PROVA, file_lingua, leggi, nome_seduta, parole_ngram

files = file_lingua("italian")
train = [w for f in files if nome_seduta(f) != SEDUTA_DI_PROVA for w in parole_ngram(leggi(f))]
test = [w for f in files if nome_seduta(f) == SEDUTA_DI_PROVA for w in parole_ngram(leggi(f))]
U = collections.Counter(train)
N = len(train)
V = len(U) + 1  # +1 per le parole mai viste
B = collections.defaultdict(collections.Counter)
T = collections.defaultdict(collections.Counter)
for a, b in zip(train, train[1:]):
    B[a][b] += 1
for a, b, c in zip(train, train[1:], train[2:]):
    T[(a, b)][c] += 1


def p(w, u, v, pesi=(0.6, 0.3, 0.1)):
    """Media pesata delle stime da triple, coppie e singole parole.
    - Vocabolario: le parole delle nove sedute di addestramento più una parola
      speciale «sconosciuta», che rappresenta qualunque parola mai vista.
    - Singole parole: a ogni voce del vocabolario si aggiunge un'occorrenza
      fittizia, così nessuna parola ha probabilità zero.
    - Contesti mai visti: se la coppia (u, v) o la parola v non compaiono mai
      come contesto, la loro stima non è disponibile e i pesi delle stime
      rimanenti vengono riscalati in modo da sommare a 1."""
    stime = [(pesi[2], (U.get(w, 0) + 1) / (N + V))]
    cb = B.get(v)
    if cb:
        stime.append((pesi[1], cb[w] / sum(cb.values())))
    ct = T.get((u, v))
    if ct:
        stime.append((pesi[0], ct[w] / sum(ct.values())))
    totale = sum(l for l, _ in stime)
    return sum(l * q for l, q in stime) / totale


def perplessita(ws):
    s = sum(-math.log(p(ws[i], ws[i - 2], ws[i - 1])) for i in range(2, len(ws)))
    return math.exp(s / (len(ws) - 2))


print("perplessità sulla seduta tenuta da parte: %.0f" % perplessita(test))
pref = re.sub(r"[#*_]", "", open(os.path.join(QUI, "prefazione.txt"), encoding="utf-8").read())
print("perplessità sulla prefazione del libro: %.0f" % perplessita(parole_ngram(pref)))

for frase in ["Signor Presidente, vorrei ringraziare la Commissione per il suo lavoro.",
              "Signor Presidente, vorrei ringraziare la Commissione per il suo gatto."]:
    ws = ["."] + parole_ngram(frase)
    righe = [(ws[i], p(ws[i], ws[i - 2], ws[i - 1])) for i in range(2, len(ws))]
    print(frase)
    for w, q in righe:
        print("  %-12s %9.4f%%  sorpresa %.2f" % (w, 100 * q, -math.log(q)))
    print("  sorpresa media %.2f" % (sum(-math.log(q) for _, q in righe) / len(righe)))


def campiona(inizio, n, tau, seme):
    """La temperatura si applica elevando i conteggi alla potenza 1/tau."""
    rnd = random.Random(seme)
    out = parole_ngram(inizio)
    k = len(out)
    while len(out) < k + n:
        c = T.get((out[-2], out[-1])) or B.get(out[-1])
        ws, cs = zip(*c.items())
        out.append(rnd.choices(ws, [x ** (1 / tau) for x in cs])[0])
    s = re.sub(r" ([.,;:!?])", r"\1", " ".join(out))
    return s.replace("' ", "'")


for tau in (0.2, 1.0, 2.5):
    for seme in (4, 5):
        print("tau=%.1f" % tau, campiona("Signor Presidente,", 24, tau, seme))
for seme in (1, 2, 3):
    print("domanda:", campiona("Qual è la capitale dell'Italia?", 20, 1.0, seme))
