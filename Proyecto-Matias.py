'''
Análisis de ventas de una empresa de electrodomésticos
'''

print('\n' + '='*72)
print("--- 1. IMPORTACIÓN Y RECONOCIMIENTO DEL ARCHIVO ---")
print('='*72)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carga del DataFrame
df = pd.read_excel('C:/Users/matia/Documentos/Documents/Resumen paralelo 4 (Autosaved)/02 - Cursos/Cilsa - PYTHON/Clase 9/ventas_electrodomesticos_integrador.xlsx')

# Exploración inicial
print(f"\n> Primeras filas: \n{df.head()}\n")
print(f"> Últimas filas: \n{df.tail()}\n")
print(f"> Filas y columnas del DataFrame: {df.shape}\n")
print(f"> Etiquetas de las columnas: \n{df.columns}\n")
print(f"> Tipos de datos de las columnas: \n{df.dtypes}\n")

print("-" * 50)
print("Resumen de .info():")
df.info()
print("-" * 50)

print(f"\n> Estadísticas generales automáticas: \n{df.describe().round(2)}\n")

print("\n--- Respuestas a las preguntas de exploración ---")
print(f"• Cantidad de variables (columnas): {len(df.columns)}")
print(f"• Variables numéricas detectadas:\n{df.select_dtypes(include=['number']).dtypes}\n")
print(f"• Cantidad de registros (filas): {df.shape[0]}")
print(f"• Variables categóricas detectadas:\n{df.select_dtypes(include=['object']).dtypes}\n")

print("• ¿Qué información representa cada fila?")
print("Cada fila representa una transacción de venta individual. Contiene el registro detallado de un producto vendido, incluyendo variables de tiempo, ubicación, datos del cliente, métricas financieras y el estado de la entrega.")


print('\n' + '='*72)
print("--- 2. CALIDAD Y PREPARACIÓN DE LOS DATOS ---")
print('='*72)

print(f"\n> Valores faltantes por columna: \n{df.isna().sum()[df.isna().sum() > 0]}\n")

print("> Filas que contienen algún valor nulo para análisis visual:")
print(df[df.isnull().any(axis=1)]) 

# Relleno de nulos para futuros cálculos
df['Descuento_Porc'] = df['Descuento_Porc'].fillna(0) 
df['Costo_Envio'] = df['Costo_Envio'].fillna(0)

print(f"\n> Cantidad de registros duplicados: {df.duplicated().sum()}")

print("\n> Control de posibles inconsistencias:")
print(f"  - Registros con Precio Unitario menor o igual a 0: {len(df[df['Precio_Unitario'] <= 0])}")
print(f"  - Registros con Cantidad menor o igual a 0: {len(df[df['Cantidad'] <= 0])}")
print(f"  - Registros con Descuentos fuera de rango (0-100%): {len(df[(df['Descuento_Porc'] < 0) | (df['Descuento_Porc'] > 100)])}")
print("  - Ventas canceladas que de todas formas tienen calificación:")
print(df[(df['Estado_Venta'] == 'Cancelado') & (df['Calificacion'].notna())])

print("\n> Valores únicos en columnas categóricas (Control de ortografía):")
print(f"  - Sucursales: {sorted(df['Sucursal'].unique())}")
print(f"  - Ciudades:   {sorted(df['Ciudad'].unique())}")
print(f"  - Canales:    {sorted(df['Canal'].unique())}")
print(f"  - Vendedores: {sorted(df['Vendedor'].unique())}")
print(f"  - Categorías: {sorted(df['Categoria'].unique())}")
print(f"  - Marcas:     {sorted(df['Marca'].unique())}")
print(f"  - Estados:    {sorted(df['Estado_Venta'].unique())}")


print('\n' + '='*72)
print("--- 3. CREAR NUEVAS VARIABLES ---")
print('='*72)

print("\n> Calculando y agregando nuevas columnas financieras...")
df['Total_bruto'] = df['Cantidad'] * df['Precio_Unitario']
df['Monto_Descuento'] = (df['Total_bruto'] * df['Descuento_Porc']).astype(int)
df['Importe_venta'] = df['Total_bruto'] - df['Monto_Descuento'] + df['Costo_Envio']
print("¡Columnas creadas con éxito! ('Total_bruto', 'Monto_Descuento', 'Importe_venta')")


print('\n' + '='*72)
print("--- 4. ANÁLISIS EXPLORATORIO GENERAL ---")
print('='*72)

columnas_analisis = ['Cantidad', 'Precio_Unitario', 'Descuento_Porc', 'Costo_Envio', 'Calificacion', 'Importe_venta']

