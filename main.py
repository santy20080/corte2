from fastapi import FastAPI, Body
import csv

app = FastAPI()

archivo = "productos.csv"

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

# crear producto
@app.post("/productos")
def crear(
    cod: int = Body(),
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    datos = leer()

    nuevo = {
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi
    }

    datos.append(nuevo)
    guardar(datos)
    return nuevo

# actualizar
@app.put("/productos/{cod}")
def actualizar(
    cod: int,
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    datos = leer()

    for p in datos:
        if p["codigo"] == cod:
            p["nombre"] = nom
            p["valor"] = val
            p["existencias"] = exi
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