import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# --------------------------------------------
# Cargar el CSV desde la ruta especificada
# --------------------------------------------

csv_path = r'C:\Users\jesus\OneDrive - UNIVERSIDAD NACIONAL DE INGENIERIA\INKAMOTORS\REPORTES\MES ACTUAL\PRUEBA3_PIVOTEADA.csv'

# Leer el CSV
df = pd.read_csv(csv_path)

# Limpiar espacios y convertir a minúsculas en los nombres de las columnas
df.columns = df.columns.str.strip().str.lower()

# --------------------------------------------
# Renombrar las columnas
# --------------------------------------------

df = df.rename(columns={
    'leads_corte_mes3': 'Leads Marzo',
    'leads_corte_mes4': 'Leads Abril',
    'leads_si_corte_mes3': 'Cotizacion Marzo',
    'leads_si_corte_mes4': 'Cotizacion Abril',
    'facturado_corte_mes3': 'Facturacion Marzo',
    'facturado_corte_mes4': 'Facturacion Abril',
    'reservado_corte_mes3': 'Reservado Marzo',
    'reservado_corte_mes4': 'Reservado Abril'
})

# Columnas a mostrar con los nuevos nombres
cols = [
    'Leads Marzo', 'Leads Abril',
    'Cotizacion Marzo', 'Cotizacion Abril',
    'Facturacion Marzo', 'Facturacion Abril',
    'Reservado Marzo', 'Reservado Abril'
]

# Agrupar los datos
df_grouped = df.groupby(['sede', 'tienda', 'marca'])[cols].sum().reset_index()

# Crear columna jerárquica para tree structure (sin mostrarla en la tabla)
df_grouped['tree'] = df_grouped[['sede', 'tienda', 'marca']].agg(' / '.join, axis=1)

# --------------------------------------------
# Mostrar el reporte en Streamlit usando AgGrid
# --------------------------------------------

# Crear la configuración de AgGrid
gb = GridOptionsBuilder.from_dataframe(df_grouped)

# Configuración de la agrupación
gb.configure_default_column(groupable=True, enableRowGroup=True)

# Configuración de la agrupación jerárquica
gb.configure_grid_options(
    rowGroupPanelShow='always',  # Siempre mostrar el panel de grupo
    groupDefaultExpanded=0,  # Contraído por defecto
    autoGroupColumnDef={
        "headerName": "Sede / Tienda / Marca",
        "field": "tree",  # Usamos 'tree' para la agrupación
        "cellRendererParams": {
            "suppressCount": True  # No mostrar el conteo de filas
        }
    }
)

# Configuración de los grupos
gb.configure_column("sede", rowGroup=True, hide=True)  # Ocultar 'sede'
gb.configure_column("tienda", rowGroup=True, hide=True)  # Ocultar 'tienda'
gb.configure_column("marca", rowGroup=True, hide=True)  # Ocultar 'marca'

# Configurar las columnas de valores (leads, facturado, etc.) para que estén visibles siempre
for col in cols:
    gb.configure_column(col, hide=False, aggFunc='sum')  # Agregar función de agregación (suma) para columnas numéricas

# No mostrar la columna 'tree' en la tabla final
gb.configure_columns(["tree"], hide=True)

# Opciones finales para el grid
grid_options = gb.build()

# Mostrar con AgGrid
st.subheader("📊 Reporte Expandible por Sede, Tienda y Marca (estilo Excel +)")
AgGrid(
    df_grouped,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode="NO_UPDATE",
    fit_columns_on_grid_load=True,
    enable_grouping=True  # Habilitar agrupación
)

# Agregar un enlace de descarga para el CSV
st.download_button(
    label="Descargar CSV",
    data=df_grouped.to_csv(index=False, encoding="utf-8-sig"),
    file_name="PRUEBA3_PIVOTEADA.csv",
    mime="text/csv",
)
