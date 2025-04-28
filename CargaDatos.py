import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

# Configurar página
st.set_page_config(
    page_title="Carga de Datos - Celebración 14 años",
    page_icon="🎉",
    layout="centered"
)

# Aplicar fondo personalizado con CSS
page_bg_img = '''
<style>
.stApp {
    background-color: #7AC0CD;  /* Color corporativo azul claro */
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Mostrar el logo
logo = Image.open('Images\Screenshot 2025-04-28 152319.png')  # Ajusta la ruta si es necesario
st.image(logo, use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #003366;'>Bienvenido al Portal de Carga de Datos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #003366;'>Por favor sube tu archivo de Excel para continuar.</p>", unsafe_allow_html=True)

# Separador
st.markdown("---")

# Subida de archivo
uploaded_file = st.file_uploader("Selecciona tu archivo .XLSX, recuerda que debes cargar el archivo con MÍNIMO 5 años.", type=["xlsx"])

if uploaded_file is not None:
    st.success("✅ Archivo cargado exitosamente. ¡Pronto lo enviaremos a GCP!")
    # Aquí más adelante agregaríamos la lógica para cargar a GCP
    df = None
    try:
        
        df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())  # Mostrar una vista previa del archivo
        if df.shape[1] > (12*3*5):   # 12 meses, 3 años, 5 años mínimo
            st.success("✅ El archivo contiene datos válidos.")
        else:
            st.error("❌ El archivo no contiene la cantidad de años suficientes.")
    except Exception as e:
        st.error(f"❌ Error leyendo el archivo: {e}")

# Pie de página
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px;'>Celebramos 14 años llevando frescura a tu vida. 🦜</p>", unsafe_allow_html=True)