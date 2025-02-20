from src.modelos.interpretador_base import InterpretadorBase

class InterpretadorPLE(InterpretadorBase):
    def interpretar(self, resultados, tipo_problema, contexto=None):
        """Genera una interpretación de los resultados de programación lineal entera."""
        # Determinar si es minimización o maximización
        tipo_problema_str = "minimización" if tipo_problema == 'min' else "maximización"
        
        # Crear el prompt con el contexto y los resultados
        prompt = (
            "A continuación se presentan los resultados de un problema de programación lineal entera:\n"
            f"Tipo de problema: {tipo_problema_str}\n"
            f"Valor óptimo de la función objetivo: {resultados['valor_objetivo']}\n"
            f"Valores de las variables: {resultados['variables']}\n"
            f"Precios sombra: {resultados['dual_restricciones']}\n"
            f"Costos reducidos: {resultados['reducidos']}\n"
            f"Análisis de sensibilidad: {resultados['sensibilidad']}\n"
            "Por favor, analiza e interpreta estos resultados en un contexto real, teniendo en cuenta que las variables son enteras.\n"
            "Además, explica qué significa cada valor de los precios sombra obtenidos.\n"
        )

        # Agregar el contexto del problema si está disponible
        if contexto:
            prompt += f"Contexto del problema: {contexto}\n"

        return self.generar_interpretacion(prompt)