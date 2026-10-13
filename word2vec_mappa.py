"""Capitolo 6: una piccola mappa dei significati con word2vec (gensim)."""
import re
from gensim.models import Word2Vec
from comune import file_lingua

frasi = []
for f in file_lingua("italian"):
    for riga in open(f, encoding="utf-8"):
        ws = re.findall(r"[^\W\d_]+", riga.lower())
        if len(ws) > 2:
            frasi.append(ws)
m = Word2Vec(frasi, vector_size=100, window=5, min_count=5, workers=1, sg=1, epochs=15, seed=42)
for w in ["italia", "lunedì", "commissione", "aumentare", "acqua", "inglese", "uomini", "pesca", "bambini"]:
    if w in m.wv:
        print(w, [(x, round(s, 2)) for x, s in m.wv.most_similar(w, topn=6)])
print("francia - parigi + roma:", m.wv.most_similar(positive=["roma", "francia"], negative=["parigi"], topn=5))
