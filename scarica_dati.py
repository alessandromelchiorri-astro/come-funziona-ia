"""Scarica il campione del corpus Europarl distribuito con NLTK (pacchetto europarl_raw)."""
import io
import os
import urllib.request
import zipfile

URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/europarl_raw.zip"
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dati")
os.makedirs(dest, exist_ok=True)
with urllib.request.urlopen(URL) as risposta:
    zipfile.ZipFile(io.BytesIO(risposta.read())).extractall(dest)
print("Corpus estratto in", os.path.join(dest, "europarl_raw"))
