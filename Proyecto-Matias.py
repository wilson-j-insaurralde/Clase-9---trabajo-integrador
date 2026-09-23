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

# Detecta automáticamente la carpeta actual donde está este archivo .py
carpeta_actual = os.path.dirname(__file__) if '__file__' in locals() else os.getcwd()
ruta_excel = os.path.join(carpeta_actual, 'ventas_electrodomesticos_integrador.xlsx')

# Carga del DataFrame garantizada en cualquier entorno
df = pd.read_excel(ruta_excel)

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

print(f"\n> Estadísticas generales de las columnas numéricas: \n{df.describe().round(2)}\n")

print("\n--- Respuestas a las preguntas de exploración ---")
print(f"• Cantidad de variables (columnas): {len(df.columns)}")
print(f"• Variables numéricas detectadas:\n{df.select_dtypes(include=['number']).dtypes}\n")
print(f"• Cantidad de registros (filas): {df.shape[0]}")
print(f"• Variables categóricas detectadas:\n{df.select_dtypes(include=['str']).dtypes}\n")

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
print(f"\nSe rellenaron nulos en las columnas 'Descuento_Porc' y 'Costo_Envio")
print(f"\nCalificacion: Se conservan los NaN porque corresponden a ventas Canceladas o Pendientes.\nRellenar con 0 alteraría erróneamente el promedio de satisfacción de clientes.")

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
print(f"\nMostramos el dataframe con las columnas agregadas: \n{df.head()}")


print('\n' + '='*72)
print("--- 4. ANÁLISIS EXPLORATORIO GENERAL ---")
print('='*72)

columnas_analisis = ['Cantidad', 'Precio_Unitario', 'Descuento_Porc', 'Costo_Envio', 'Calificacion', 'Importe_venta']

resumen_estadistico = df[columnas_analisis].describe().round(2)
print("--- Estadísticas Descriptivas Generales ---")
print(f'\n{resumen_estadistico}')

# Filtro para trabajar solo con las ventas que fueron entregadas
df_entregado = df[df['Estado_Venta'] == 'Entregada']

print("\n--- Métricas Clave Globales ---")

def formato_moneda(val):
    """Formatea un número al estilo regional: $1.234.567,89"""
    if pd.isna(val): 
        return ""
    # Formato inicial USA: 1,234,567.89
    res = f"${val:,.2f}"
    # Intercambio de coma por punto y punto por coma
    return res.replace(",", "X").replace(".", ",").replace("X", ".")

# Consideramos todas las operaciones
print(f"Total de operaciones registradas: {len(df)}") 
# Solo se consideran las operaciones que figuran como entregadas
print(f"Total de unidades vendidas:       {df_entregado['Cantidad'].sum()} unidades")
print(f"Facturación bruta:                {formato_moneda(df_entregado['Total_bruto'].sum())}")
print(f"Total otorgado en descuentos:     {formato_moneda(df_entregado['Monto_Descuento'].sum())}")
print(f"Total recaudado por envíos:       {formato_moneda(df_entregado['Costo_Envio'].sum())}")
print(f"Facturación neta total:           {formato_moneda(df_entregado['Importe_venta'].sum())}")
print(f"Ticket promedio por venta:        {formato_moneda(df_entregado['Importe_venta'].mean())}")
calif_promedio = f"{df_entregado['Calificacion'].mean():.2f}".replace('.', ',')
print(f"Calificación promedio general:    {calif_promedio} / 5.0")

"""
Volumen de datos (count): El análisis se basa en 36 operaciones comerciales registradas. 

Volumen de compra por operación (Cantidad): Los clientes compran en promedio 1.31 productos por transacción. Lo más habitual es que compren 1 solo artículo (así lo indican el mínimo, el percentil 25%, 50% y 75%), siendo 4 la cantidad máxima registrada en una sola operación.

Precios de los productos (Precio_Unitario): Existe una altísima dispersión de precios (desviación estándar de ~$357,414.94). El producto más barato cuesta $52,000.00 y el más costoso alcanza los $1,450,000.00. La mitad de los productos vendidos se sitúan por debajo de los $457,500.00.

Estrategia de descuentos (Descuento_Porc): El descuento promedio aplicado es del 7% (0.07). El 75% de las transacciones reciben un descuento igual o inferior al 10%, alcanzando un beneficio máximo puntual del 20%. Cabe destacar que hay operaciones que no registraron ningún descuento (mínimo de 0%).

Logística (Costo_Envio): El costo de envío promedio por pedido es de $10,833.33. Hay transacciones donde el envío fue gratuito ($0.00, presente hasta el percentil 25%), mientras que el costo logístico más elevado fue de $38,000.00.

Satisfacción del cliente (Calificacion): La experiencia es mayoritariamente muy positiva, con una calificación media de 4.29 sobre 5. El 50% de los clientes calificó la compra con una nota perfecta de 5.00, y la puntuación más baja registrada fue de 3.00.

Facturación por venta (Importe_Venta): El ticket promedio de facturación se ubica en $482,201.39 por operación. La transacción de menor valor fue de $137,750.00, mientras que la venta más grande del período generó un ingreso de $1,275,600.00.
"""


