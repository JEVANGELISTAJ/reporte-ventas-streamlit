import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# --------------------------------------------
# Cargar el CSV desde la ruta local del proyecto
# --------------------------------------------

csv_path = 'PRUEBA3_PIVOTEADA.csv'

# Leer el CSV
df = pd.read_csv(csv_path)

# Limpiar espacios y convertir a minúsculas en los nombres de las columnas
df.columns = df.columns.str.strip().str.lower()

# Validar que existan las columnas esperadas
expected_cols = [
    'leads_corte_mes3', 'leads_corte_mes4',
    'leads_si_corte_mes3', 'leads_si_corte_mes4',
    'facturado_corte_mes3', 'facturado_corte_mes4',
    'reservado_corte_mes3', 'reservado_corte_mes4'
]

missing = [col for col in expected_cols if col not in df.columns]
if missing:
    st.error(f"Columnas faltantes en el CSV: {', '.join(missing)}")
    st.stop()

# Renombrar columnas para mostrar
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

cols = [
    'Leads Marzo', 'Leads Abril',
    'Cotizacion Marzo', 'Cotizacion Abril',
    'Facturacion Marzo', 'Facturacion Abril',
    'Reservado Marzo', 'Reservado Abril'
]

# Agrupar los datos
df_grouped = df.groupby(['sede', 'tienda', 'marca'])[cols].sum().reset_index()

# --------------------------------------------
# Mostrar el reporte en Streamlit usando AgGrid
# --------------------------------------------

gb = GridOptionsBuilder.from_dataframe(df_grouped)
gb.configure_default_column(groupable=True, enableRowGroup=True)
gb.configure_grid_options(rowGroupPanelShow='always', groupDefaultExpanded=0)
grid_options = gb.build()

st.markdown("### 📊 Reporte Expandible por Sede, Tienda y Marca")

AgGrid(
    df_grouped,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode="NO_UPDATE",
    fit_columns_on_grid_load=True
)

# Botón de descarga
st.download_button(
    label="📥 Descargar CSV Agrupado",
    data=df_grouped.to_csv(index=False, encoding="utf-8-sig"),
    file_name="PRUEBA3_PIVOTEADA.csv",
    mime="text/csv",
)
