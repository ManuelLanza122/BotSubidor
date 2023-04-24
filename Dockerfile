# Selecciona la imagen base de Python
FROM python:3.8-slim-buster

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios a /app
COPY requirements.txt .
COPY main.py .
COPY .env .

# Instala los paquetes necesarios
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el bot
CMD ["python", "main.py"]
