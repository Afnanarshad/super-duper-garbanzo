FROM python:3.10.9-slim-buster

WORKDIR /app

#added for app server
EXPOSE 8000

ADD /src/requirements.txt .
ADD /src/repository.py .
ADD /src/main.py .
# Uncomment the following line to use a local copy of the .env file
# ADD .env .

RUN apt-get update -y && apt-get install -y curl gnupg g++ unixodbc-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list 

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install --upgrade -r requirements.txt

# For running the container locally 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "360", "--log-level", "debug", "--bind", "0.0.0.0:8000"]
#this worked! with azure web app