# Método Húngaro — Asignación Óptima con Análisis de IA

Este proyecto es una aplicación de escritorio desarrollada en Python utilizando **Tkinter** para resolver problemas de asignación mediante el **Método Húngaro** (tanto para la minimización de costos como para la maximización de beneficios). Además, incorpora un módulo de Inteligencia Artificial conectado a la API de **Groq** (`llama-3.1-8b-instant`) para generar análisis e interpretaciones prácticas de las asignaciones óptimas desde la perspectiva de la investigación de operaciones.

El algoritmo está desarrollado por completo utilizando la lógica pura del método sin depender de librerías externas de optimización (como `scipy` o `numpy`).

Proyecto desarrollado por: **Ignacio Aceña** y **Roberto Siracusa**

---

## 🚀 Características principales

- **Grilla Dinámica y Editable**: Permite cambiar la dimensión del problema ($N \times N$) de 2x2 hasta 10x10. Se pueden editar libremente los nombres de los trabajadores (filas) y las tareas (columnas).
- **Herramientas de Entrada**: Generación de matrices aleatorias para pruebas rápidas y botón de limpieza completa.
- **Visualización Detallada**: Muestra de forma desglosada los pasos lógicos del algoritmo (reducción por filas/columnas, líneas de cobertura e iteraciones).
- **Resaltado Visual**: Las celdas que forman parte de la solución óptima se destacan automáticamente en la interfaz en un tono verde de éxito.
- **Consultor de IA Integrado**: Un botón dedicado envía el resultado óptimo y la estructura del problema a Groq para obtener una interpretación ejecutiva y resumida (máx. 150 palabras).

---

## 📁 Estructura del Proyecto

El código está modularizado de la siguiente manera:

- `met_hungaro.py`: Contiene el core del algoritmo del Método Húngaro, el manejo de estados de la matriz y toda la interfaz gráfica responsiva construida con Tkinter (TTK).
- `groq_client.py`: Módulo compartido encargado de gestionar las llamadas HTTP POST hacia la API de Groq empleando **únicamente la librería estándar de Python** (`urllib`, `json`, `os`). Carga automáticamente las variables de entorno locales.
- `.env`: Archivo de configuración local para el almacenamiento seguro de credenciales.

---

## ⚙️ Configuración del Entorno y Seguridad

El sistema requiere una clave de API de Groq para habilitar el botón de análisis de IA. Por motivos de seguridad, **esta clave nunca debe hardcodearse en el código fuente**.

### Configuración del archivo `.env`

1. En la raíz del proyecto (junto a `met_hungaro.py` y `groq_client.py`), crea un archivo de texto llamado `.env`.
2. Añade tu API Key de Groq siguiendo el formato de clave-valor exacto:
```
GROQ_API_KEY=tu_clave_aqui
```
3. Guarda el archivo. El módulo `groq_client.py` se encargará de cargar esta variable de entorno automáticamente al ejecutar la aplicación.