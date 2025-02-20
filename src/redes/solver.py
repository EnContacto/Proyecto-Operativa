import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import networkx as nx

class SolverRedes:
    def __init__(self, datos):
        self.datos = datos
        self.grafo = nx.Graph()
        
        # Construir el grafo
        for nodo in self.datos['nodos']:
            self.grafo.add_node(nodo)
        for conexion in self.datos['conexiones']:
            nodo1, nodo2, distancia = conexion
            self.grafo.add_edge(nodo1, nodo2, weight=distancia)
        
    def calcular_ruta_mas_corta(self, inicio, fin):
        """Calcula la ruta más corta entre dos nodos usando Dijkstra."""
        print("Nodos en el grafo:", list(self.grafo.nodes))  # Depuración
        print("Conexiones en el grafo:", list(self.grafo.edges))  # Depuración
        
        if inicio not in self.grafo or fin not in self.grafo:
            print(f"Error: Uno de los nodos no existe en el grafo.")
            return None
        
        try:
            ruta = nx.dijkstra_path(self.grafo, inicio, fin)
            distancia = nx.dijkstra_path_length(self.grafo, inicio, fin)
            
            # Generar el gráfico
            self.generar_grafico(ruta)
            
            return {
                'ruta': ruta,
                'distancia': distancia
            }
        except nx.NetworkXNoPath:
            print(f"No hay ruta entre {inicio} y {fin}.")
            return None
    
    def generar_grafico(self, ruta):
        """Genera y guarda un gráfico del grafo con la ruta más corta resaltada."""
        pos = nx.spring_layout(self.grafo)
        plt.figure()
        
        # Dibujar el grafo completo
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        
        # Resaltar la ruta más corta
        path_edges = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_nodes(self.grafo, pos, nodelist=ruta, node_color='orange')
        nx.draw_networkx_edges(self.grafo, pos, edgelist=path_edges, edge_color='red', width=2)
        
        # Guardar el gráfico en un archivo
        plt.savefig('static/grafo.png')
        plt.close()