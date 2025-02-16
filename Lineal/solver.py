from pulp import *

class SolverPL:
    def __init__(self, datos):
        self.datos = datos
        self.modelo = None
        self.variables = None
        self.resultado = None
        
    def crear_modelo(self):
        """Crea y configura el modelo de programación lineal."""
        # Determinar si es maximización o minimización
        if self.datos['tipo'] == 'max':
            self.modelo = LpProblem("Problema_PL", LpMaximize)
        else:
            self.modelo = LpProblem("Problema_PL", LpMinimize)
            
        # Crear variables
        self.variables = [LpVariable(f'x{i+1}', lowBound=0) 
                         for i in range(self.datos['num_variables'])]
        
        # Función objetivo
        self.modelo += lpSum([self.variables[i] * self.datos['coef_objetivo'][i] 
                            for i in range(self.datos['num_variables'])])
        
        # Restricciones
        for r in self.datos['restricciones']:
            expr = lpSum([self.variables[i] * r['coeficientes'][i] 
                        for i in range(self.datos['num_variables'])])
            if r['signo'] == '<=':
                self.modelo += expr <= r['valor']
            elif r['signo'] == '>=':
                self.modelo += expr >= r['valor']
            else:
                self.modelo += expr == r['valor']
                
    def resolver(self):
        """Resuelve el modelo y guarda los resultados."""
        self.modelo.solve()
        
        self.resultado = {
            'estado': LpStatus[self.modelo.status],
            'valor_objetivo': value(self.modelo.objective),
            'variables': {v.name: v.value() for v in self.variables},
            'dual_restricciones': [c.pi for c in self.modelo.constraints.values()],
            'reducidos': {v.name: v.dj for v in self.variables},
            'sensibilidad': self._analizar_sensibilidad()
        }
        
        return self.resultado
        
    def _analizar_sensibilidad(self):
        """Realiza el análisis de sensibilidad."""
        sensibilidad = {
            'variables': {},
            'restricciones': {}
        }
        
        # Análisis de sensibilidad para variables
        for v in self.variables:
            sensibilidad['variables'][v.name] = {
                'rango_inferior': v.upBound,
                'rango_superior': v.lowBound
            }
            
        # Análisis de sensibilidad para restricciones
        for i, c in enumerate(self.modelo.constraints.values()):
            sensibilidad['restricciones'][f'restriccion_{i+1}'] = {
                'dual': c.pi,
                'rhs': c.constant
            }
            
        return sensibilidad