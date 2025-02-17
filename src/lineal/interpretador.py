from src.modelos.interpretador_base import InterpretadorBase

class InterpretadorPL(InterpretadorBase):
    def interpretar(self, resultados):
        """Genera una interpretación de los resultados de programación lineal."""
        prompt = (
            "A continuación se presentan los resultados de un problema de programación lineal:\n"
            f"Estado de la solución: {resultados['estado']}\n"
            f"Valor óptimo de la función objetivo: {resultados['valor_objetivo']}\n"
            f"Valores de las variables: {resultados['variables']}\n"
            f"Precios sombra: {resultados['dual_restricciones']}\n"
            f"Costos reducidos: {resultados['reducidos']}\n"
            f"Análisis de sensibilidad: {resultados['sensibilidad']}\n"
            "Por favor, analiza e interpreta estos resultados en un contexto real."
        )
        return self.generar_interpretacion(prompt)