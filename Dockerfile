# Usar imagen base oficial de Streamlit
FROM python:3.10-slim

# Instalar dependencias necesarias
RUN pip install --no-cache-dir streamlit pandas pillow google-cloud-storage

# Crear directorio para la app
WORKDIR /app

# Copiar todos los archivos de la app al contenedor
COPY . /app

# Exponer el puerto en el que corre Streamlit
EXPOSE 8501

# Comando para iniciar Streamlit
CMD ["streamlit", "run", "CargaDatos.py", "--server.port=8501", "--server.enableCORS=false"]
