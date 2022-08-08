FROM python:3-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

## falta instalar node16
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install nodejs npm -y
RUN npm install

COPY . .

CMD [ "python", "./API/main.py" ]
