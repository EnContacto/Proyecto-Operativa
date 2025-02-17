from pulp import *

class SolverTransporte:
    def __init__(self, datos):
        self.datos = datos
        self.modelo = None
        self.variables = None
        self.resultado = None
        self.restricciones_oferta = []
        self.restricciones_demanda = []
        
    def crear_modelo(self):
        """Crea y configura el modelo de transporte."""
        # Crear el problema de minimización
        self.modelo = LpProblem("Problema_Transporte", LpMinimize)
        
        # Crear índices para orígenes y destinos
        origenes = self.datos['origenes']
        destinos = self.datos['destinos']
        
        # Crear variables de decisión
        self.variables = LpVariable.dicts("X",
                                        ((i, j) for i in origenes for j in destinos),
                                        lowBound=0)
        
        # Función objetivo
        self.modelo += lpSum(self.datos['costos'][i][j] * self.variables[origenes[i], destinos[j]]
                           for i in range(len(origenes))
                           for j in range(len(destinos)))
        
        # Restricciones de oferta
        for i in range(len(origenes)):
            restriccion = lpSum(self.variables[origenes[i], destinos[j]]
                              for j in range(len(destinos))) <= self.datos['ofertas'][i]
            self.restricciones_oferta.append(restriccion)
            self.modelo += restriccion
        
        # Restricciones de demanda
        for j in range(len(destinos)):
            restriccion = lpSum(self.variables[origenes[i], destinos[j]]
                              for i in range(len(origenes))) >= self.datos['demandas'][j]
            self.restricciones_demanda.append(restriccion)
            self.modelo += restriccion
    
    def resolver(self):
        """Resuelve el modelo y guarda los resultados."""
        self.modelo.solve()
        
        # Preparar resultados
        self.resultado = {
            'estado': LpStatus[self.modelo.status],
            'valor_objetivo': value(self.modelo.objective),
            'flujos': self._obtener_flujos(),
            'dual_origenes': self._obtener_duales_origenes(),
            'dual_destinos': self._obtener_duales_destinos(),
            'analisis_sensibilidad': self._analizar_sensibilidad()
        }
        
        return self.resultado
    
    def _obtener_flujos(self):
        """Obtiene los flujos óptimos entre orígenes y destinos."""
        flujos = {}
        for i in self.datos['origenes']:
            for j in self.datos['destinos']:
                valor = value(self.variables[i, j])
                if valor > 1e-10:  # Consideramos valores mayores a 0
                    flujos[f"{i}-{j}"] = valor
        return flujos
    
    def _obtener_duales_origenes(self):
        """Obtiene los precios sombra de las restricciones de oferta."""
        constraints = list(self.modelo.constraints.values())
        return [constraints[i].pi if i < len(self.restricciones_oferta) else 0 
                for i in range(len(self.datos['origenes']))]
    
    def _obtener_duales_destinos(self):
        """Obtiene los precios sombra de las restricciones de demanda."""
        constraints = list(self.modelo.constraints.values())
        offset = len(self.restricciones_oferta)
        return [constraints[i + offset].pi if i + offset < len(constraints) else 0 
                for i in range(len(self.datos['destinos']))]
    
    def _analizar_sensibilidad(self):
        """Realiza el análisis de sensibilidad para ofertas y demandas."""
        duales_origenes = self._obtener_duales_origenes()
        duales_destinos = self._obtener_duales_destinos()
        
        return {
            'origenes': {
                origen: {'dual': dual if dual is not None else 0}
                for origen, dual in zip(self.datos['origenes'], duales_origenes)
            },
            'destinos': {
                destino: {'dual': dual if dual is not None else 0}
                for destino, dual in zip(self.datos['destinos'], duales_destinos)
            }
        }