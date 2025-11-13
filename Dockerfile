# Python base image ligera
FROM python:3.11-slim

# Crear directorio de la app
WORKDIR /app

# Copiar dependencias y luego instalar (mejor cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /app

# Exponer puerto de la app
EXPOSE 8000

# Comando por defecto (Flask dev server en contenedor)
CMD ["python", "app.py"]