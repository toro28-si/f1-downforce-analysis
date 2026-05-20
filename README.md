# 🏎️ Análisis Aerodinámico en Fórmula 1

## 🎯 Objetivo
Determinar el ángulo óptimo del alerón delantero de un F1 para minimizar el tiempo por vuelta en el circuito de Mónaco.

## 📊 Variables analizadas
- **Downforce**: Fuerza que pega el coche al suelo (aumenta con el ángulo)
- **Drag**: Resistencia aerodinámica (también aumenta con el ángulo)
- **Velocidad máxima en curvas**: Limitada por downforce y fricción
- **Tiempo por vuelta**: Suma de tiempo en rectas + curvas

## 🔬 Metodología
1. Se modelan los coeficientes aerodinámicos C_L y C_D como funciones del ángulo
2. Se calcula downforce y drag para cada ángulo
3. Se estima la velocidad máxima en rectas (limitada por drag) y curvas (limitada por downforce)
4. Se calcula el tiempo por vuelta para cada configuración
5. Se identifica el ángulo que minimiza el tiempo total

## 📈 Resultados clave
- **Ángulo óptimo**: XX° (el código lo calcula automáticamente)
- **Mejora de tiempo**: X.X% respecto al peor ángulo
- **Correlación downforce-tiempo**: -0.XX (más downforce = menos tiempo)

## 🛠️ Tecnologías
- Python 3.x
- NumPy, Pandas (manejo de datos)
- Matplotlib, Seaborn (visualización)
- Scikit-learn (métricas R² y MSE)

## 📁 Archivos generados
- `resultados_F1_monaco.csv` - Datos completos de la simulación
- `*.png` - Gráficas profesionales del análisis

## ▶️ Cómo ejecutar
```bash
python F1.py
