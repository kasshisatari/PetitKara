cd /home/pi/Desktop/PetitKara
python Controller.py >> stdout.log 2>> stderr.log &
chromium-browser http://localhost:8080/console &
