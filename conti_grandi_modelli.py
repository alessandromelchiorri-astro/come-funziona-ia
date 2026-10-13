"""Capitolo 13: i conti di un grande modello (Llama 2 da 70 miliardi) e dei modelli a esperti."""
N = 70e9          # parametri
D = 2000e9        # token di addestramento
print("memoria dei pesi: 16 bit %.0f GB, 8 bit %.0f GB, 4 bit %.0f GB" % (2 * N / 1e9, N / 1e9, N / 2 / 1e9))
C = 6 * N * D     # regola pratica: 6 operazioni per parametro e per token
print("calcolo di addestramento: %.2e operazioni" % C)
picco, efficienza = 312e12, 0.40   # GPU A100 (16 bit), frazione sfruttata
ore = C / (picco * efficienza) / 3600
print("ore-GPU: %.2f milioni; con 2.000 GPU: %.0f giorni (Meta dichiara 1,7 milioni)" % (ore / 1e6, ore / 2000 / 24))
per_token = 2 * N                  # circa 2 operazioni per parametro per ogni token generato
risposta = 500 * per_token
print("una risposta di 500 token: %.1e operazioni; risposte per eguagliare l'addestramento: %.1e" % (risposta, C / risposta))
# LoRA di rango 8 su due matrici 4.096 x 4.096 in ciascuno dei 32 blocchi di un modello da 7 miliardi
lora = 32 * 2 * 8 * (4096 + 4096)
print("LoRA: %.1f milioni di parametri, %.2f%% di 7 miliardi" % (lora / 1e6, 100 * lora / 7e9))
# Modello a esperti: DeepSeek-V3, 671 miliardi totali, 37 miliardi attivi per token
print("esperti: %.0f miliardi di operazioni per token; rapporto con un modello denso da 671 miliardi: %.1f" % (2 * 37, 671 / 37))
