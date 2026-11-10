"""BASE EDUCATIVA INSEGURA. Corregir los TODO antes de la entrega."""
import json
from datetime import datetime
from pathlib import Path
from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
# TODO: controlar archivo ausente y JSON inválido. No sobrescribirlos.
    try:
        return json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Error: no se encontró el archivo de inventario.")
    except json.JSONDecodeError:
        print("Error: el archivo de inventario no tiene un formato JSON válido.")
    return None
    

def guardar_inventario(productos):
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")


def registrar_evento(usuario, accion, resultado, **detalles):
# TODO: guardar un objeto JSON por línea; fecha/hora, usuario, acción,
# resultado y detalles no sensibles. Nunca guardar contraseña ni hash.
    evento = {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "usuario": usuario,
        "accion": accion,
        "resultado": resultado,
        **detalles,
    }
    with open(LOG, "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def autenticar(nombre, clave):
    usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    for usuario in usuarios:
        if usuario["usuario"] == nombre and verificar_clave(usuario["hash"], clave):
            registrar_evento(nombre, "login", "exitoso")
            return {"usuario": nombre, "rol": usuario["rol"]}
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
# TODO: rechazar si no existe sesión válida.
    if not sesion:
        print("Acceso denegado: debe iniciar sesión.")
        registrar_evento("sin_sesion", "consultar", "rechazado")
        return
    productos = cargar_inventario()
    if productos is None:
        return
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])


def modificar_cantidad(sesion, identificador, entrada):
# TODO: verificar sesión y rol AQUÍ, antes de modificar.
# TODO: validar entero entre 0 y 1000, sin interrumpir el programa.
# TODO: informar identificador inexistente, sin crear productos.
    # 1. Sesión
    if not sesion:
        print("Acceso denegado: debe iniciar sesión.")
        registrar_evento("sin_sesion", "modificar", "rechazado",
                         producto=identificador)
        return False
    # 2. Rol
    if sesion.get("rol") != "admin":
        print("Acceso denegado: solo admin puede modificar cantidades.")
        registrar_evento(sesion["usuario"], "modificar", "rechazado_permisos",
                         producto=identificador)
        return False
    # 3. Validación
    texto = str(entrada).strip()
    if not texto.isdecimal() or int(texto) > 1000:
        print("Cantidad inválida: escriba un número entero entre 0 y 1000.")
        return False
    cantidad = int(texto)
    # 4. Buscar y aplicar
    productos = cargar_inventario()
    if productos is None:
        return False
    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            guardar_inventario(productos)
            registrar_evento(
                sesion["usuario"], "modificar", "exitoso",
                producto=identificador, anterior=anterior, nueva=cantidad
            )
            print("Cantidad actualizada.")
            return True
    print("No existe un producto con el identificador", identificador)
    return False


def main():
    print("Inventario académico — BASE CON DEBILIDADES")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            sesion = autenticar(nombre, input("Contraseña de prueba: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesión | 0. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
