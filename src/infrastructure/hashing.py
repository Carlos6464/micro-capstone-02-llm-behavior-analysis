import hashlib


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Calcula hash SHA-256 do texto.
def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
