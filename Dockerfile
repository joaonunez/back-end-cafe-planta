# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo los archivos necesarios para la instalación de dependencias
COPY Pipfile Pipfile.lock /app/

# Instala pipenv y las dependencias del proyecto
RUN pip install --no-cache-dir pipenv && pipenv install --deploy --ignore-pipfile

# Copia el resto del código fuente
COPY . /app

# Exponer el puerto que utilizará la aplicación
EXPOSE $PORT

# Comando para ejecutar la aplicación utilizando Gunicorn
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
