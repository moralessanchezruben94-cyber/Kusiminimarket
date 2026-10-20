
import json
import csv
import os

INVENTARIO = "inventario.json"
VENTAS = "ventas.csv"
IGV = 0.18


def cargar_productos():
    # Carga el inventario guardado o crea productos de prueba.
    if os.path.exists(INVENTARIO):
        with open(INVENTARIO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return [
        {"nombre": "Arroz Costeño", "precio": 5.50, "stock": 50},
        {"nombre": "Azucar", "precio": 4.20, "stock": 40},
        {"nombre": "Aceite", "precio": 8.50, "stock": 30}
    ]


def guardar_productos(productos):
    # Guarda el stock actualizado para conservar los cambios.
    with open(INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)


def registrar_venta(productos):
    # Muestra los productos disponibles y sus existencias.
    for i, p in enumerate(productos, 1):
        print(f"{i}. {p['nombre']} - S/ {p['precio']:.2f}"
              f" - Stock: {p['stock']}")

    try:
        opcion = int(input("Seleccione el producto: "))
        cantidad = int(input("Cantidad a comprar: "))

        if not 1 <= opcion <= len(productos) or cantidad <= 0:
            print("Datos incorrectos.")
            return

        producto = productos[opcion - 1]

        if cantidad > producto["stock"]:
            print("Stock insuficiente.")
            return

        # Calcula subtotal, descuento, IGV y total.
        subtotal = producto["precio"] * cantidad
        descuento = subtotal * 0.10 if subtotal >= 100 else 0
        igv = (subtotal - descuento) * IGV
        total = subtotal - descuento + igv

        print(f"Subtotal: S/ {subtotal:.2f}")
        print(f"Descuento: S/ {descuento:.2f}")
        print(f"IGV: S/ {igv:.2f}")
        print(f"Total a pagar: S/ {total:.2f}")

        pago = float(input("Monto recibido: S/ "))
        if pago < total:
            print("Pago insuficiente. Venta no registrada.")
            return

        vuelto = pago - total
        producto["stock"] -= cantidad
        guardar_productos(productos)

        # Registra la operación en el archivo de ventas.
        nuevo = not os.path.exists(VENTAS)
        with open(VENTAS, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            if nuevo:
                escritor.writerow(["Producto", "Cantidad", "Total"])
            escritor.writerow([producto["nombre"], cantidad, f"{total:.2f}"])

        print(f"Vuelto: S/ {vuelto:.2f}")
        print(f"Stock restante: {producto['stock']}")
        print("Venta registrada correctamente.")

    except ValueError:
        print("Error: ingrese datos numericos validos.")
    except OSError as error:
        print(f"Error al guardar los archivos: {error}")


def main():
    # Controla el menú principal del sistema.
    productos = cargar_productos()

    while True:
        print("\n=== KUSI MINIMARKET ===")
        print("1. Mostrar inventario")
        print("2. Registrar venta")
        print("3. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            for p in productos:
                print(f"{p['nombre']} | S/ {p['precio']:.2f}"
                      f" | Stock: {p['stock']}")
        elif opcion == "2":
            registrar_venta(productos)
        elif opcion == "3":
            guardar_productos(productos)
            print("Sistema finalizado.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()

