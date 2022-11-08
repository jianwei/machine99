cd service && python3 main.py --to_do run && python3 main.py --to_do work
cd detect && python3 detect.py --camera_id 20 --to_do run && python3 detect.py --camera_id 22 --to_do work


ubuntu nomachine:
sudo systemctl stop gdm3
sudo /etc/NX/nxserver --restart


virtualenv -p /usr/bin/python3 venv
source venv/bin/activate


CPU 温度：
1.echo $[$(cat /sys/class/thermal/thermal_zone0/temp)/1000]°
2.apt-get install lm-sensors
    2.1 sensors