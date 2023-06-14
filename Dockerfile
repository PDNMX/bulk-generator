FROM nikolaik/python-nodejs:python3.10-nodejs16-slim

USER root
WORKDIR /home/pn/bulk/API

ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD . ./
RUN yarn install

WORKDIR /home/pn/bulk/API
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install cron
RUN apt-get update && apt-get -y install cron

COPY ./cronfile /etc/cron.d/cronfile
RUN chmod 0644 /etc/cron.d/cronfile
RUN crontab /etc/cron.d/cronfile
#RUN crontab -l | { cat; echo "* * * * * root /usr/bin/python /home/pn/bulk/API/actualizacion.py >> /home/pn/bulk/API/out.actualizacion.log 2>&1"; } | crontab -
#RUN cron
CMD [ "cron", "-f"]
