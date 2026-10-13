"""Capitolo 5: quanti token servono all'italiano rispetto all'inglese.
Usa le nove sedute presenti in entrambe le lingue."""
import os
import re
import mistral_common
from mistral_common.tokens.tokenizers.sentencepiece import SentencePieceTokenizer
from mistral_common.tokens.tokenizers.tekken import Tekkenizer
from comune import file_lingua, leggi, nome_seduta

d = os.path.join(os.path.dirname(mistral_common.__file__), "data")
tekken = Tekkenizer.from_file(os.path.join(d, "tekken_240911.json"))  # 131.072 token
vecchio = SentencePieceTokenizer(os.path.join(d, "tokenizer.model.v1"))  # 32.000 token
it = {nome_seduta(f): f for f in file_lingua("italian")}
en = {nome_seduta(f): f for f in file_lingua("english")}
comuni = sorted(set(it) & set(en))
print("sedute comuni:", len(comuni))
ris = {}
for nome, mappa in (("IT", it), ("EN", en)):
    t = "".join(leggi(mappa[s]) + "\n" for s in comuni)
    parole = len(re.findall(r"[^\W\d_]+", t))
    n1 = len(tekken.encode(t, bos=False, eos=False))
    n2 = len(vecchio.encode(t, bos=False, eos=False))
    ris[nome] = (parole, n1, n2)
    print(nome, "parole", parole, "| Tekken", n1, "(%.2f per parola)" % (n1 / parole),
          "| vecchio", n2, "(%.2f per parola)" % (n2 / parole))
print("italiano/inglese: parole %.3f, token Tekken %.3f, token vecchio %.3f" % (
    ris["IT"][0] / ris["EN"][0], ris["IT"][1] / ris["EN"][1], ris["IT"][2] / ris["EN"][2]))
