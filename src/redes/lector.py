class LectorRedes:
    def __init__(self):
        self.nodos = set()
        self.conexiones = []
        
    def agregar_nodo(self, nodo):
        """Agrega un nodo al grafo."""
        if nodo not in self.nodos:
            self.nodos.add(nodo)
        else:
            print(f"El nodo '{nodo}' ya existe.")
        
    def agregar_conexion(self, nodo1, nodo2, distancia):
        """Agrega una conexión entre dos nodos con una distancia."""
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            print(f"Error: Uno de los nodos no existe en el grafo.")
        else:
            self.conexiones.append((nodo1, nodo2, float(distancia)))
        
    def eliminar_conexion(self, indice):
        """Elimina una conexión por su índice."""
        if 0 <= indice < len(self.conexiones):
            self.conexiones.pop(indice)
        else:
            print(f"Índice {indice} fuera de rango.")
        
    def obtener_datos(self):
        """Retorna todos los datos del grafo."""
        return {
            'nodos': list(self.nodos),
            'conexiones': self.conexiones
        }