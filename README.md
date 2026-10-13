# Codice dei riquadri «Proviamo»

Questo pacchetto permette di ripetere i calcoli dei riquadri «Proviamo» del libro
*Come funziona l'intelligenza artificiale?* di Alessandro Melchiorri (testo aggiornato al 13 ottobre 2026).

## Preparazione

Serve Python 3.10 o successivo (i calcoli del libro sono stati fatti con Python 3.13).

    pip install -r requirements.txt
    python scarica_dati.py

Il secondo comando scarica il campione del corpus Europarl distribuito con NLTK
(pacchetto `europarl_raw`) nella cartella `dati/`.

## Script e riquadri

| Script | Capitolo | Che cosa calcola |
| --- | --- | --- |
| `ngram_conteggi_e_testi.py` | 1 e 5 | conteggi di coppie («Signor» → «Presidente») e testi generati con modelli sempre più ricchi |
| `coppie_mai_viste.py` | 5 | coppie e triple di una seduta nuova mai viste nelle altre nove |
| `token_it_en.py` | 5 | token per parola in italiano e in inglese (Tekken e vecchio tokenizzatore da 32.000 token) |
| `word2vec_mappa.py` | 6 | parole vicine nella «mappa dei significati» |
| `sorpresa_perplessita_temperatura.py` | 8, 9, 11, 12 | sorpresa parola per parola, perplessità, temperatura, il modello che «continua ma non risponde» |
| `zipf.py` | 10 | legge di Zipf (con `--figura` disegna anche il grafico) |
| `conti_grandi_modelli.py` | 13 | memoria, calcolo e tempo per Llama 2 da 70 miliardi, LoRA, modelli a esperti |
| `figura_temperatura.py` | 8 | la figura con le distribuzioni a quattro temperature |

## Scelte di metodo

- **Pulizia.** Nel corpus la punteggiatura è staccata dalle parole; il testo viene ricomposto riattaccando segni di punteggiatura e apostrofi (`comune.py`).
- **Parole.** Per i modelli a n-gram sono «parole» le sequenze di lettere, con l'eventuale apostrofo finale («dell'»), i numeri e i segni `. , ; : ! ?`; maiuscole e minuscole sono distinte. Per Zipf e word2vec si usano solo le parole, in minuscolo.
- **Seduta di prova.** Per sorpresa e perplessità la seduta del 14 febbraio 2000 (`ep-00-02-14`, circa 29.000 parole) è tenuta da parte; il modello è addestrato sulle altre nove.
- **Vocabolario e probabilità non nulle.** Il vocabolario contiene le parole delle nove sedute di addestramento più una voce speciale che rappresenta tutte le parole mai viste. La probabilità di una parola è la media pesata delle stime da triple (0,6), coppie (0,3) e singole parole (0,1); alle singole parole si aggiunge un'occorrenza fittizia per ogni voce. Per questo una parola mai vista come «gatto» riceve una probabilità piccolissima ma non nulla.
- **Contesti mai visti.** Se la coppia di parole precedenti (o la singola parola precedente) non compare mai come contesto, la relativa stima manca e i pesi delle stime rimanenti vengono riscalati in modo da sommare a 1: le probabilità di tutte le voci sommano così sempre a 1.
- **Temperatura.** Nel modello a triple si applica elevando i conteggi alla potenza 1/τ.
- **Token.** Libreria mistral-common 1.12.0: `tekken_240911.json` (131.072 token) e `tokenizer.model.v1` (32.000 token). Il confronto italiano–inglese usa le nove sedute presenti in entrambe le lingue.
- **word2vec.** gensim 4.4.0, skip-gram, vettori di 100 numeri, finestra 5, almeno 5 occorrenze, 15 passate, seme 42, un solo processo.

I testi generati dipendono dal seme casuale e dalla versione di Python: con le versioni indicate
si ottengono gli stessi risultati del libro. Le perplessità sulla prefazione si riferiscono al testo
in `prefazione.txt`.
