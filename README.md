# FDTbot

Bot um die Frage des Tages automatisiert zu veröffentlichen

## Docker

copy the docker-compose.yml file and set the environment variables with your values an then run
```sh
docker-compose up -d
```
if you want to use a custom cron job timer you will need to compile the docker image yourself (after editing the example-crontab file)

## manual Installation

```sh
git clone https://github.com/roverserver/FDTbot.git && cd FDTbot
pip3 install -r requirements.txt
cp example.env .env
```

- edit .env (e.g. `nano .env`)
- create cron job (e.g. with `crontab -e`) for send.py (e.g. `0 8 * * * ~//FDTbot/send.py ~/FDTbot/data/ 2>&1 >> ~/FDTbot/data/log.txt` to send the question every day at 8:00)

start bot to add questions from discord with `python3 edit.py`
