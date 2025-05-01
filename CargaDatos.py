import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from google.cloud import storage
import tempfile
import csv
import io

#Función de carga de los datos al bucket
def upload_to_gcs(file_obj, destination_blob_name, bucket_name="etl_ventas_bucket"):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_obj.getbuffer())
            tmp.flush()
            blob.upload_from_filename(tmp.name)

        return True, f"Archivo subido a gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        return False, str(e)

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
logo = Image.open('Images/Screenshot 2025-04-28 152319.png')  # Ajusta la ruta si es necesario
st.image(logo, use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #003366;'>Bienvenido al Portal de Carga de Datos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #003366;'>Por favor sube tu archivo CSV continuar.</p>", unsafe_allow_html=True)

# Separador
st.markdown("---")

# Subida de archivo
uploaded_file = st.file_uploader("Selecciona tu archivo csv, recuerda que debes cargar el archivo con MÍNIMO 5 años.", type=["csv"])

if uploaded_file is not None:
    st.success("✅ Archivo cargado exitosamente. ¡Pronto lo enviaremos a GCP!")
    # Aquí más adelante agregaríamos la lógica para cargar a GCP
    df = None
    try:

        # Detectar delimitador automáticamente
        sample = uploaded_file.read(2048).decode("utf-8")
        uploaded_file.seek(0)  # volver al inicio del archivo
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        uploaded_file.seek(0)

        # Leer CSV con delimitador detectado
        df = pd.read_csv(uploaded_file, delimiter=dialect.delimiter)

        st.dataframe(df.head())  # Mostrar una vista previa del archivo
        if df.shape[1] > (12*3*5):   # 12 meses, 3 años, 5 años mínimo
            st.success("✅ El archivo contiene datos válidos.")
            blob_name = uploaded_file.name
            with st.spinner("Subiendo archivo a Google Cloud Storage..."):
                success, msg = upload_to_gcs(uploaded_file, blob_name)
                if success:
                    st.success("☁️ " + msg)
                else:
                    st.error("❌ Error al subir el archivo: " + msg)

        else:
            st.error("❌ El archivo no contiene la cantidad de años suficientes.")
    except Exception as e:
        st.error(f"❌ Error leyendo el archivo: {e}")


# Pie de página
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px;'>Celebramos 14 años llevando frescura a tu vida. 🦜</p>", unsafe_allow_html=True)

