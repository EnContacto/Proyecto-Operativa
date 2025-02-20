# lector_ple.py
class LectorPLE:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.tipo_problema = None
        self.coeficientes_objetivo = []
        self.restricciones = []
        self.num_variables = 0
        
    def leer_archivo(self):
        """Lee el archivo de texto y extrae la información del problema."""
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                lineas = archivo.readlines()
                
                # Primera línea: tipo de problema (max/min)
                self.tipo_problema = lineas[0].strip().lower()
                
                # Segunda línea: número de variables
                self.num_variables = int(lineas[1].strip())
                
                # Tercera línea: coeficientes de la función objetivo
                self.coeficientes_objetivo = [float(x) for x in lineas[2].strip().split()]
                
                # Cuarta línea: número de restricciones
                num_restricciones = int(lineas[3].strip())
                
                # Resto de líneas: restricciones
                for i in range(num_restricciones):
                    linea = lineas[i + 4].strip().split()
                    coefs = [float(x) for x in linea[:-2]]
                    signo = linea[-2]
                    valor = float(linea[-1])
                    self.restricciones.append({
                        'coeficientes': coefs,
                        'signo': signo,
                        'valor': valor
                    })
                    
            return True
            
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            return False
            
    def obtener_datos(self):
        """Retorna todos los datos del problema."""
        return {
            'tipo': self.tipo_problema,
            'num_variables': self.num_variables,
            'coef_objetivo': self.coeficientes_objetivo,
            'restricciones': self.restricciones
        }