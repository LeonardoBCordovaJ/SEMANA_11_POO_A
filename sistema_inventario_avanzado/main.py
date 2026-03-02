from modelos.producto import Producto
from servicios.inventario_service import Inventario


def leer_entero(mensaje: str) -> int:
    """Solicita un numero entero con validacion."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada invalida. Ingresa un numero entero.")


def leer_flotante(mensaje: str) -> float:
    """Solicita un numero decimal con validacion."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada invalida. Ingresa un numero decimal.")


def mostrar_menu():
    print("\n======= SISTEMA AVANZADO DE INVENTARIO =======")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Listar todos los productos")
    print("6. Ver resumen del inventario")
    print("0. Salir")
    print("===============================================")


def opcion_agregar(inventario: Inventario):
    print("\n--- Agregar Producto ---")
    id_p = input("ID unico: ").strip()
    nombre = input("Nombre: ").strip()
    cantidad = leer_entero("Cantidad: ")
    precio = leer_flotante("Precio: ")

    producto = Producto(id_p, nombre, cantidad, precio)
    if inventario.agregar_producto(producto):
        print(f"Producto '{nombre}' agregado y guardado correctamente.")
    else:
        print(f"Error: Ya existe un producto con el ID '{id_p}'.")


def opcion_eliminar(inventario: Inventario):
    print("\n--- Eliminar Producto ---")
    id_p = input("ID del producto a eliminar: ").strip()
    if inventario.eliminar_producto(id_p):
        print(f"Producto con ID '{id_p}' eliminado y archivo actualizado.")
    else:
        print(f"Error: No se encontro un producto con el ID '{id_p}'.")


def opcion_actualizar(inventario: Inventario):
    print("\n--- Actualizar Producto ---")
    id_p = input("ID del producto a actualizar: ").strip()
    print("Deja vacio si no deseas cambiar ese valor.")

    texto_cant = input("Nueva cantidad: ").strip()
    texto_precio = input("Nuevo precio: ").strip()

    nueva_cantidad = int(texto_cant) if texto_cant else None
    nuevo_precio = float(texto_precio) if texto_precio else None

    if nueva_cantidad is None and nuevo_precio is None:
        print("No se ingreso ningun cambio.")
        return

    try:
        if inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio):
            print(f"Producto '{id_p}' actualizado y archivo guardado.")
        else:
            print(f"Error: No se encontro el producto con ID '{id_p}'.")
    except ValueError as e:
        print(f"Error de validacion: {e}")


def opcion_buscar(inventario: Inventario):
    print("\n--- Buscar Producto por Nombre ---")
    texto = input("Texto a buscar: ").strip()
    resultados = inventario.buscar_por_nombre(texto)

    if not resultados:
        print("No se encontraron productos que coincidan.")
    else:
        print(f"\n{len(resultados)} resultado(s) encontrado(s):")
        for p in resultados:
            print(" -", p)


def opcion_listar(inventario: Inventario):
    print("\n--- Inventario Completo ---")
    productos = inventario.listar_productos()
    if not productos:
        print("El inventario esta vacio.")
    else:
        print(f"{len(productos)} producto(s) registrado(s):")
        for p in productos:
            print(" -", p)


def opcion_resumen(inventario: Inventario):
    print("\n--- Resumen del Inventario ---")
    total, nombres_unicos, ids = inventario.resumen()
    print(f"Total de productos registrados : {total}")
    print(f"Total de nombres unicos        : {nombres_unicos}")
    print(f"IDs registrados                : {ids}")


def main():
    print("Iniciando Sistema Avanzado de Gestion de Inventarios...")
    inventario = Inventario()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            opcion_agregar(inventario)
        elif opcion == "2":
            opcion_eliminar(inventario)
        elif opcion == "3":
            opcion_actualizar(inventario)
        elif opcion == "4":
            opcion_buscar(inventario)
        elif opcion == "5":
            opcion_listar(inventario)
        elif opcion == "6":
            opcion_resumen(inventario)
        elif opcion == "0":
            print("Saliendo del sistema. Hasta luego.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    main()