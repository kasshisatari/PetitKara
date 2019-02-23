sudo rm -fr /home/pi/.config/chromium/Singleton*
cd /home/pi/Desktop/PetitKara
sudo sh updateSSID.sh
python Controller.py >> stdout.log 2>> stderr.log &
