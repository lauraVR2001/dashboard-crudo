import pandas as pd
import glob
import os
import re
import unicodedata

# Función para capitalizar columnas
def capitalizar_columnas(df):
    # Capitaliza solo la primera letra, el resto minúscula, para todas las columnas
    def cap(col):
        col = str(col)
        # Si la columna es un año numérico (ej. 2013) o completamente numérica, dejar igual
        if col.isdigit():
            return col
        # Manejar columnas vacías
        if col == '':
            return col
        return col[:1].upper() + col[1:].lower()
    df.columns = [cap(col) for col in df.columns]
    return df

ruta_archivos = r"D:\Analisis producción de gas 2025\Bases_produccion_crudo"
archivos = glob.glob(os.path.join(ruta_archivos, "Produccion_Fiscalizada_Crudo_*.xlsx"))

print("Archivos encontrados:")
for archivo in archivos:
    print(archivo)

tablas_mensuales = []

produccion_anual_por_campo = []

# Meses esperados en el archivo (normalizados)
meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']

# Función para normalizar nombres de columnas
def normalizar_columna(s):
    if pd.isnull(s):
        return ''
    s = str(s).lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\s+', '', s)
    return s

for archivo in archivos:
    nombre_archivo = os.path.basename(archivo)
    match = re.search(r'(20\d{2})', nombre_archivo)
    if match:
        anio = int(match.group(1))
    else:
        print(f"No se pudo extraer el año de: {nombre_archivo}")
        continue
    xls = pd.ExcelFile(archivo)
    hoja = xls.sheet_names[0]
    df = pd.read_excel(xls, sheet_name=hoja)
    # Normalizar nombres de columnas
    df.columns = [normalizar_columna(col) for col in df.columns]
    # Mostrar columnas para depuración
    print(f"Columnas normalizadas en hoja '{hoja}' de {nombre_archivo}: {list(df.columns)}")
    # Verifica que existan todas las columnas de meses
    if not all(m in df.columns for m in meses):
        print(f"Faltan columnas de meses en {hoja} de {nombre_archivo}")
        continue
    # Suma anual por campo
    df['total_anual'] = df[meses].sum(axis=1)
    df['año'] = anio
    # Guardar todas las columnas clave si existen
    columnas_clave = ['departamento','municipio','operadora','campo','contrato','año','total_anual']
    cols_presentes = [col for col in columnas_clave if col in df.columns or col in ['año','total_anual']]
    # Si faltan columnas clave, agrégalas vacías
    for col in columnas_clave:
        if col not in df.columns and col not in ['año','total_anual']:
            df[col] = ''
    # LIMPIEZA DE NOMBRES DE CAMPO SEGÚN MAPEO
    def limpiar_campo(nombre):
        if pd.isnull(nombre):
            return nombre
        nombre = str(nombre).strip().upper()
        reemplazos = {
            'TECA-COCORNA': 'AREA TECA-COCORNA',
            'ÁREA TECA - COCORNA': 'AREA TECA-COCORNA',
            'COPA UNIFICADO': 'COPA',
            'PETIRROJO UNIFICADO': 'PETIRROJO',
            'YNF LA LOMA': 'LA LOMA YNF',
            'TEMPRANILLO UNIFICADO': 'TEMPRANILLO',
            'UNIFICADO PALOGRANDE': 'PALOGRANDE UNIFICADO',
            'UNIFICADO RÍO CEIBAS': 'RIO CEIBAS',
            'UNIFICADO RIO CEIBAS': 'RIO CEIBAS',
            'LOMALARGA': 'LOMA LARGA',
            'VALDIVIA - ALMAGRO': 'VALDIVIA ALMAGRO',
            'LLANOS 58-4': 'LLANOS-58-4',
            'PAVAS - CACHIRA': 'PAVAS CACHIRA',
            'ACAE-SAN MIGUEL': 'ACAE SAN MIGUEL',
            'LISAMA NORTE': 'LISAMA-NORTE',
        }
        nombre = nombre.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('AREA TECA - COCORNA', 'AREA TECA-COCORNA')
        nombre = nombre.replace('Ñ', 'N')
        nombre = nombre.replace('  ', ' ')
        if nombre in reemplazos:
            return reemplazos[nombre]
        return nombre
    df['campo_limpio'] = df['campo'].apply(limpiar_campo)
    # Usar campo_limpio en lugar de campo en los reportes
    columnas_clave_limpio = ['departamento','municipio','operadora','campo_limpio','contrato','año','total_anual']
    df_campo = df[[col if col != 'campo' else 'campo_limpio' for col in columnas_clave]].copy()
    df_campo.columns = columnas_clave  # Renombrar para mantener consistencia
    produccion_anual_por_campo.append(df_campo)
    # Tabla mensual total
    totales_mes = {mes: df[mes].sum(skipna=True) for mes in meses}
    tabla_mes = pd.DataFrame({'Mes': list(totales_mes.keys()), 'Total': list(totales_mes.values())})
    tabla_mes['Año'] = anio
    tablas_mensuales.append(tabla_mes)
    print(f"\nTotales mensuales para {anio} - hoja {hoja}:")
    print(tabla_mes[['Año','Mes','Total']].to_string(index=False))

