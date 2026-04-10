from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI()

archivo = "productos.csv"

# modelo json
class Producto(BaseModel):
    codigo: int
    nombre: str
    valor: float
    existencias: int

# leer productos
def leer():
    datos = []
    try:
        with open(archivo, "r") as f:
            lector = csv.DictReader(f)
            for x in lector:
                datos.append({
                    "codigo": int(x["codigo"]),
                    "nombre": x["nombre"],
                    "valor": float(x["valor"]),
                    "existencias": int(x["existencias"])
                })
    except:
        pass
    return datos

# guardar productos
def guardar(datos):
    with open(archivo, "w", newline="") as f:
        campos = ["codigo", "nombre", "valor", "existencias"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

# ver todos
@app.get("/productos")
def todos():
    return leer()

# buscar por codigo
@app.get("/producto/{cod}")
def uno(cod: int):
    datos = leer()
    for p in datos:
        if p["codigo"] == cod:
            return p
    return {"mensaje": "no existe"}

# crear producto (json + validaciones)
@app.post("/productos")
def crear(producto: Producto):
    datos = leer()

    if producto.codigo <= 0:
        return {"mensaje": "codigo invalido"}

    if producto.valor <= 0:
        return {"mensaje": "valor invalido"}

    if producto.existencias < 0:
        return {"mensaje": "existencias invalidas"}

    if producto.nombre.strip() == "":
        return {"mensaje": "nombre vacio"}

    for p in datos:
        if p["codigo"] == producto.codigo:
            return {"mensaje": "codigo repetido"}

    nuevo = {
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "valor": producto.valor,
        "existencias": producto.existencias
    }

    datos.append(nuevo)
    guardar(datos)
    return nuevo

# actualizar (con validaciones basicas)
@app.put("/productos/{cod}")
def actualizar(cod: int, producto: Producto):
    datos = leer()

    if producto.valor <= 0:
        return {"mensaje": "valor invalido"}

    if producto.existencias < 0:
        return {"mensaje": "existencias invalidas"}

    if producto.nombre.strip() == "":
        return {"mensaje": "nombre vacio"}

    for p in datos:
        if p["codigo"] == cod:
            p["nombre"] = producto.nombre
            p["valor"] = producto.valor
            p["existencias"] = producto.existencias
            guardar(datos)
            return p

    return {"mensaje": "no encontrado"}

# eliminar
@app.delete("/productos/{cod}")
def eliminar(cod: int):
    datos = leer()

    for p in datos:
        if p["codigo"] == cod:
            datos.remove(p)
            guardar(datos)
            return {"eliminado": p}

    return {"mensaje": "no encontrado"}