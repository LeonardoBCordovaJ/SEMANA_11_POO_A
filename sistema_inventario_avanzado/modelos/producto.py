class Producto:
    """
    Clase que representa un producto del inventario.
    Utiliza encapsulamiento con atributos privados,
    getters y setters para acceder a ellos de forma segura.
    """

    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        # Atributos privados del producto
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # ---- Getters ----
    def get_id(self) -> str:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_cantidad(self) -> int:
        return self._cantidad

    def get_precio(self) -> float:
        return self._precio

    # ---- Setters con validacion ----
    def set_cantidad(self, cantidad: int) -> None:
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = cantidad

    def set_precio(self, precio: float) -> None:
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio

    def to_csv(self) -> str:
        """
        Convierte el producto a una linea de texto CSV
        para guardarlo en el archivo de inventario.
        Formato: id,nombre,cantidad,precio
        """
        return f"{self._id},{self._nombre},{self._cantidad},{self._precio}"

    @staticmethod
    def from_csv(linea: str):
        """
        Crea un objeto Producto desde una linea de texto CSV.
        Retorna None si la linea esta corrupta o mal formateada.
        """
        try:
            partes = linea.strip().split(",")
            if len(partes) != 4:
                return None
            return Producto(partes[0], partes[1], int(partes[2]), float(partes[3]))
        except (ValueError, IndexError):
            return None

    def __str__(self) -> str:
        return (f"ID: {self._id} | "
                f"Nombre: {self._nombre} | "
                f"Cantidad: {self._cantidad} | "
                f"Precio: ${self._precio:.2f}")