print('\n' + '='*72)
print("--- 5. ANÁLISIS POR SUCURSAL ---")
print('='*72)

resumen_sucursal = df_entregado.groupby('Sucursal').agg(
    Cant_Operaciones=('ID_Venta', 'count'),
    Facturacion_Total=('Importe_venta', 'sum'),  # <-- Cambiado aquí
    Ticket_Promedio=('Importe_venta', 'mean')    # <-- Cambiado aquí
).sort_values(by='Facturacion_Total', ascending=False)

print("--- Resumen de Desempeño por Sucursal ---")

resumen_sucursal_formato = resumen_sucursal.copy()
resumen_sucursal_formato['Facturacion_Total'] = resumen_sucursal_formato['Facturacion_Total'].apply(formato_moneda)
resumen_sucursal_formato['Ticket_Promedio'] = resumen_sucursal_formato['Ticket_Promedio'].apply(formato_moneda)
print(f"\n{resumen_sucursal_formato}")

categorias_sucursal = df_entregado.groupby(['Sucursal', 'Categoria'])['Cantidad'].sum().reset_index()
# Ordenamos para que quede primero la sucursal y luego la categoría con más ventas
categorias_sucursal = categorias_sucursal.sort_values(by=['Sucursal', 'Cantidad'], ascending=[True, False])
print("\n--- Categorías con más unidades vendidas por Sucursal ---")
print(categorias_sucursal)

'''El negocio está liderado por la sucursal Centro, mientras que las demás muestran un comportamiento competitivo pero con tickets de menor valor.

Centro (El líder indiscutido): Es la sucursal que más operaciones registra (10) y la que genera el mayor volumen de ingresos con $6.563.250,00. Su éxito se debe a que tiene el Ticket Promedio más alto de toda la cadena ($656.325,00), lo que indica que vende productos de mayor valor unitario o más artículos por combo.

Sur (Segundo en facturación): Registra 9 operaciones y recauda $3.984.050,00. Aunque vende casi la misma cantidad de veces que el Centro, su ticket promedio es notablemente menor ($442.672,22).

Oeste (Menor volumen, buen ticket): Con solo 8 operaciones (la menor cantidad de la red), logra posicionarse en tercer lugar facturando $3.742.500,00 gracias a un sólido ticket promedio de $467.812,50 (el segundo más alto del negocio).

Norte (Mucha actividad, baja rentabilidad): Empata en cantidad de transacciones con la sucursal Sur (9 operaciones), pero queda última en facturación ($3.069.450,00) debido a que su ticket promedio es el más bajo de todos ($341.050,00).'''

print('\n' + '='*72)
print("--- 6. COMPARATIVA: CANAL ONLINE VS PRESENCIAL ---")
print('='*72)

comparativa_canal = df_entregado.groupby('Canal').agg(
    Operaciones=('ID_Venta', 'count'),
    Unidades_Totales=('Cantidad', 'sum'),
    Facturacion_Total=('Importe_venta', 'sum'),
    Ticket_Promedio=('Importe_venta', 'mean'),   
    Descuento_Promedio=('Descuento_Porc', 'mean'),
    Costo_Envio_Promedio=('Costo_Envio', 'mean')
)

print("\n--- Comparativa Global: Online vs Presencial ---")

