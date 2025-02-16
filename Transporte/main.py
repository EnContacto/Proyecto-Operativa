from lector import LectorTransporte
from solver import SolverTransporte

def guardar_resultados(resultados, datos, nombre_archivo="resultados_transporte.txt"):
    """Guarda los resultados en un archivo de texto."""
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DEL PROBLEMA DE TRANSPORTE\n")
        f.write("=" * 50 + "\n\n")
        
        # Estado de la solución
        f.write(f"Estado de la solución: {resultados['estado']}\n\n")
        
        # Costo total
        f.write(f"Costo total de transporte: {resultados['valor_objetivo']:.2f}\n\n")
        
        # Flujos óptimos
        f.write("FLUJOS ÓPTIMOS DE TRANSPORTE:\n")
        f.write("-" * 30 + "\n")
        for ruta, cantidad in resultados['flujos'].items():
            origen, destino = ruta.split('-')
            f.write(f"De {origen} a {destino}: {cantidad:.2f} unidades\n")
        f.write("\n")
        
        # Análisis de sensibilidad
        f.write("ANÁLISIS DE SENSIBILIDAD:\n")
        f.write("-" * 30 + "\n")
        
        f.write("\nPara orígenes (ofertas):\n")
        for origen in datos['origenes']:
            dual = resultados['analisis_sensibilidad']['origenes'][origen]['dual']
            f.write(f"{origen}:\n")
            f.write(f"  Precio sombra: {dual if dual is not None else 0:.2f}\n")
        
        f.write("\nPara destinos (demandas):\n")
        for destino in datos['destinos']:
            dual = resultados['analisis_sensibilidad']['destinos'][destino]['dual']
            f.write(f"{destino}:\n")
            f.write(f"  Precio sombra: {dual if dual is not None else 0:.2f}\n")

def main():
    # Crear instancia del lector
    lector = LectorTransporte("entrada_transporte.txt")
    
    # Leer datos
    if not lector.leer_archivo():
        print("Error al leer el archivo de entrada")
        return
    
    # Obtener datos del problema
    datos = lector.obtener_datos()
    
    # Crear y resolver el modelo
    solver = SolverTransporte(datos)
    solver.crear_modelo()
    resultados = solver.resolver()
    
    # Guardar resultados
    guardar_resultados(resultados, datos)
    
    print("El problema ha sido resuelto y los resultados han sido guardados en 'resultados_transporte.txt'")

if __name__ == "__main__":
    main()