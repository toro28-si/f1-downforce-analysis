"""
ANÁLISIS AERODINÁMICO EN FÓRMULA 1
====================================
Este script analiza cómo el ángulo del alerón delantero afecta:
- Downforce (carga aerodinámica)
- Drag (resistencia)
- Velocidad máxima en curvas
- Tiempo total por vuelta (circuito de Mónaco)

Autor: Rodrigo Estrada
Fecha: [19/05/26]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score

# ==================================================
# 1. PARÁMETROS DEL PROBLEMA
# ==================================================

angulos = np.arange(1, 31, 2)          # Ángulos del alerón: 1° a 30° cada 2°
p = 1.225                              # Densidad del aire (kg/m³)
A = 1.5                                # Área frontal del coche (m²)
v_m = 87                               # Velocidad máxima en recta (m/s)
L = 3337                               # Longitud del circuito (m)
m = 800                                # Masa del coche (kg)
l_c = 0.80 * L                         # 80% del circuito son curvas
l_rectas = 0.20 * L                    # 20% son rectas
coef_friccion = 1.5                    # Coeficiente de fricción neumático-pista
r_curvas_prom = 50                     # Radio promedio de curvas (m)

# ==================================================
# 2. FUNCIONES FÍSICAS
# ==================================================

def C_L(angulo):
    """Coeficiente de sustentación (negativo = downforce)"""
    return -0.3 - 0.5 * np.radians(angulo)

def C_D(angulo):
    """Coeficiente de arrastre (positivo)"""
    return 0.2 + 0.015 * np.radians(angulo) + 0.0005 * np.radians(angulo)**2

def downforce(angulo):
    """Fuerza vertical que pega el coche al suelo (N)"""
    return 0.5 * C_L(angulo) * p * A * v_m**2

def drag(angulo):
    """Resistencia aerodinámica (N)"""
    return 0.5 * C_D(angulo) * p * A * v_m**2

# ==================================================
# 3. CÁLCULOS PRINCIPALES
# ==================================================

# Calcular downforce y drag
Df = downforce(angulos)
Dg = drag(angulos)

# Velocidad promedio afectada por drag
v_prom_kmh = 300 - 0.03 * Dg
v_prom_mps = v_prom_kmh / 3.6

# Velocidad máxima en curvas (depende del downforce)
v_max_curvas = np.sqrt(r_curvas_prom * coef_friccion * (9.81 + Df / m))

# Verificar si la velocidad promedio es alcanzable en curvas
v_prom_mps_ajustada = np.where(v_prom_mps < v_max_curvas, v_prom_mps, v_max_curvas)

# Tiempos por sección
T_rectas = l_rectas / v_prom_mps_ajustada
T_curvas = l_c / v_max_curvas
T_total = T_curvas + T_rectas

# ==================================================
# 4. CREAR DATAFRAME
# ==================================================

df = pd.DataFrame({
    'angulo_grados': angulos,
    'C_L': C_L(angulos),
    'C_D': C_D(angulos),
    'downforce_N': Df,
    'drag_N': Dg,
    'vel_promedio_kmh': v_prom_kmh,
    'vel_promedio_mps': v_prom_mps_ajustada,
    'vel_max_curvas_mps': v_max_curvas,
    'tiempo_rectas_s': T_rectas,
    'tiempo_curvas_s': T_curvas,
    'tiempo_total_s': T_total
})

# ==================================================
# 5. ENCONTRAR ÁNGULO ÓPTIMO
# ==================================================

mejor_angulo = df.loc[df['tiempo_total_s'].idxmin(), 'angulo_grados']
mejor_tiempo = df['tiempo_total_s'].min()
peor_tiempo = df['tiempo_total_s'].max()
mejora_porcentaje = (peor_tiempo - mejor_tiempo) / peor_tiempo * 100

print("=" * 60)
print("RESULTADOS DEL ANÁLISIS")
print("=" * 60)
print(f"Ángulo óptimo del alerón: {mejor_angulo}°")
print(f"Tiempo por vuelta óptimo: {mejor_tiempo:.2f} s")
print(f"Mejora respecto al peor ángulo: {mejora_porcentaje:.1f}%")
print("=" * 60)

# ==================================================
# 6. MÉTRICAS DE CALIDAD DEL MODELO
# ==================================================

# Evaluar correlación entre downforce y tiempo
correlacion_df_tiempo = np.corrcoef(df['downforce_N'], df['tiempo_total_s'])[0, 1]

# Modelo simple: predecir tiempo a partir de downforce (para demostrar R²)
from sklearn.linear_model import LinearRegression
X = df[['downforce_N']].values
y = df['tiempo_total_s'].values
modelo = LinearRegression()
modelo.fit(X, y)
y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)

print(f"\nMÉTRICAS DE CALIDAD:")
print(f"Correlación downforce-tiempo: {correlacion_df_tiempo:.3f}")
print(f"R² (tiempo ~ downforce): {r2:.4f}")
print(f"MSE: {mse:.4f}")

# ==================================================
# 7. EXPORTAR RESULTADOS A CSV
# ==================================================

df.to_csv('resultados_F1_monaco.csv', index=False)
print(f"\n✅ Resultados guardados en 'resultados_F1_monaco.csv'")

# ==================================================
# 8. GRÁFICAS PROFESIONALES
# ==================================================

sns.set_theme(style="whitegrid", palette="viridis")

# Gráfica 1: Downforce y Drag vs Ángulo
plt.figure(figsize=(10, 6))
plt.plot(df['angulo_grados'], df['downforce_N'], 'b-', linewidth=2.5, label='Downforce')
plt.plot(df['angulo_grados'], df['drag_N'], 'r-', linewidth=2.5, label='Drag')
plt.xlabel('Ángulo del alerón (grados)', fontsize=12)
plt.ylabel('Fuerza (N)', fontsize=12)
plt.title('Downforce y Drag vs Ángulo del Alerón', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('downforce_drag_vs_angulo.png', dpi=150)
plt.show()

# Gráfica 2: Tiempo por vuelta vs Ángulo
plt.figure(figsize=(10, 6))
plt.plot(df['angulo_grados'], df['tiempo_total_s'], 'g-', linewidth=2.5)
plt.scatter(mejor_angulo, mejor_tiempo, color='red', s=100, 
            label=f'Óptimo: {mejor_angulo}° → {mejor_tiempo:.1f}s', zorder=5)
plt.xlabel('Ángulo del alerón (grados)', fontsize=12)
plt.ylabel('Tiempo por vuelta (s)', fontsize=12)
plt.title('Tiempo por vuelta en Mónaco vs Ángulo del Alerón', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('tiempo_vs_angulo.png', dpi=150)
plt.show()

# Gráfica 3: Velocidad máxima en curvas vs Ángulo
plt.figure(figsize=(10, 6))
plt.plot(df['angulo_grados'], df['vel_max_curvas_mps'], 'purple', linewidth=2.5)
plt.xlabel('Ángulo del alerón (grados)', fontsize=12)
plt.ylabel('Velocidad máxima en curvas (m/s)', fontsize=12)
plt.title('Velocidad en curva vs Ángulo del Alerón', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('velocidad_curva_vs_angulo.png', dpi=150)
plt.show()

# Gráfica 4: Comparación de tiempos por sección
plt.figure(figsize=(10, 6))
plt.plot(df['angulo_grados'], df['tiempo_rectas_s'], 'orange', linewidth=2, label='Rectas')
plt.plot(df['angulo_grados'], df['tiempo_curvas_s'], 'blue', linewidth=2, label='Curvas')
plt.plot(df['angulo_grados'], df['tiempo_total_s'], 'black', linewidth=2.5, 
         linestyle='--', label='Total')
plt.xlabel('Ángulo del alerón (grados)', fontsize=12)
plt.ylabel('Tiempo (s)', fontsize=12)
plt.title('Descomposición del tiempo por vuelta', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('tiempos_por_seccion.png', dpi=150)
plt.show()

print("\n✅ Gráficas guardadas como PNG")