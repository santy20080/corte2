from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

productos = [
    {
        "codigo": 1,
        "nombre": "esfero",
        "valor": 3500,
        "existencias": 10
    },
    {
        "codigo": 2,
        "nombre": "cuaderno",
        "valor": 5000,
        "existencias": 15
    },
    {
        "codigo": 3,
        "nombre": "lapiz",
        "valor": 200,
        "existencias": 12
    }
]

@app.get("/productoall/")
def listProductos():
    return productos

@app.get("/producto/{cod}")
def findProducto(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            return prod
    return {"mensaje": "Producto no encontrado"}

@app.get("/producto/")
def findProductos2(nom: str):
    for prod in productos:
        if prod["nombre"].lower() == nom.lower():
            return prod
    return {"mensaje": "Producto no encontrado"}

@app.post("/productos")
def createProducto(cod: int, nom: str, val: float, exi: int):
    if val <= 0 or exi <= 0:
        return {"mensaje": "El valor y las existencias deben ser mayores a cero"}
    
    # Verifica que el código sea el siguiente consecutivo
    if cod != max([prod["codigo"] for prod in productos]) + 1:
        return {"mensaje": "El código debe ser el siguiente consecutivo"}

    productos.append({
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos2")
def createProducto2(
    cod: int = Body(),
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    if val <= 0 or exi <= 0:
        return {"mensaje": "El valor y las existencias deben ser mayores a cero"}

    # Verifica que el código sea el siguiente consecutivo
    if cod != max([prod["codigo"] for prod in productos]) + 1:
        return {"mensaje": "El código debe ser el siguiente consecutivo"}

    productos.append({
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.put("/productos/{cod}")
def updateProducto(
    cod: int,
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    producto = None
    for prod in productos:
        if prod["codigo"] == cod:
            producto = prod
            break

    if not producto:
        return {"mensaje": "Producto no encontrado"}

    if val <= 0 or exi <= 0:
        return {"mensaje": "El valor y las existencias deben ser mayores a cero"}

    # Mostrar producto original y actualizado
    producto_original = producto.copy()
    producto["nombre"] = nom
    producto["valor"] = val
    producto["existencias"] = exi
    return {"producto_original": producto_original, "producto_actualizado": producto}

@app.delete("/productos")
def deleteProducto(cod: int):
    producto = None
    for prod in productos:
        if prod["codigo"] == cod:
            producto = prod
            break

    if not producto:
        return {"mensaje": "Producto no encontrado"}

    productos.remove(producto)
    return {"producto_eliminado": producto}