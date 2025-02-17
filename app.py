from flask import Flask, render_template, request, jsonify, session
from src.transporte.lector import LectorTransporte
from src.transporte.solver import SolverTransporte
from src.transporte.interpretador import InterpretadorTransporte
from src.lineal.lector import LectorPL
from src.lineal.solver import SolverPL
from src.lineal.interpretador import InterpretadorPL
from src.redes.solver import SolverRedes
from src.redes.lector import LectorRedes
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Obtener la API Key de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar sesiones

# Instancias de los interpretadores
interpretador_transporte = InterpretadorTransporte()
interpretador_lineal = InterpretadorPL()

# Variable global para almacenar el estado de LectorRedes
lector_redes = LectorRedes()

# Ruta principal (página de inicio)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el problema de transporte
@app.route('/transporte', methods=['GET', 'POST'])
def transporte():
    if request.method == 'POST':
        # Procesar el archivo subido
        archivo = request.files['archivo']
        archivo.save('entrada_transporte.txt')

        # Leer y resolver el problema
        lector = LectorTransporte("entrada_transporte.txt")
        if not lector.leer_archivo():
            return "Error al leer el archivo de entrada"

        datos = lector.obtener_datos()
        solver = SolverTransporte(datos)
        solver.crear_modelo()
        resultados = solver.resolver()

        # Interpretar los resultados
        interpretacion = interpretador_transporte.interpretar(resultados)

        return render_template('resultados_transporte.html', resultados=resultados, interpretacion=interpretacion, datos=datos)

    return render_template('transporte.html')

# Ruta para el problema de programación lineal
@app.route('/lineal', methods=['GET', 'POST'])
def lineal():
    if request.method == 'POST':
        archivo = request.files['archivo']
        archivo.save('entrada_lineal.txt')

        lector = LectorPL("entrada_lineal.txt")
        if not lector.leer_archivo():
            return "Error al leer el archivo de entrada"

        datos = lector.obtener_datos()
        solver = SolverPL(datos)
        solver.crear_modelo()
        resultados = solver.resolver()

        interpretacion = interpretador_lineal.interpretar(resultados)

        return render_template('resultados_lineal.html', resultados=resultados, interpretacion=interpretacion)

    return render_template('lineal.html')

# Rutas para análisis de resultados
@app.route('/analizar_transporte', methods=['POST'])
def analizar_transporte():
    resultados = request.json['resultados']
    interpretacion = interpretador_transporte.interpretar(resultados)
    return jsonify({'interpretacion': interpretacion})

@app.route('/analizar_lineal', methods=['POST'])
def analizar_lineal():
    resultados = request.json['resultados']
    interpretacion = interpretador_lineal.interpretar(resultados)
    return jsonify({'interpretacion': interpretacion})

# Ruta para el problema de redes
@app.route('/redes', methods=['GET', 'POST'])
def redes():
    global lector_redes  # Usar la variable global

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'agregar_nodo':
            nodo = request.form.get('nodo')
            if nodo:
                lector_redes.agregar_nodo(nodo)

        elif accion == 'agregar_conexion':
            nodo1 = request.form.get('nodo1')
            nodo2 = request.form.get('nodo2')
            distancia = request.form.get('distancia')
            if nodo1 and nodo2 and distancia:
                lector_redes.agregar_conexion(nodo1, nodo2, distancia)

        elif accion == 'eliminar_conexion':
            indice = int(request.form.get('indice'))
            lector_redes.eliminar_conexion(indice)

        elif accion == 'calcular_ruta':
            inicio = request.form.get('inicio')
            fin = request.form.get('fin')
            if inicio and fin:
                datos = lector_redes.obtener_datos()
                print("Datos del grafo:", datos)  # Depuración
                solver = SolverRedes(datos)
                resultados = solver.calcular_ruta_mas_corta(inicio, fin)
                if resultados:
                    return render_template('resultados_redes.html', resultados=resultados)
                else:
                    return "No hay ruta entre los nodos especificados."

    # Obtener las conexiones para mostrarlas en la plantilla
    conexiones = lector_redes.obtener_datos()['conexiones']
    return render_template('redes.html', conexiones=conexiones)

if __name__ == '__main__':
    app.run(debug=True)