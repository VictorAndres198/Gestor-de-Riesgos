FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo el contenido del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 5000

# Comando por defecto
CMD ["python", "matriz_riesgos.py"]
