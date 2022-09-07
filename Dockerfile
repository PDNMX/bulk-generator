FROM nikolaik/python-nodejs:python3.10-nodejs16-slim

USER root
WORKDIR /home/pn/bulk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN yarn install

WORKDIR /home/pn/bulk/API

CMD [ "python", "main.py" ]
