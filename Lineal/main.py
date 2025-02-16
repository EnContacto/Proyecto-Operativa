from lector import LectorPL
from solver import SolverPL

def guardar_resultados(resultados, nombre_archivo="resultadoslineal.txt"):
    """Guarda los resultados en un archivo de texto."""
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DEL PROBLEMA DE PROGRAMACIÓN LINEAL\n")
        f.write("=" * 50 + "\n\n")
        
        # Estado de la solución
        f.write(f"Estado de la solución: {resultados['estado']}\n\n")
        
        # Valor de la función objetivo
        f.write(f"Valor óptimo de la función objetivo: {resultados['valor_objetivo']:.4f}\n\n")
        
        # Valores de las variables
        f.write("VALORES DE LAS VARIABLES:\n")
        for var, valor in resultados['variables'].items():
            f.write(f"{var} = {valor:.4f}\n")
        f.write("\n")
        
        # Precios sombra (variables duales)
        f.write("PRECIOS SOMBRA:\n")
        for i, dual in enumerate(resultados['dual_restricciones']):
            f.write(f"Restricción {i+1}: {dual:.4f}\n")
        f.write("\n")
        
        # Costos reducidos
        f.write("COSTOS REDUCIDOS:\n")
        for var, reducido in resultados['reducidos'].items():
            f.write(f"{var}: {reducido:.4f}\n")
        f.write("\n")
        
        # Análisis de sensibilidad
        f.write("ANÁLISIS DE SENSIBILIDAD:\n")
        f.write("\nPara las variables:\n")
        for var, rangos in resultados['sensibilidad']['variables'].items():
            f.write(f"{var}:\n")
            f.write(f"  Rango inferior: {rangos['rango_inferior']}\n")
            f.write(f"  Rango superior: {rangos['rango_superior']}\n")
            
        f.write("\nPara las restricciones:\n")
        for rest, datos in resultados['sensibilidad']['restricciones'].items():
            f.write(f"{rest}:\n")
            f.write(f"  Precio sombra: {datos['dual']}\n")
            f.write(f"  Valor actual RHS: {datos['rhs']}\n")
def main():
    # Crear instancia del lector
    lector = LectorPL("entrada.txt")
    
    # Leer datos
    if not lector.leer_archivo():
        print("Error al leer el archivo de entrada")
        return
        
    # Obtener datos del problema
    datos = lector.obtener_datos()
    
    # Crear y resolver el modelo
    solver = SolverPL(datos)
    solver.crear_modelo()
    resultados = solver.resolver()
    
    # Guardar resultados
    guardar_resultados(resultados)
    
    print("El problema ha sido resuelto y los resultados han sido guardados en 'resultadoslineal.txt'")

if __name__ == "__main__":
    main()