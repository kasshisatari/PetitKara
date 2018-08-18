cd /home/pi/Desktop/PetitKara
python Controller.py >> stdout.log 2>> stderr.log &
chromium-browser --start-maximized http://localhost:8080/console &
