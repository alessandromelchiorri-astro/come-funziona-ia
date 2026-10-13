"""Funzioni comuni: lettura e pulizia del corpus Europarl (campione NLTK)."""
import glob
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.join(QUI, "dati", "europarl_raw")

# Seduta tenuta da parte per sorpresa e perplessità (14 febbraio 2000).
SEDUTA_DI_PROVA = "ep-00-02-14"


def file_lingua(lingua):
    """Elenco ordinato dei file di una lingua ('italian' o 'english')."""
    return sorted(glob.glob(os.path.join(DATI, lingua, "*")))


def pulisci(testo):
    """Il corpus ha la punteggiatura staccata: la riattacchiamo, con gli apostrofi."""
    testo = re.sub(r" ([.,;:!?)\]])", r"\1", testo)
    testo = re.sub(r"([(\[]) ", r"\1", testo)
    testo = re.sub(r" ' ", "'", testo)
    testo = re.sub(r"(\w)' (\w)", r"\1'\2", testo)
    return testo


def leggi(percorso):
    return pulisci(open(percorso, encoding="utf-8").read())


def parole_ngram(testo):
    """Parole per i modelli a n-gram: lettere (con eventuale apostrofo finale),
    numeri e i segni . , ; : ! ? come parole a sé; maiuscole distinte."""
    return re.findall(r"[^\W\d_]+'?|[0-9]+|[.,;:!?]", testo)


def nome_seduta(percorso):
    return os.path.basename(percorso)[:-3]
