import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# --------------------------------------------
# Cargar el CSV desde GitHub
# --------------------------------------------
url_csv = "https://raw.githubusercontent.com/JEVANGELISTAJ/reporte-ventas-streamlit/refs/heads/main/PRUEBA3_PIVOTEADA.csv"
df = pd.read_csv(url_csv)

# Limpiar espacios y convertir a minúsculas en los nombres de las columnas
df.columns = df.columns.str.strip().str.lower()

# Reemplazar valores NaN por None en todo el DataFrame
df = df.where(pd.notnull(df), None)

# --------------------------------------------
# Mostrar datos en Streamlit usando AgGrid
# --------------------------------------------

# Renombrar las columnas como en tu código anterior
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

# Agrupar los datos como en tu código original
df_grouped = df.groupby(['sede', 'tienda', 'marca'])[cols].sum().reset_index()

# Crear columna jerárquica para tree structure (sin mostrarla en la tabla)
df_grouped['tree'] = df_grouped[['sede', 'tienda', 'marca']].agg(' / '.join, axis=1)

# Crear grid con agrupación en modo jerárquico
gb = GridOptionsBuilder.from_dataframe(df_grouped)

# Configurar agrupación jerárquica para la tabla sin la fila concatenada
gb.configure_default_column(groupable=True, enableRowGroup=True)

# Configuración de agrupación jerárquica
gb.configure_grid_options(
    rowGroupPanelShow='always',  # Siempre mostrar el panel de grupo
    groupDefaultExpanded=0,  # Contraído por defecto
    autoGroupColumnDef={
        "headerName": "Sede / Tienda / Marca",
        "field": "tree",  # Mantener el campo para la agrupación interna
        "cellRendererParams": {
            "suppressCount": True  # No mostrar el conteo de filas
        }
    }
)

# Configurar las columnas de agrupación, pero ocultarlas para la vista final
gb.configure_column("sede", rowGroup=True, hide=True)  # Ocultar 'sede'
gb.configure_column("tienda", rowGroup=True, hide=True)  # Ocultar 'tienda'
gb.configure_column("marca", rowGroup=True, hide=True)  # Ocultar 'marca'

# Configurar las columnas de valores (leads, facturado, etc.) para que estén visibles siempre
for col in cols:
    gb.configure_column(col, hide=False, aggFunc='sum')  # Agregar función de agregación (suma) para columnas numéricas

# No mostrar la columna 'tree' en la tabla final, solo para la agrupación
gb.configure_columns(["tree"], hide=True)

grid_options = gb.build()

# Mostrar con AgGrid
st.subheader("📊 Reporte Expandible por Sede, Tienda y Marca (estilo Excel +)")
AgGrid(
    df_grouped,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode="NO_UPDATE",
    fit_columns_on_grid_load=True
)
