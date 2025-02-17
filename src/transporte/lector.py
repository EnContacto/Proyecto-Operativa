class LectorTransporte:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.origenes = []
        self.destinos = []
        self.costos = []
        self.ofertas = []
        self.demandas = []
        
    def leer_archivo(self):
        """Lee el archivo de texto y extrae la información del problema de transporte."""
        try:
            with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
                
                # Leer número de orígenes y destinos
                num_origenes = int(lineas[0].strip())
                num_destinos = int(lineas[1].strip())
                
                # Leer nombres de orígenes
                self.origenes = lineas[2].strip().split()
                if len(self.origenes) != num_origenes:
                    raise ValueError("Número de orígenes no coincide")
                
                # Leer nombres de destinos
                self.destinos = lineas[3].strip().split()
                if len(self.destinos) != num_destinos:
                    raise ValueError("Número de destinos no coincide")
                
                # Leer matriz de costos
                linea_actual = 4
                for i in range(num_origenes):
                    costos_fila = [float(x) for x in lineas[linea_actual + i].strip().split()]
                    if len(costos_fila) != num_destinos:
                        raise ValueError(f"Número incorrecto de costos en fila {i+1}")
                    self.costos.append(costos_fila)
                
                # Leer ofertas
                linea_actual += num_origenes
                self.ofertas = [float(x) for x in lineas[linea_actual].strip().split()]
                if len(self.ofertas) != num_origenes:
                    raise ValueError("Número de ofertas no coincide con orígenes")
                
                # Leer demandas
                self.demandas = [float(x) for x in lineas[linea_actual + 1].strip().split()]
                if len(self.demandas) != num_destinos:
                    raise ValueError("Número de demandas no coincide con destinos")
                
                # Verificar balance de oferta y demanda
                total_oferta = sum(self.ofertas)
                total_demanda = sum(self.demandas)
                if abs(total_oferta - total_demanda) > 1e-10:
                    print("Advertencia: El problema no está balanceado")
                    print(f"Total oferta: {total_oferta}, Total demanda: {total_demanda}")
                
            return True
            
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            return False
    
    def obtener_datos(self):
        """Retorna todos los datos del problema."""
        return {
            'origenes': self.origenes,
            'destinos': self.destinos,
            'costos': self.costos,
            'ofertas': self.ofertas,
            'demandas': self.demandas
        }