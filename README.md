# FDTbot

Bot um die Frage des Tages automatisiert zu veröffentlichen

## installation

```bash
git clone https://github.com/roverserver/FDTbot.git
cd FDTbot
cp example.env .env
cp example.send.sh send.sh
chmod +x send.sh
touch fdt.txt
touch archiv.txt
```

- edit .env
- set current directory in send.sh
- create cron job for send.sh

start bot to add questions from discord with `python3 edit.py`
