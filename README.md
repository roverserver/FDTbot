# FDTbot

Bot um die Frage des Tages automatisiert zu veröffentlichen

## Linux Installation

```sh
git clone https://github.com/roverserver/FDTbot.git && cd FDTbot
pip3 install -r requirements.txt
cp example.env .env
```

- edit .env (e.g. `nano .env`)
- create cron job (e.g. with `crontab -e`) for send.py (e.g. `8 0 * * * ~//FDTbot/send.py ~/FDTbot/data/ 2>&1 >> ~/FDTbot/data/log.txt` to send the question every day at 8:00)

start bot to add questions from discord with `python3 edit.py`