comparativa_canal_formato = comparativa_canal.copy()
comparativa_canal_formato['Facturacion_Total'] = comparativa_canal_formato['Facturacion_Total'].apply(formato_moneda)
comparativa_canal_formato['Ticket_Promedio'] = comparativa_canal_formato['Ticket_Promedio'].apply(formato_moneda)
comparativa_canal_formato['Descuento_Promedio'] = (comparativa_canal_formato['Descuento_Promedio'] * 100).map('{:.2f}%'.format)
comparativa_canal_formato['Costo_Envio_Promedio'] = comparativa_canal_formato['Costo_Envio_Promedio'].apply(formato_moneda)

print(f"\n{comparativa_canal_formato}\n") 

print(f'\nEscribir una breve interpretación de las diferencias observadas.\n')

print("Interpretación del análisis por Canal:\nEl canal Online se consolida como el principal motor de la empresa, liderando tanto en volumen de operaciones (20 frente a 16 del Presencial) como en rentabilidad por ticket, alcanzando un importe promedio de $571.815,00 (considerablemente superior a los $370.184,00 del canal físico). Este mayor rendimiento digital se ve impulsado por la integración de costos de envío y una política de descuentos más agresiva y variada, que actúa como un claro incentivo para el consumidor. En cuanto al perfil del comprador, el cliente particular mantiene el liderazgo absoluto en ambas modalidades. Por último, la categoría de Pequeños Electrodomésticos se posiciona como el producto estrella del negocio, registrando la mayor frecuencia de transacciones tanto en el entorno virtual como en las tiendas presenciales.")

print('\n' + '='*72)
print("--- 7. ANÁLISIS DE DESEMPEÑO POR VENDEDOR ---")
print('='*72)

resumen_vendedores = df_entregado.groupby('Vendedor').agg(
    Operaciones=('ID_Venta', 'count'),
    Unidades_Vendidas=('Cantidad', 'sum'),
    Facturacion_Total=('Importe_venta', 'sum'),
    Ticket_Promedio=('Importe_venta', 'mean'),
    Calificacion_Promedio=('Calificacion', 'mean')
).sort_values(by='Facturacion_Total', ascending=False)

resumen_vendedores_formato = resumen_vendedores.copy()
resumen_vendedores_formato['Facturacion_Total'] = resumen_vendedores_formato['Facturacion_Total'].apply(formato_moneda)
resumen_vendedores_formato['Ticket_Promedio'] = resumen_vendedores_formato['Ticket_Promedio'].apply(formato_moneda)

print("--- Desempeño General de Vendedores ---")
print(f"\n{resumen_vendedores_formato.round(2)}\n")

print("\nInterpretación del desempeño por Vendedor:\n" \
"El ranking de volumen de operaciones está liderado por Diego Fernández, Lucía Gómez, Nicolás Díaz y Martín López. Al analizar en detalle los comportamientos, se observan perfiles comerciales muy marcados:\nDiego Fernández se posiciona como el vendedor más eficiente y valioso para el negocio: lidera la facturación total y posee una de las mejores calificaciones promedio, lo que demuestra un excelente equilibrio entre rentabilidad y satisfacción al cliente.\nNicolás Díaz representa el perfil de volumen o 'mayorista': aunque no lidera en facturación, es el vendedor que logró colocar la mayor cantidad de unidades físicas de productos en el mercado.Esta diferencia nos permite concluir que mientras Diego Fernández se enfoca en transacciones de mayor valor unitario (tickets más altos), Nicolás Díaz tracciona el movimiento de stock mediante ventas masivas de menor valor.")


print('\n' + '='*72)
print("--- 8. ANÁLISIS DE PRODUCTOS Y CATEGORÍAS ---")
print('='*72)

resumen_categorias = df_entregado.groupby('Categoria').agg(
    Operaciones=('ID_Venta', 'count'),
    Unidades_Vendidas=('Cantidad', 'sum'),
    Facturacion_Total=('Importe_venta', 'sum'),
    Precio_Unitario_Promedio=('Precio_Unitario', 'mean')
).sort_values(by='Facturacion_Total', ascending=False)

resumen_categorias_formato = resumen_categorias.copy()
resumen_categorias_formato['Facturacion_Total'] = resumen_categorias_formato['Facturacion_Total'].apply(formato_moneda)
resumen_categorias_formato['Precio_Unitario_Promedio'] = resumen_categorias_formato['Precio_Unitario_Promedio'].apply(formato_moneda)

print("--- Rendimiento por Categoría (Unidades, Facturación y Precio Promedio) ---")
print(resumen_categorias_formato.round(2))

