# Proyecto de Programación Lineal en Python

Este proyecto ha sido desarrollado en **Python** y utiliza diversas librerías como `pulp`, `matplotlib` y otras necesarias para resolver problemas de **programación lineal**. El sistema funciona completamente **offline** y genera resultados en formato `.txt` para facilitar su interpretación.

## Estructura del Proyecto
El repositorio se organiza en tres carpetas principales, cada una dedicada a un tema específico:

1. **Programación Lineal**
   - Contiene scripts y recursos para resolver problemas generales de programación lineal.
   - Instrucciones detalladas sobre cómo ejecutar los scripts.
   
2. **Transporte**
   - Incluye herramientas para resolver problemas de optimización en redes de transporte.
   - Métodos y algoritmos específicos para minimizar costos de distribución.

3. **Redes**
   - Contiene implementaciones de algoritmos de optimización en redes de flujo.
   - Modelos aplicables a problemas de comunicación, logística y más.

## Instalación y Dependencias
Para ejecutar este proyecto, es necesario contar con **Python 3.11** y las siguientes librerías:

```bash
pip install pulp matplotlib numpy pandas
```

## Uso y Ejecución
Cada carpeta contiene un archivo `README.md` con instrucciones detalladas para la ejecución de los scripts. En general, el proceso es:

1. Colocar el archivo de entrada en el formato esperado.
2. Ejecutar el script correspondiente.
3. Revisar los resultados en el archivo de salida `.txt` generado.

## Formato de Resultados
Cada ejecución genera un archivo `.txt` con los siguientes datos:
- Valores óptimos de la función objetivo.
- Valores de las variables de decisión.
- Información sobre restricciones y dualidad.
- Representación gráfica del resultado (cuando aplica).

## Contribuciones
Si deseas contribuir al proyecto, puedes enviar un **pull request** o reportar problemas en la sección de **issues**.

## Licencia
Este proyecto está distribuido bajo la licencia MIT. Para más información, consulta el archivo `LICENSE`.

