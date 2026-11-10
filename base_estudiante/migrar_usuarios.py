import json
from seguridad import crear_hash

usuarios = json.load(open("usuarios.json", encoding="utf-8"))
for u in usuarios:
    u["hash"] = crear_hash(u.pop("clave"))   # crea el hash y elimina "clave"
json.dump(usuarios, open("usuarios.json", "w", encoding="utf-8"), indent=2)