print("\n--- 1. CATEGORÍAS CON MAYOR CANTIDAD DE UNIDADES VENDIDAS ---")
unidades_categoria = df_entregado.groupby("Categoria")["Cantidad"].sum()
print(unidades_categoria.sort_values(ascending=False))

print("\n--- 2. CATEGORÍAS CON MAYOR FACTURACIÓN ---")
facturacion_categoria = df_entregado.groupby("Categoria")["Importe_venta"].sum().sort_values(ascending=False)
facturacion_categoria_formato = facturacion_categoria.apply(formato_moneda)
print(facturacion_categoria_formato)

print("\n--- 3. PRODUCTOS MÁS FRECUENTES ---")
productos_frecuentes = df_entregado.groupby("Producto").size().head(5)
print(productos_frecuentes.sort_values(ascending=False))

print("\n--- 4. MARCAS CON MAYOR PRESENCIA ---")
marcas_presencia = df_entregado.groupby("Marca").size()
print(marcas_presencia.sort_values(ascending=False))

print("\n--- 5. DIFERENCIAS DE PRECIO ENTRE CATEGORÍAS ---")
precio_categoria = df_entregado.groupby("Categoria")["Precio_Unitario"].agg(
    Precio_Minimo='min',
    Precio_Maximo='max',
    Precio_Promedio='mean'
).sort_values(by='Precio_Promedio', ascending=False)

# 2. Creamos una copia para darle formato de pesos a las columnas numéricas
precio_categoria_formato = precio_categoria.copy()

precio_categoria_formato['Precio_Minimo'] = precio_categoria_formato['Precio_Minimo'].apply(formato_moneda)
precio_categoria_formato['Precio_Maximo'] = precio_categoria_formato['Precio_Maximo'].apply(formato_moneda)
precio_categoria_formato['Precio_Promedio'] = precio_categoria_formato['Precio_Promedio'].apply(formato_moneda)
print(precio_categoria_formato)


print('\n' + '='*72)
print("--- 9. VISUALIZACIÓN DE DATOS ---")
print('='*72)

# Configuración inicial del estilo de los gráficos
plt.style.use('dark_background')

"""
Gráfico 1: El rendimiento de las Sucursales
Tipo de gráfico: Dos subplots de barras verticales (Cantidad izquierda vs. Facturación derecha).
¿Qué intenta mostrar?: 
El mapa geográfico del negocio. Muestra que la sucursal Centro es el motor de liquidez y captación de caja de la empresa, mientras que las demás sucursales se mantienen estables en cantidad de operaciones pero con menor recaudación.
"""

# Calculamos los totales solo para lo efectivamente entregado
resumen_suc = df_entregado.groupby("Sucursal")[["Cantidad", "Importe_venta"]].sum()
sucursales = resumen_suc.index

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# --- GRÁFICO 1A: CANTIDAD ---
ax1.bar(sucursales, resumen_suc["Cantidad"], color="orange")
ax1.set_title("Cantidad total vendida por Sucursal\n(Solo Entregadas)")
ax1.set_ylabel("Unidades")

# --- GRÁFICO 1B: FACTURACIÓN ---
ax2.bar(sucursales, resumen_suc["Importe_venta"], color="blue")
ax2.set_title("Facturación total por Sucursal\n(Solo Entregadas)")
ax2.set_ylabel("Monto ($)")
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(",", ".")))

plt.tight_layout()
plt.show()


"""
Gráfico 2: El desempeño de los Vendedores (El dolor del personal)
Tipo de gráfico: Dos subplots de barras verticales (Cantidad de tickets vs. Facturación real).
¿Qué intenta mostrar?: 
El comportamiento de los empleados. Diego Fernández lidera la recaudación, mientras que Nicolás Díaz es un perfil de volumen que mueve muchas unidades físicas pero de menor valor.
"""

resumen_vend = df_entregado.groupby("Vendedor")[["Cantidad", "Importe_venta"]].sum()
vendedores = resumen_vend.index

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# --- GRÁFICO 2A: CANTIDAD ---
ax1.bar(vendedores, resumen_vend["Cantidad"], color="orange")
ax1.set_title("Cantidad total vendida por Vendedor (Solo Entregadas)")
ax1.set_ylabel("Unidades")
ax1.tick_params(axis='x', rotation=30)

