cd service && python3 main.py --to_do run && python3 main.py --to_do work
cd detect && python3 detect.py --camera_id 20 --to_do run && python3 detect.py --camera_id 22 --to_do work

sudo chmod -R 777 /dev/ttyACM0

CPU 温度：
1.echo $[$(cat /sys/class/thermal/thermal_zone0/temp)/1000]°
2.apt-get install lm-sensors
    2.1 sensors

debian wifi:
vim /etc/network/interfaces

auto wlan0
iface wlan0 inet dhcp
wpa-essid Raspberry_PI_5G
wpa-psk tuniu890!


redis:
sudo apt update
sudo apt upgrade
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
systemctl status redis-server




brew install pyqt --build-from-source python@3.9


pip debug --verbose
# 切换活动的 Python 版本
sudo update-alternatives --config python3

sudo vim /usr/bin/gnome-terminal
line 1 :
#!/usr/bin/python3.10