df_mensual = pd.concat(tablas_mensuales, ignore_index=True)
## df_resumen = pd.DataFrame(resumen_anual).sort_values('Año')  # Eliminado

# --- NUEVO REPORTE: Serie anual por campo (una hoja, columnas: campo, 2013, 2014, ... 2024) ---
if produccion_anual_por_campo:
    df_campo_anual = pd.concat(produccion_anual_por_campo, ignore_index=True)
    # Agrupar por todas las columnas clave y año
    columnas_clave = ['departamento','municipio','operadora','campo','contrato']
    df_campo_anual = df_campo_anual.groupby(columnas_clave + ['año'], as_index=False)['total_anual'].sum()
    # Definir todos_los_anios para uso posterior
    todos_los_anios = sorted(df_campo_anual['año'].unique())
    # --- Agregar cuenca a la hoja principal ---
    archivo_cuencas = r"D:\Analisis producción de gas 2025\cuencas_campos_crudo.xlsx"
    df_cuencas = pd.read_excel(archivo_cuencas)
    df_cuencas.columns = df_cuencas.columns.str.strip().str.upper()
    def normalizar_campo(s):
        if pd.isnull(s):
            return ''
        s = str(s).upper().strip()
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        s = re.sub(r'\s+', ' ', s)
        return s
    df_campo_anual['CAMPO_NORM'] = df_campo_anual['campo'].apply(normalizar_campo)
    df_cuencas['CAMPO_NORM'] = df_cuencas['CAMPO'].apply(normalizar_campo)
    df_serie_merge = pd.merge(df_campo_anual, df_cuencas, how='left', left_on='CAMPO_NORM', right_on='CAMPO_NORM')
    # Asignación manual de cuenca a campos específicos (igual que en el bloque de cuenca)
    asignaciones_manual = {
        'SANTO DOMINGO UNIFICADO': 'LLAO',
        'ALBERTA': 'LLAO',
        'KIMBO': 'LLAO',
        'CUERVA NOROESTE': 'LLAO',
        'BARQUE4': 'LLAO',
        'HABANERO': 'VMM',
        'PALERMO - SANTA CLARA UNIFICADO': 'VSM',
        'AMANECER': 'LLAO',
        'COPLERO': 'LLAO',
        'GALOPE': 'LLAO',
        'SEJE': 'LLAO',
        'VALDIVIA-ALMAGRO': 'LLAO',
        'LLANOS 58': 'LLAO',
        'QUIRIYANA': 'CAG-PUT',
        'MIRTO - AGAPANTO UNIFICADO': 'CAG-PUT',
        'LILIA-ANGIE UNIFICADO': 'VMM',
        'PROGRE3': 'LLAO',
    }
    def normalizar_nombre_campo_manual(nombre):
        if pd.isnull(nombre):
            return ''
        nombre = str(nombre).upper().strip()
        nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn')
        nombre = re.sub(r'\s+', ' ', nombre)
        return nombre
    for campo, cuenca in asignaciones_manual.items():
        campo_norm = normalizar_nombre_campo_manual(campo)
        mask = (df_serie_merge['CUENCA'].isnull()) & (df_serie_merge['CAMPO_NORM'] == campo_norm)
        df_serie_merge.loc[mask, 'CUENCA'] = cuenca
    # Reorganizar para hoja principal: año, Departamento, Municipio, Operadora, Campo, Contrato, Cuenca, Produccion Crudo
    df_serie = df_serie_merge.rename(columns={
        'año': 'Año',
        'departamento': 'Departamento',
        'municipio': 'Municipio',
        'operadora': 'Operadora',
        'campo': 'Campo',
        'contrato': 'Contrato',
        'total_anual': 'Produccion Crudo',
        'CUENCA': 'Cuenca'
    })
    # Ordenar columnas
    df_serie = df_serie[['Año', 'Departamento', 'Municipio', 'Operadora', 'Campo', 'Contrato', 'Cuenca', 'Produccion Crudo']]
    # 2. Hoja: por campo (serie de tiempo)
    df_campo_pivot = df_campo_anual.pivot_table(index='campo', columns='año', values='total_anual', aggfunc='sum', fill_value=0)
    df_campo_pivot = df_campo_pivot.reset_index()
    cols_campo = ['campo'] + [anio for anio in todos_los_anios]
    df_campo_pivot = df_campo_pivot[cols_campo]

    # 3. Hoja: por cuenca (serie de tiempo)
    archivo_cuencas = r"D:\Analisis producción de gas 2025\cuencas_campos_crudo.xlsx"
    df_cuencas = pd.read_excel(archivo_cuencas)
    df_cuencas.columns = df_cuencas.columns.str.strip().str.upper()
    def normalizar_campo(s):
        if pd.isnull(s):
            return ''
        s = str(s).upper().strip()
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        s = re.sub(r'\s+', ' ', s)
        return s
    df_campo_anual['CAMPO_NORM'] = df_campo_anual['campo'].apply(normalizar_campo)
    df_cuencas['CAMPO_NORM'] = df_cuencas['CAMPO'].apply(normalizar_campo)
    df_merge = pd.merge(df_campo_anual, df_cuencas, how='left', left_on='CAMPO_NORM', right_on='CAMPO_NORM')
    if 'CUENCA' in df_merge.columns:
        # Asignación manual de cuenca a campos específicos
        asignaciones_manual = {
            'SANTO DOMINGO UNIFICADO': 'LLAO',
            'ALBERTA': 'LLAO',
            'KIMBO': 'LLAO',
            'CUERVA NOROESTE': 'LLAO',
            'BARQUE4': 'LLAO',
            'HABANERO': 'VMM',
            'PALERMO - SANTA CLARA UNIFICADO': 'VSM',
            'AMANECER': 'LLAO',
            'COPLERO': 'LLAO',
            'GALOPE': 'LLAO',
            'SEJE': 'LLAO',
            'VALDIVIA-ALMAGRO': 'LLAO',
            'LLANOS 58': 'LLAO',
            'QUIRIYANA': 'CAG-PUT',
            'MIRTO - AGAPANTO UNIFICADO': 'CAG-PUT',
            'LILIA-ANGIE UNIFICADO': 'VMM',
            'PROGRE3': 'LLAO',
        }
        # Normalizar nombres para comparar
        def normalizar_nombre_campo_manual(nombre):
            if pd.isnull(nombre):
                return ''
            nombre = str(nombre).upper().strip()
            nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn')
            nombre = re.sub(r'\s+', ' ', nombre)
            return nombre
        for campo, cuenca in asignaciones_manual.items():
            campo_norm = normalizar_nombre_campo_manual(campo)
            mask = (df_merge['CUENCA'].isnull()) & (df_merge['CAMPO_NORM'] == campo_norm)
            df_merge.loc[mask, 'CUENCA'] = cuenca
        df_cuenca_anual = df_merge.groupby(['CUENCA', 'año'], as_index=False)['total_anual'].sum()
        df_cuenca_pivot = df_cuenca_anual.pivot_table(index='CUENCA', columns='año', values='total_anual', aggfunc='sum', fill_value=0)
        df_cuenca_pivot = df_cuenca_pivot.reset_index()
        cols_cuenca = ['CUENCA'] + [anio for anio in todos_los_anios]
        df_cuenca_pivot = df_cuenca_pivot[cols_cuenca]
        # Agregar fila 'SIN CUENCA' con sumatoria de campos sin cuenca
        sin_cuenca_df = df_merge[df_merge['CUENCA'].isnull()]
        if not sin_cuenca_df.empty:
            suma_sin_cuenca = sin_cuenca_df.groupby('año')['total_anual'].sum()
            fila = ['SIN CUENCA'] + [suma_sin_cuenca.get(anio, 0) for anio in todos_los_anios]
            df_cuenca_pivot.loc[len(df_cuenca_pivot)] = fila
    else:
        df_cuenca_pivot = pd.DataFrame()

    # Exportar todo a un solo Excel
    archivo_final = os.path.join(ruta_archivos, "produccion_crudo_anual.xlsx")
    # Capitalizar columnas antes de exportar
    df_serie = capitalizar_columnas(df_serie)
    df_campo_pivot = capitalizar_columnas(df_campo_pivot)
    df_cuenca_pivot = capitalizar_columnas(df_cuenca_pivot)
    with pd.ExcelWriter(archivo_final) as writer:
        df_serie.to_excel(writer, sheet_name="Serie_Anual", index=False)
        df_campo_pivot.to_excel(writer, sheet_name="Por_Campo", index=False)
        df_cuenca_pivot.to_excel(writer, sheet_name="Por_Cuenca", index=False)
        # 4. Hoja: Linea anual (suma total por año)
        try:
            # Calcular totales anuales y variación porcentual año a año
            df_linea_anual = df_campo_anual.groupby('año', as_index=False)['total_anual'].sum()
            df_linea_anual = df_linea_anual.rename(columns={'año': 'Año', 'total_anual': 'Produccion Crudo'})
            # Ordenar años descendente
            df_linea_anual = df_linea_anual.sort_values('Año', ascending=False).reset_index(drop=True)
            # Calcular variación porcentual año a año
            df_linea_anual['Variacion %'] = df_linea_anual['Produccion Crudo'].pct_change(periods=-1) * 100
            # La variación del año más reciente será NaN, la dejamos vacía
            df_linea_anual['Variacion %'] = df_linea_anual['Variacion %'].apply(lambda x: '' if pd.isnull(x) else round(x,2))
            df_linea_anual = capitalizar_columnas(df_linea_anual)
            df_linea_anual.to_excel(writer, sheet_name="Linea_Anual", index=False)
        except Exception as e:
            print(f"No se pudo crear la hoja 'Linea_Anual': {e}")

        # 5. Hoja: Linea_Tiempo (totales anuales por campo en formato ancho)
        try:
            # Pivotear para tener una fila por combinación y columnas por año
            columnas_base = ['departamento','municipio','operadora','campo','contrato']
            df_tiempo = df_campo_anual.pivot_table(index=columnas_base, columns='año', values='total_anual', aggfunc='sum', fill_value=0)
            df_tiempo = df_tiempo.reset_index()
            # Ordenar columnas: base + años en orden ascendente
            cols_tiempo = columnas_base + sorted([col for col in df_tiempo.columns if isinstance(col, int)])
            df_tiempo = df_tiempo[cols_tiempo]
            # Capitalizar columnas
            df_tiempo = capitalizar_columnas(df_tiempo)
            df_tiempo.to_excel(writer, sheet_name="Linea_Tiempo", index=False)
        except Exception as e:
            print(f"No se pudo crear la hoja 'Linea_Tiempo': {e}")
        except Exception as e:
            print(f"No se pudo crear la hoja 'Linea_Anual': {e}")
    print(f"\nArchivo Excel generado con 3 hojas: {archivo_final}")

    # Imprimir totales anuales en consola
    totales_anuales = df_campo_anual.groupby('año')['total_anual'].sum()
    print("\nTotales anuales de producción de crudo:")
    for anio, total in totales_anuales.items():
        print(f"Año {anio}: {total:,.2f}")

