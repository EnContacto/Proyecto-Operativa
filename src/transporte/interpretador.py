from src.modelos.interpretador_base import InterpretadorBase

class InterpretadorTransporte(InterpretadorBase):
    def interpretar(self, resultados, contexto=None):
        """Genera una interpretación de los resultados de transporte."""
        # Crear el prompt con el contexto y los resultados
        prompt = (
            "A continuación se presentan los resultados de un problema de transporte:\n"
            f"Estado de la solución: {resultados['estado']}\n"
            f"Costo total de transporte: {resultados['valor_objetivo']}\n"
            f"Flujos óptimos:\n"
        )

        # Agregar detalles de los flujos óptimos
        for ruta, flujo in resultados['flujos'].items():
            origen, destino = ruta.split('-')
            prompt += f"- Desde {origen} hasta {destino}: {flujo} unidades\n"

        # Agregar precios sombra (duales) de orígenes y destinos
        prompt += "\nPrecios sombra (duales) de los orígenes:\n"
        for origen, dual in resultados['analisis_sensibilidad']['origenes'].items():
            prompt += f"- {origen}: {dual['dual']}\n"

        prompt += "\nPrecios sombra (duales) de los destinos:\n"
        for destino, dual in resultados['analisis_sensibilidad']['destinos'].items():
            prompt += f"- {destino}: {dual['dual']}\n"

        # Agregar el contexto del problema si está disponible
        if contexto:
            prompt += f"\nContexto del problema: {contexto}\n"

        # Solicitar una interpretación detallada
        prompt += (
            "\nPor favor, analiza e interpreta estos resultados en un contexto real.\n"
            "Explica qué significa cada valor de los precios sombra obtenidos.\n"
            "Ten en cuenta el contexto proporcionado para personalizar la interpretación.\n"
        )

        return self.generar_interpretacion(prompt)