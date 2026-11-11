import app
print("Estudiante: Kenneth Pérez Camacho")
sesion = app.autenticar("user", "UserDemo2700!")
app.modificar_cantidad(sesion, "P001", "99")
app.modificar_cantidad(None, "P001", "99")
app.consultar_inventario(None)
admin = app.autenticar("admin", "AdminDemo2700!")
app.consultar_inventario(admin)