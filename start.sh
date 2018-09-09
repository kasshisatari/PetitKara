sudo rm -fr /home/pi/.config/chromium/Singleton*
cd /home/pi/Desktop/PetitKara
python Controller.py >> stdout.log 2>> stderr.log &
chromium-browser --noerrdialogs --kiosk --incognito http://localhost:8080/console &