for col in columnas_analisis:
    print(f"\n--- Estadísticos detallados de la columna: '{col}' ---")
    print(f"  Min: {df[col].min().round(2)} | Max: {df[col].max().round(2)}")
    print(f"  Promedio: {df[col].mean().round(2)} | Mediana: {df[col].median().round(2)}")
    print(f"  Desviación Estándar: {df[col].std().round(2)}")
    print(f"  Resumen describe:\n{df[col].describe().round(2)}")


print('\n' + '='*72)
print("--- 5. ANÁLISIS POR SUCURSAL ---")
print('='*72)

print("\n• Cantidad de operaciones por sucursal:")
print(df.groupby('Sucursal')['ID_Venta'].count())

print("\n• Facturación total por sucursal:")
print(df.groupby('Sucursal')['Importe_venta'].sum().round(2))

print("\n• Unidades vendidas por categoría en cada sucursal:")
print(df.groupby(['Sucursal', 'Categoria'])['Cantidad'].sum())

print("\n• Importe promedio de las ventas por sucursal:")
print(df.groupby('Sucursal')['Importe_venta'].mean().round(2))


print('\n' + '='*72)
print("--- 6. COMPARATIVA: CANAL ONLINE VS PRESENCIAL ---")
print('='*72)

print("\n• Unidades totales vendidas por Canal:")
print(df.groupby('Canal')['Cantidad'].sum())

print("\n• Importe promedio por transacción según el Canal:")
print(df.groupby('Canal')['Importe_venta'].mean().round(2))

print("\n• Facturación total por Canal (Solo Ventas Entregadas):")
facturacion_canales_entregados = df[df['Estado_Venta'] == 'Entregada'].groupby('Canal')['Importe_venta'].sum().round(2)
print(facturacion_canales_entregados)

print("\n• Distribución de tasas de descuento aplicadas por Canal:")
print(df.groupby('Canal')['Descuento_Porc'].value_counts())

print("\n• Distribución de costos de envío cobrados por Canal:")
print(df.groupby('Canal')['Costo_Envio'].value_counts())

print("\n• Tipos de clientes frecuentes por Canal:")
print(df.groupby('Canal')['Tipo_Cliente'].value_counts())

print("\n• Categorías más vendidas según el Canal:")
print(df.groupby('Canal')['Categoria'].value_counts())

print(f'\nEscribir una breve interpretación de las diferencias observadas.\n')

print("Interpretación del análisis por Canal:El canal Online se consolida como el principal motor de la empresa, liderando tanto en volumen de operaciones (20 frente a 16 del Presencial) como en rentabilidad por ticket, alcanzando un importe promedio de $571.815,00 (considerablemente superior a los $370.184,00 del canal físico). Este mayor rendimiento digital se ve impulsado por la integración de costos de envío y una política de descuentos más agresiva y variada, que actúa como un claro incentivo para el consumidor. En cuanto al perfil del comprador, el cliente particular mantiene el liderazgo absoluto en ambas modalidades. Por último, la categoría de Pequeños Electrodomésticos se posiciona como el producto estrella del negocio, registrando la mayor frecuencia de transacciones tanto en el entorno virtual como en las tiendas presenciales.")

print('\n' + '='*72)
print("--- 7. ANÁLISIS DE DESEMPEÑO POR VENDEDOR ---")
print('='*72)

print("\n• Ranking: Cantidad de operaciones por Vendedor:")
print(df.groupby('Vendedor')['ID_Venta'].count().sort_values(ascending=False))

print("\n• Ranking: Unidades físicas vendidas por Vendedor:")
print(df.groupby('Vendedor')['Cantidad'].sum().sort_values(ascending=False))

print("\n• Ranking: Facturación total (Solo Ventas Entregadas) por Vendedor:")
facturacion_vendedor_entregados = df[df['Estado_Venta'] == 'Entregada'].groupby('Vendedor')['Importe_venta'].sum().round(2).sort_values(ascending=False)
print(facturacion_vendedor_entregados)

print("\n• Ranking: Calificación promedio de clientes por Vendedor:")
print(df.groupby('Vendedor')['Calificacion'].mean().sort_values(ascending=False))

print("\nInterpretación del desempeño por Vendedor:\n" \
"El ranking de volumen de operaciones está liderado por Diego Fernández, Lucía Gómez, Nicolás Díaz y Martín López. Al analizar en detalle los comportamientos, se observan perfiles comerciales muy marcados:\nDiego Fernández se posiciona como el vendedor más eficiente y valioso para el negocio: lidera la facturación total y posee una de las mejores calificaciones promedio, lo que demuestra un excelente equilibrio entre rentabilidad y satisfacción al cliente.\nNicolás Díaz representa el perfil de volumen o 'mayorista': aunque no lidera en facturación, es el vendedor que logró colocar la mayor cantidad de unidades físicas de productos en el mercado.Esta diferencia nos permite concluir que mientras Diego Fernández se enfoca en transacciones de mayor valor unitario (tickets más altos), Nicolás Díaz tracciona el movimiento de stock mediante ventas masivas de menor valor.")


