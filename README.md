Para la materia de optimización 2025-1   Métodos Heurísticos de Optimización: Colonia de Hormigas

# 🐜 Visualizador ACO para el Problema del Viajante (TSP)

Este proyecto es una aplicación de escritorio en Python con interfaz gráfica (GUI) que permite visualizar el funcionamiento del algoritmo de optimización por colonia de hormigas (ACO) aplicado al problema del viajante de comercio (TSP).

## 🚀 Características

- Agrega ciudades interactivamente con clics en el gráfico.
- Ajusta parámetros como número de hormigas, iteraciones, y coeficientes del algoritmo ACO.
- Visualiza el progreso de la optimización iteración por iteración.
- Muestra:
  - Ruta actual más corta encontrada.
  - Distancia total del camino.
  - Iteración donde se encontró el último mejor camino.
- Conexiones visuales entre todas las ciudades.
- Botones de control para ejecutar, detener y limpiar.

## 📸 Captura de pantalla

![image](https://github.com/user-attachments/assets/7927387d-bc84-4ca2-9367-f21f8aaac216)


## 🧱 Requisitos

- Python 3.7+
- Bibliotecas:

1. 📂 Cómo usar
  Clona el repositorio:
  git clone https://github.com/tuusuario/visualizador-aco.git
  cd visualizador-aco

2. Ejecuta la aplicación:

3. Usa la GUI:

  Haz clic en el área blanca para agregar ciudades.
  
  Ajusta los parámetros.
  
  Haz clic en "Ejecutar ACO" para iniciar la optimización.
  
  Puedes detener el proceso con el botón "Detener" o "Limpiar" para empezar de nuevo.



⚙️ Parámetros
  Hormigas: cantidad de hormigas simuladas por iteración.
  Iteraciones: número máximo de ciclos de optimización.
  Alpha (α): influencia de las feromonas.
  Beta (β): influencia de la heurística (distancia).
  Rho (ρ): tasa de evaporación de feromonas.
  Q: cantidad de feromonas depositadas por hormiga.

📚 Conceptos clave
  El algoritmo ACO (Ant Colony Optimization) es una técnica de metaheurística inspirada en el comportamiento de las hormigas reales para encontrar caminos óptimos en grafos. Este proyecto muestra su aplicación al clásico problema del viajante, donde se busca el recorrido más corto que pase por todas las ciudades una sola vez.
