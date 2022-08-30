#!/bin/sh
# clone repo
echo "Cloning repo"
git clone https://github.com/roverserver/FDTbot.git && cd FDTbot

#copy config file
cp example.env .env

# create "database"
mkdir data
touch data/fdt.txt
touch data/archiv.txt
touch data/geloescht.txt

touch data/times_no_fdt.txt
touch data/wiederholt.txt

echo "creating send.sh"
# create send.sh - see example.send.sh for Reference
echo "#!/bin/sh\ncd " > send.sh
pwd >> send.sh
echo " && python3 send.py >> data/log.txt" >> send.sh
chmod +x send.sh

echo "getting dependencies"
# install python dependencies
pip3 install -r requirements.txt

echo "done"