# --- GRÁFICO 2B: FACTURACIÓN ---
ax2.bar(vendedores, resumen_vend["Importe_venta"], color="blue")
ax2.set_title("Facturación total por Vendedor (Solo Entregadas)")
ax2.set_ylabel("Monto ($)")
ax2.tick_params(axis='x', rotation=30)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}".replace(",", ".")))

plt.tight_layout()
plt.show()


"""
Gráfico 3: La estrategia comercial por Canal (El dolor del cliente)
Tipo de gráfico: Gráfico combinado de Boxplot + Stripplot (Nube de puntos sobre cajas transparentes).
¿Qué intenta mostrar?
Cómo la flexibilidad en los descuentos define el éxito de cada canal. El canal presencial es conservador y se estanca en el 10% de descuento, mientras que el canal online rompe ese techo, genera un 50% de sus ventas con descuentos de doble dígito (entre 10% y 20%) y amplía significativamente su volumen comercial.
"""

plt.figure(figsize=(8, 6))

sns.boxplot(
    data=df,  # Mantiene df general si deseas ver la política comercial histórica de descuentos
    x='Canal',
    y='Descuento_Porc',
    palette='muted',
    boxprops=dict(alpha=0.3)
)

sns.stripplot(
    data=df,
    x='Canal',
    y='Descuento_Porc',
    palette='cool',
    size=8,          
    jitter=0.2,      
    linewidth=1,     
    edgecolor='white'
)

plt.title('Relación de Descuentos Aplicados según el Canal de Venta', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Canal de Venta', fontsize=11)
plt.ylabel('Porcentaje de Descuento (%)', fontsize=11)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x)}%"))

plt.tight_layout()
plt.show()


"""
Gráfico 4: Dispersión de Precios de Venta por Categoría
Tipo de gráfico: Gráfico de dispersión categórica (Stripplot) con dimensiones de Precio Unitario (Eje Y) y Unidades por Venta (Color/Hue).
¿Qué intenta mostrar?: 
La diferencia entre el volumen físico de ventas y el valor nominal de cada operación para entender qué mueve la caja bruta. Demuestra visualmente que "Heladeras" y "Televisores" registran los tickets individuales más elevados del negocio (alcanzando techos de entre $1.0 y $1.4 millones), consolidándose como los principales captadores de ingresos brutos por operación. En contraste, "Pequeños Electrodomésticos" compensa su bajo precio unitario mediante el volumen de unidades por ticket, siendo la única categoría que registra compras de 3 y 4 unidades juntas (puntos naranjas y amarillos) en el extremo inferior de precios.
"""

plt.figure(figsize=(10, 6))

sns.stripplot(
    data=df_entregado,  # Enfocado en productos entregados reales
    x='Categoria',
    y='Precio_Unitario',          
    hue='Cantidad',       
    palette='spring',     
    size=8,          
    jitter=0.25,          
    alpha=0.8
)

plt.title('Dispersión de Precios de Venta por Categoría (Solo Entregadas)', fontsize=12, fontweight='bold')
plt.xlabel('Categoría')
plt.ylabel('Precio Unitario ($)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}".replace(",", ".")))
plt.xticks(rotation=15)
plt.legend(title='Unidades por Venta', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()


# Construimos la ruta de guardado dinámica para la misma carpeta del script
ruta_guardado = os.path.join(carpeta_actual, "Preparado_Ventas_Electrodomésticos.csv")

try:
    df.to_csv(
        ruta_guardado,
        index=False,
        encoding='utf-8-sig',
        sep=';'  # Opcional: Recomendado si tus profesores abren el CSV directo en Excel en español
    )
    print("\n" + "="*50)
    print("¡PROYECTO FINALIZADO Y GUARDADO CON ÉXITO!")
    print(f"Se creó el archivo en: {ruta_guardado}")
    print("="*50)

except PermissionError:
    # Si el archivo está abierto en Excel, avisa y DETIENE el programa
    print("\n" + "!"*50)
    print("⚠️ ERROR DE PERMISOS: No se pudo guardar el archivo.")
    print("El archivo 'Preparado_Ventas_Electrodomésticos.csv' está abierto en Excel.")
    print("Por favor, ciérralo y vuelve a ejecutar el script en VS Code.")
    print("!"*50 + "\n")
    exit()

except Exception as e:
    print(f"\nOcurrió un error inesperado al guardar: {e}")


