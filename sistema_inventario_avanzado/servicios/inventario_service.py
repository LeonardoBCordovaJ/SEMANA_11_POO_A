import os
from modelos.producto import Producto

# Nombre del archivo donde se guarda el inventario
ARCHIVO = "inventario.txt"


class Inventario:
    """
    Clase que gestiona el inventario de productos.

    Colecciones utilizadas:
    - Diccionario (_productos): permite busqueda rapida por ID en O(1).
    - Conjunto (_nombres_registrados): evita duplicados de nombres rapidamente.
    - Tupla: usada al mostrar resumen de estadisticas del inventario.
    - Lista: usada al retornar resultados de busqueda.
    """

    def __init__(self):
        # Diccionario principal: clave = ID, valor = objeto Producto
        self._productos: dict[str, Producto] = {}

        # Conjunto para controlar nombres ya registrados (sin duplicados)
        self._nombres_registrados: set[str] = set()

        # Carga automatica al iniciar el programa
        self._cargar_desde_archivo()

    # -------------------------------------------------------
    # METODOS PUBLICOS
    # -------------------------------------------------------

    def agregar_producto(self, producto: Producto) -> bool:
        """
        Agrega un producto al diccionario si el ID no existe.
        Retorna True si se agrego, False si el ID ya existia.
        """
        if producto.get_id() in self._productos:
            return False

        self._productos[producto.get_id()] = producto
        self._nombres_registrados.add(producto.get_nombre().lower())
        self._guardar_en_archivo()
        return True

    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto del diccionario por su ID.
        Retorna True si se elimino, False si no se encontro.
        """
        if id_producto not in self._productos:
            return False

        nombre = self._productos[id_producto].get_nombre().lower()
        del self._productos[id_producto]
        self._nombres_registrados.discard(nombre)
        self._guardar_en_archivo()
        return True

    def actualizar_producto(self, id_producto: str,
                            nueva_cantidad: int = None,
                            nuevo_precio: float = None) -> bool:
        """
        Actualiza cantidad y/o precio de un producto por ID.
        Retorna True si se actualizo, False si no se encontro.
        """
        if id_producto not in self._productos:
            return False

        producto = self._productos[id_producto]

        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)

        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        self._guardar_en_archivo()
        return True

    def buscar_por_nombre(self, texto: str) -> list[Producto]:
        """
        Busca productos por coincidencia parcial en el nombre.
        Retorna una lista con los resultados encontrados.
        """
        texto = texto.lower()
        return [p for p in self._productos.values()
                if texto in p.get_nombre().lower()]

    def listar_productos(self) -> list[Producto]:
        """
        Retorna todos los productos como una lista.
        """
        return list(self._productos.values())

    def resumen(self) -> tuple:
        """
        Retorna una tupla con estadisticas del inventario:
        (total_productos, total_nombres_unicos, id_productos)
        """
        return (
            len(self._productos),
            len(self._nombres_registrados),
            list(self._productos.keys())
        )

    # -------------------------------------------------------
    # METODOS PRIVADOS: Manejo de archivos
    # -------------------------------------------------------

    def _guardar_en_archivo(self) -> None:
        """
        Guarda todos los productos en el archivo inventario.txt.
        Maneja PermissionError si no hay permisos de escritura.
        """
        try:
            with open(ARCHIVO, 'w', encoding='utf-8') as archivo:
                for producto in self._productos.values():
                    archivo.write(producto.to_csv() + "\n")
            print(f"Archivo '{ARCHIVO}' actualizado correctamente.")
        except PermissionError:
            print(f"Error: No tienes permisos para escribir en '{ARCHIVO}'.")
        except OSError as e:
            print(f"Error inesperado al guardar: {e}")

    def _cargar_desde_archivo(self) -> None:
        """
        Carga los productos desde inventario.txt al iniciar.
        Si el archivo no existe, lo crea vacio.
        Omite lineas corruptas y avisa al usuario.
        """
        try:
            if not os.path.exists(ARCHIVO):
                open(ARCHIVO, 'w', encoding='utf-8').close()
                print(f"Archivo '{ARCHIVO}' creado nuevo.")
                return

            with open(ARCHIVO, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            corruptas = 0
            for linea in lineas:
                if linea.strip() == "":
                    continue
                producto = Producto.from_csv(linea)
                if producto:
                    self._productos[producto.get_id()] = producto
                    self._nombres_registrados.add(producto.get_nombre().lower())
                else:
                    corruptas += 1

            print(f"Inventario cargado: {len(self._productos)} producto(s).")
            if corruptas > 0:
                print(f"Advertencia: {corruptas} linea(s) corrupta(s) omitidas.")

        except PermissionError:
            print(f"Error: Sin permisos para leer '{ARCHIVO}'.")
        except OSError as e:
            print(f"Error inesperado al cargar: {e}")