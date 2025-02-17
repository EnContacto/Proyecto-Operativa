from src.modelos.interpretador_base import InterpretadorBase

class InterpretadorTransporte(InterpretadorBase):
    def interpretar(self, resultados):
        """Genera una interpretación de los resultados de transporte."""
        prompt = (
            "A continuación se presentan los resultados de un problema de transporte:\n"
            f"Estado de la solución: {resultados['estado']}\n"
            f"Costo total de transporte: {resultados['valor_objetivo']}\n"
            f"Flujos óptimos: {resultados['flujos']}\n"
            f"Análisis de sensibilidad: {resultados['analisis_sensibilidad']}\n"
            "Por favor, analiza e interpreta estos resultados en un contexto real."
        )
        return self.generar_interpretacion(prompt)