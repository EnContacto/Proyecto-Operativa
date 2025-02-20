from flask import Flask, render_template, request, jsonify, session
from src.transporte.lector import LectorTransporte
from src.transporte.solver import SolverTransporte
from src.transporte.interpretador import InterpretadorTransporte
from src.ple.lector import LectorPLE  
from src.ple.solver import SolverPLE  
from src.lineal.interpretador import InterpretadorPL
from src.lineal.lector import LectorPL
from src.lineal.solver  import SolverPL
from src.ple.interpretador import InterpretadorPLE  
from src.redes.solver import SolverRedes
from src.bigm.gran_m import GranM
from src.redes.lector import LectorRedes
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener la API Key de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Instancias de los interpretadores
interpretador_transporte = InterpretadorTransporte()
interpretador_ple = InterpretadorPLE()  
interpretador_lineal = InterpretadorPL()

lector_redes = LectorRedes()

@app.route('/')
def index():
    return render_template('index.html')
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

@app.route('/analizar_lineal', methods=['POST'])
def analizar_lineal():
    resultados = request.json['resultados']
    interpretacion = interpretador_lineal.interpretar(resultados)
    return jsonify({'interpretacion': interpretacion})

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

        # Obtener el contexto del problema desde el formulario
        contexto = request.form.get('contexto')

        # Interpretar los resultados con el contexto
        interpretacion = interpretador_transporte.interpretar(resultados, contexto)

        return render_template('resultados_transporte.html', resultados=resultados, interpretacion=interpretacion, datos=datos)

    return render_template('transporte.html')

@app.route('/ple', methods=['GET', 'POST'])
def ple():
    if request.method == 'POST':
        archivo = request.files['archivo']
        archivo.save('entrada_ple.txt')

        lector = LectorPLE("entrada_ple.txt")
        if not lector.leer_archivo():
            return "Error al leer el archivo de entrada"

        datos = lector.obtener_datos()
        solver = SolverPLE(datos)
        solver.crear_modelo()
        resultados = solver.resolver()

        # Incluir el tipo de problema en los resultados
        resultados['tipo'] = datos.get('tipo', 'min')  # Por defecto es minimización

        # Obtener el contexto del problema desde el formulario
        contexto = request.form.get('contexto')

        # Interpretar los resultados con el tipo de problema y el contexto
        interpretacion = interpretador_ple.interpretar(resultados, resultados['tipo'], contexto)

        return render_template('resultados_ple.html', resultados=resultados, interpretacion=interpretacion)

    return render_template('ple.html')

# Rutas para análisis de resultados
@app.route('/analizar_transporte', methods=['POST'])
def analizar_transporte():
    # Verifica que los datos estén en formato JSON
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser en formato JSON"}), 400

    # Obtiene los resultados y el contexto del cuerpo de la solicitud
    data = request.json
    resultados = data.get('resultados')
    contexto = data.get('contexto')

    if not resultados:
        return jsonify({"error": "El campo 'resultados' es requerido"}), 400

    # Genera la interpretación con el contexto
    interpretacion = interpretador_transporte.interpretar(resultados, contexto)
    return jsonify({'interpretacion': interpretacion})

@app.route('/analizar_ple', methods=['POST'])
def analizar_ple():
    # Verifica que los datos estén en formato JSON
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser en formato JSON"}), 400

    # Obtiene los resultados y el contexto del cuerpo de la solicitud
    data = request.json
    resultados = data.get('resultados')
    contexto = data.get('contexto')

    if not resultados:
        return jsonify({"error": "El campo 'resultados' es requerido"}), 400

    # Obtener el tipo de problema (min o max) desde los resultados
    tipo_problema = resultados.get('tipo', 'min')  # Por defecto es minimización

    # Genera la interpretación con el tipo de problema y el contexto
    interpretacion = interpretador_ple.interpretar(resultados, tipo_problema, contexto)
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
@app.route('/bigm')
def bigm():
    
    return render_template('bigm.html')  

@app.route('/vogel')
def vogel():
    
    return render_template('vogel.html')  
@app.route('/resolver_bigm', methods=['POST'])
def resolver_bigm():
    # Obtener datos del formulario
    funcion_objetivo = list(map(float, request.form['funcion_objetivo'].split(',')))
    restricciones = [linea.split(',') for linea in request.form['restricciones'].split('\n')]
    tipo_problema = request.form['tipo_problema']

    # Crear y resolver el problema
    problema = GranM(funcion_objetivo, restricciones, tipo_problema)
    problema.resolver()
    resultados = problema.obtener_resultados()

    # Mostrar resultados
    return render_template('bigm_resultados.html', iteraciones=resultados['iteraciones'], solucion_optima=resultados['solucion_optima'])

if __name__ == '__main__':
    app.run(debug=True)