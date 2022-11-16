cd service && python3 main.py --to_do run && python3 main.py --to_do work
cd detect && python3 detect.py --camera_id 20 --to_do run && python3 detect.py --camera_id 22 --to_do work

sudo chmod -R 777 /dev/ttyACM0

CPU 温度：
1.echo $[$(cat /sys/class/thermal/thermal_zone0/temp)/1000]°
2.apt-get install lm-sensors
    2.1 sensors

pip3.9 install pyyaml -i   http://pypi.douban.com/simple --trusted-host pypi.douban.com


debian wifi:
vim /etc/network/interfaces

auto wlan0
iface wlan0 inet dhcp
wpa-essid Raspberry_PI_5G
wpa-psk tuniu890!
