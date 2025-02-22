from openai import OpenAI
import os

class InterpretadorBase:
    def __init__(self):
        # Configura tu API Key de OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)  # Inicializa el cliente de OpenAI

    def generar_interpretacion(self, prompt):
        """Genera una interpretación usando GPT-3.5 Turbo."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Selecciona GPT-3.5 Turbo
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de problemas de optimización."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,  # Longitud máxima de la respuesta
                temperature=0.7  # Controla la creatividad (0 = más determinista)
            )
            return response.choices[0].message.content  # Accede al contenido de la respuesta
        except Exception as e:
            return f"Error al generar la interpretación: {str(e)}"