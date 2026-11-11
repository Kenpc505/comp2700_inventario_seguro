# Base educativa — COMP 2700

Kenneth Pérez Camacho       Y00616770

Esta versión contiene debilidades intencionales. Utilice únicamente los datos
ficticios incluidos, en su computadora. No es una aplicación de producción.

Requiere Python 3.10 o posterior. Desde esta carpeta:

    python -m venv .venv

Windows CMD:

    .venv\Scripts\activate.bat

macOS/Linux:

    source .venv/bin/activate

Luego:

    python -m pip install -r requirements.txt
    python app.py

En algunos sistemas debe utilizar python3 en lugar de python.

Cuentas públicas y exclusivamente ficticias:
- admin / AdminDemo2700!
- user / UserDemo2700!

Comience probando consulta y cambio de cantidad con admin. La base no aplica
todos los controles: user también puede modificar, las claves están legibles,
las entradas inválidas pueden causar errores y no se guarda auditoría.
Los TODO de app.py guían las correcciones; seguridad.py contiene funciones listas.

Para migrar las contraseñas, cree un pequeño script que llame crear_hash para
cada cuenta y guarde el resultado en un campo hash. Elimine el campo clave del
archivo final. Adapte autenticar para llamar verificar_clave. No compare dos
hashes recién generados: sus salts serán diferentes.

Los archivos se resuelven respecto a app.py. Guarde una copia del inventario
antes de las pruebas de errores. Use P001 con cantidad 10 al comenzar.

Puede hacer pruebas directas desde un script que importe app:

    import app
    sesion = app.autenticar("user", "UserDemo2700!")
    app.modificar_cantidad(sesion, "P001", "99")

Después de corregir los permisos, esa llamada debe rechazarse sin cambiar P001.
Repita con None como sesión. No fabrique un diccionario con rol admin para
simular una sesión válida: esta aplicación confía en su propio proceso.

JSON almacena un documento completo (lista de productos o usuarios).
Solamente auditoria.jsonl utiliza un objeto por línea.

Complete este README con su nombre, ejecución, pruebas, fuentes y uso de IA.
No suba .venv, __pycache__, credenciales reales ni datos personales de terceros.

## Pruebas

| Área | Prueba | Resultado |
|---|---|---|
| Autenticación | Login correcto, contraseña incorrecta, usuario inexistente | Acceso solo con credenciales correctas; mismo mensaje de rechazo |
| Autorización | `python prueba_autorizacion.py` (sesión user y None) | Rechazado; P001 sin cambio |
| Validación | -1, 1001, abc, 2.5, vacío / 0 y 1000 | Inválidos rechazados / límites aceptados |
| Modificación | P001 de 10 a 20; P999 | Cambio aplicado; P999 informado sin crear productos |
| Persistencia | Cerrar y volver a abrir | P001 conserva 20 |
| Errores | Archivo ausente; `ESTO NO ES JSON` | Mensaje controlado; archivo no recreado ni sobrescrito |

## Fuentes

- argon2-cffi: https://argon2-cffi.readthedocs.io/en/stable/api.html
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Python json: https://docs.python.org/3/library/json.html

## Uso de IA

- Herramienta: Claude (Anthropic).
- Uso: comprender los requisitos, organizar los pasos y las correcciones de app.py.
- Verificación: ejecuté el programa y prueba_autorizacion.py con los casos de la tabla y revisé usuarios.json y auditoria.jsonl.
- Sugerencia corregida: la validación se cambió de isdigit() a isdecimal(), porque isdigit() acepta caracteres como "²" que hacen fallar int().