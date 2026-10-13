"""Capitolo 5: quante coppie e triple di una seduta nuova mancano nelle altre nove."""
import collections
from comune import SEDUTA_DI_PROVA, file_lingua, leggi, nome_seduta, parole_ngram

files = file_lingua("italian")
train = [w for f in files if nome_seduta(f) != SEDUTA_DI_PROVA for w in parole_ngram(leggi(f))]
test = [w for f in files if nome_seduta(f) == SEDUTA_DI_PROVA for w in parole_ngram(leggi(f))]
print("addestramento:", len(train), "prova:", len(test))
c2 = set(zip(train, train[1:]))
c3 = set(zip(train, train[1:], train[2:]))
t2 = list(zip(test, test[1:]))
t3 = list(zip(test, test[1:], test[2:]))
print("coppie mai viste: %.1f%%" % (100 * sum(b not in c2 for b in t2) / len(t2)))
print("triple mai viste: %.1f%%" % (100 * sum(b not in c3 for b in t3) / len(t3)))
print("«gatto» nelle nove sedute:", collections.Counter(train).get("gatto", 0))