print('\n' + '='*72)
print("--- 8. ANÁLISIS DE PRODUCTOS Y CATEGORÍAS ---")
print('='*72)

print("\n• Categorías con mayor cantidad de unidades vendidas:")
print(df.groupby('Categoria')['Cantidad'].sum().sort_values(ascending=False))

print("\n• Categorías que generaron mayor facturación:")
print(df.groupby('Categoria')['Importe_venta'].sum().sort_values(ascending=False))

print("\n• Productos con mayor volumen de unidades vendidas:")
print(df.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False))

print("\n• Marcas con mayor presencia (cantidad de transacciones):")
print(df.groupby('Marca')['ID_Venta'].count().sort_values(ascending=False))

print("\n• Comparativa de Precios Unitarios por Categoría (Mín, Prom, Máx):")
precios_por_categoria = df.groupby('Categoria')['Precio_Unitario'].agg(['min', 'mean', 'max']).round(2)
precios_por_categoria.columns = ['Precio Mínimo', 'Precio Promedio', 'Precio Máximo']
print(precios_por_categoria.sort_values(by='Precio Promedio', ascending=False))


print('\n' + '='*72)
print("--- 9. VISUALIZACIÓN DE DATOS ---")
print('='*72)


'Gráfico 1: El rendimiento de las Sucursales'
'Tipo de gráfico:'
'Dos subplots de barras verticales (uno a la izquierda de cantidad y otro a la derecha de facturación) con fondo negro.'
'¿Qué intenta mostrar? '
'El mapa geográfico del negocio. Muestra que la sucursal Centro es el motor de liquidez y captación de caja de la empresa, mientras que las demás sucursales se mantienen estables en cantidad de operaciones pero con menor recaudación.'

# 1. Activamos el fondo oscuro
plt.style.use('dark_background')

# 2. Calcular los totales
resumen = df.groupby("Sucursal")[["Cantidad", "Importe_venta"]].sum()
sucursales = resumen.index

# 3. Crear una ventana con DOS gráficos separados (uno izquierda y otro derecha)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8))

# --- GRÁFICO 1: CANTIDAD (Izquierda) ---
ax1.bar(sucursales, resumen["Cantidad"], color="orange")
ax1.set_title("Cantidad total vendida por Sucursal")
ax1.set_ylabel("Unidades")

# --- GRÁFICO 2: FACTURACIÓN (Derecha) ---
ax2.bar(sucursales, resumen["Importe_venta"], color="blue")
ax2.set_title("Facturación total por Sucursal")
ax2.set_ylabel("Monto ($)")

# Formateamos los millones del gráfico de abajo con puntos separadores de miles
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(",", ".")))

# Ajustamos el diseño para que no se encimen los títulos
plt.tight_layout()

# Mostrar los gráficos
plt.show()


'Gráfico 2: El desempeño de los Vendedores (El dolor del personal)'
'Tipo de gráfico: Dos subplots de barras verticales (Cantidad de tickets vs. Facturación real).'
'¿Qué intenta mostrar?'
'El comportamiento de los empleados.'
'Diego Fernández lidera la recaudación, mientras que Nicolás Díaz es un perfil de volumen que mueve muchas unidades físicas pero de menor valor.'

# 1. Activamos el fondo oscuro
plt.style.use('dark_background')

# 2. Calcular los totales
resumen_vendedor = df.groupby("Vendedor")[["Cantidad", "Importe_venta"]].sum()
vendedores = resumen_vendedor.index

# 3. Crear una ventana con DOS gráficos separados (uno arriba y otro abajo)
# subplots(2, 1) crea 2 filas y 1 columna de gráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# --- GRÁFICO 1: CANTIDAD (Arriba) ---
ax1.bar(vendedores, resumen_vendedor["Cantidad"], color="orange")
ax1.set_title("Cantidad total vendida por Vendedor")
ax1.set_ylabel("Unidades")
ax1.tick_params(axis='x', rotation=45)

# --- GRÁFICO 2: FACTURACIÓN (Abajo) ---
ax2.bar(vendedores, resumen_vendedor["Importe_venta"], color="blue")
ax2.set_title("Facturación total por Vendedor")
ax2.set_ylabel("Monto ($)")
ax2.tick_params(axis='x', rotation=45)

