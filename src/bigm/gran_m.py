class GranM:
    def __init__(self, funcion_objetivo, restricciones, tipo_problema):
        """
        Inicializa el problema de programación lineal.
        :param funcion_objetivo: Lista de coeficientes de la función objetivo.
        :param restricciones: Lista de restricciones, donde cada restricción es una tupla (coeficientes, desigualdad, valor).
        :param tipo_problema: 'maximizar' o 'minimizar'.
        """
        self.funcion_objetivo = funcion_objetivo
        self.restricciones = restricciones
        self.tipo_problema = tipo_problema
        self.iteraciones = []  # Almacena las matrices de cada iteración

    def construir_tabla(self):
        """
        Construye la tabla inicial para el Método de la Gran M.
        """
        # Paso 1: Convertir restricciones a ecuaciones
        # Paso 2: Agregar variables de holgura, exceso y artificiales
        # Paso 3: Construir la matriz inicial
        # (Este es un ejemplo simplificado)
        tabla_inicial = [
            [1, 2, 1, 0, 0, 10],
            [2, 1, 0, 1, 0, 15],
            [1, 1, 0, 0, 1, 8]
        ]
        self.iteraciones.append(tabla_inicial)

    def resolver(self):
        """
        Resuelve el problema utilizando el Método de la Gran M.
        """
        self.construir_tabla()

        # Iterar hasta encontrar la solución óptima
        while not self.es_optima():
            self.iterar()

    def es_optima(self):
        """
        Verifica si la solución actual es óptima.
        """
        # Lógica para verificar optimalidad
        return True  # Cambiar según la lógica

    def iterar(self):
        """
        Realiza una iteración del Método de la Gran M.
        """
        # Lógica para pivotear y actualizar la tabla
        nueva_tabla = [
            [1, 2, 1, 0, 0, 10],
            [2, 1, 0, 1, 0, 15],
            [1, 1, 0, 0, 1, 8]
        ]
        self.iteraciones.append(nueva_tabla)

    def obtener_resultados(self):
        """
        Devuelve las iteraciones y la solución óptima.
        """
        return {
            'iteraciones': self.iteraciones,
            'solucion_optima': [10, 15]  # Ejemplo de solución
        }