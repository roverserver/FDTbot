FROM python:3.10
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install app
WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt


# setup cron

RUN apt-get update && apt-get install -y cron
COPY example-crontab /etc/cron.d/fdt-send
RUN chmod 0644 /etc/cron.d/fdt-send && crontab /etc/cron.d/fdt-send

VOLUME /app/data

ENTRYPOINT ["bash", "init.sh"]