# Ajustamos el diseño para que no se encimen los títulos
plt.tight_layout()

# Mostrar los gráficos
plt.show()


'Gráfico 3: La estrategia comercial por Canal (El dolor del cliente)'
'Tipo de gráfico: Gráfico combinado de Boxplot + Stripplot (Nube de puntos sobre cajas transparentes).'
'¿Qué intenta mostrar?'
'Intentamos mostrar cómo la flexibilidad en los descuentos define el éxito de cada canal: '
'el canal presencial es conservador y se estanca en el 10% de descuento, mientras que el canal online rompe ese techo, genera un 50% de sus ventas con descuentos de doble dígito (entre 10% y 20%) y amplía significativamente su volumen comercial."'

# 1. Activamos el fondo oscuro
plt.style.use('dark_background')
plt.figure(figsize=(8, 6))

# 2. Dibujamos las cajas de fondo (Muestran el promedio y los rangos generales)
sns.boxplot(
    data=df,
    x='Canal',
    y='Descuento_Porc',
    palette='muted',
    boxprops=dict(alpha=0.3)  # Hace la caja semi-transparente para que no tape los puntos
)

# 3. Dibujamos los puntos individuales de cada venta (¡El Stripplot!)
sns.stripplot(
    data=df,
    x='Canal',
    y='Descuento_Porc',
    palette='cool',
    size=8,          # Hacemos los puntos grandecitos para que se vean bien
    jitter=0.2,      # Separa los puntos un poquito hacia los costados para que no se encimen
    linewidth=1,     # Borde blanco fino a cada punto para que resalte
    edgecolor='white'
)

# 4. Títulos y etiquetas claras para la entrega
plt.title('Relación de Descuentos Aplicados según el Canal de Venta', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Canal de Venta', fontsize=11)
plt.ylabel('Porcentaje de Descuento (%)', fontsize=11)

# 5. Formateamos el eje Y para que muestre el signo de porcentaje de forma prolija
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x*100)}%"))

plt.tight_layout()
plt.show()


'Gráfico 4: Dispersión de Precios de Venta por Categoría'
'Tipo de gráfico: Gráfico de dispersión categórica (Stripplot) con dimensiones de Precio Unitario (Eje Y) y Unidades por Venta (Color/Hue).'
'¿Qué intenta mostrar?'
'La diferencia entre el volumen físico de ventas y el valor nominal de cada operación para entender qué mueve la caja bruta. Demuestra visualmente que "Heladeras" y "Televisores" registran los tickets individuales más elevados del negocio (alcanzando techos de entre $1.0 y $1.4 millones), consolidándose como los principales captadores de ingresos brutos por operación. En contraste, "Pequeños Electrodomésticos" compensa su bajo precio unitario mediante el volumen de unidades por ticket, siendo la única categoría que registra compras de 3 y 4 unidades juntas (puntos naranjas y amarillos) en el extremo inferior de precios.'


plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

# Llevamos el Precio al eje Y para ver la dispersión real del dinero
sns.stripplot(
    data=df,
    x='Categoria',
    y='Precio_Unitario',          # <--- El precio ahora determina la altura del punto
    hue='Cantidad',       # <--- El color te dice cuántas unidades se llevaron
    palette='spring',     # Una paleta eléctrica (rosa/amarillo) que resalta perfecto en negro
    size=8,          
    jitter=0.25,          # Aumentamos el jitter para que se dispersen más de lado y no se tapen
    alpha=0.8
)

plt.title('Dispersión de Precios de Venta por Categoría', fontsize=12, fontweight='bold')
plt.xlabel('Categoría')
plt.ylabel('Precio Unitario ($)')
plt.xticks(rotation=15)
plt.legend(title='Unidades por Venta', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


try:
    # Intentamos guardar el archivo de forma normal
    df.to_csv(
        "Preparado_Ventas_Electrodomésticos.csv",
        index=False,
        encoding='utf-8-sig'
    )
    print("\n" + "="*50)
    print("¡PROYECTO FINALIZADO Y GUARDADO CON ÉXITO!")
    print("Se creó el archivo: 'Ventas_Electrodomésticos.csv'")
    print("="*50)

except PermissionError:
    # Si el archivo está abierto en Excel, avisa y DETIENE el programa
    print("\n" + "!"*50)
    print("⚠️ ERROR DE PERMISOS: No se pudo guardar el archivo.")
    print("El archivo 'Ventas_Electrodomésticos.csv' está abierto en Excel.")
    print("Por favor, cierralo y vuelve a ejecutar el script en VS Code.")
    print("!"*50 + "\n")
    
    exit()

except Exception as e:
    print(f"\nOcurrió un error inesperado al guardar: {e}")
