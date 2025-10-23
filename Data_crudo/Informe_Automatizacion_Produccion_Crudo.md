# Informe Técnico: Automatización de la Producción de Crudo

## Descripción General

El script `Automatizacion_crudo.py` automatiza el procesamiento, consolidación y reporte de datos de producción fiscalizada de crudo en Colombia. Permite transformar archivos Excel mensuales/anuales en reportes consolidados, facilitando el análisis histórico y la visualización de tendencias por campo y cuenca.

## Objetivos
- Unificar y limpiar datos de producción de crudo provenientes de múltiples archivos Excel.
- Generar reportes anuales y mensuales por campo y cuenca.
- Facilitar la trazabilidad y el análisis de la producción a lo largo de los años.

## Principales Funcionalidades
1. **Lectura y Normalización de Archivos**
   - Busca archivos con el patrón `Produccion_Fiscalizada_Crudo_*.xlsx` en la carpeta de trabajo.
   - Normaliza nombres de columnas y campos para evitar inconsistencias.
   - Capitaliza nombres de columnas para mejorar la presentación.

2. **Procesamiento de Datos**
   - Calcula la suma anual de producción por campo y por mes.
   - Limpia y estandariza nombres de campos según mapeos definidos.
   - Asocia cada campo a su cuenca correspondiente, incluyendo asignaciones manuales.

3. **Generación de Reportes en Excel**
   - Exporta un archivo `produccion_crudo_anual.xlsx` con las siguientes hojas:
     - **PRODUCC. ANUAL CRUDO**: Detalle anual por campo, departamento, municipio, operadora y contrato.
     - **PRODUCC. POR CAMPO**: Serie de tiempo por campo, con columnas para cada año.
     - **PRODUCC. POR CUENCA**: Serie de tiempo por cuenca, con columnas para cada año.
     - **VARIACIÓN ANUAL**: Totales por año, con variación porcentual año a año.
     - **LINEA DE TIEMPO ANUAL**: Totales anuales en formato de línea de tiempo (campos fijos + años como columnas).

4. **Validaciones y Limpieza**
   - Verifica la presencia de columnas de meses esperados.
   - Rellena columnas clave vacías para mantener consistencia.
   - Imprime en consola los totales mensuales y anuales para depuración.

## Estructura de Salida
- **Archivo generado:** `produccion_crudo_anual.xlsx`
- **Hojas principales:**
  - `PRODUCC. ANUAL CRUDO`
  - `PRODUCC. POR CAMPO`
  - `PRODUCC. POR CUENCA`
  - `VARIACIÓN ANUAL`
  - `LINEA DE TIEMPO ANUAL`

## Recomendaciones de Uso
- Mantener los archivos fuente en la carpeta especificada y con el formato esperado.
- Actualizar el mapeo de campos y cuencas si se agregan nuevos campos o cambian denominaciones.
- Revisar los reportes generados para validar la integridad de los datos.

## Beneficios
- Ahorro de tiempo en la consolidación y análisis de datos históricos.
- Reducción de errores manuales en la preparación de reportes.
- Facilidad para generar visualizaciones y análisis comparativos año a año.

---

**Autor:** Laura Valentina Romero R.
**Fecha de última actualización:** Octubre 2025
