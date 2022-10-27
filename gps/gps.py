"""
# Beidou/GPS data(NMEA 0813) parser example for Python 3
# This code can be used for parsing data received by the CodingCopper USB Beidou Receiver or other NMEA 0813 data.
# CodingCopper USB Beidou Receiver is designed for Raspberry Pi, PC/Laptop and Device(Linux or Android Based) receiving GNSS Data(Beidou, GPS and GLONASS).
# You can buy the CodingCopper USB Beidou Receiver from Taobao(https://item.taobao.com/item.htm?id=627807945245).
# Copyright (c) 2020, Ray Li(ray@CodingCopper.com)
# This code is licensed under the MIT License (MIT).
"""

# Change the deviceName to your Beidou device
# You can find the device using Linux Shell Command: ls /dev/ttyUSB*
import serial
import io
import time,json
deviceName = "/dev/tty.usbserial-1420"
# deviceName = "COM9"

def parseLatLng(s):
    # 3112.99824  -> 31 deg 12.99824 min
    # 12128.94944 -> 121 deg 28.94944 min
    t = s.split(".")
    i = int(t[0])
    deg = i//100
    min = float(("0."+t[1])) + i % 100
    return deg + min/60

from datetime import datetime, timedelta, timezone

def parseDatetime(d, h, m, s):
    utc_dt = datetime(2000+d[2], d[1], d[0], h, m, int(s), tzinfo=timezone.utc)
    return utc_dt.astimezone(timezone(timedelta(hours=8)))

class GGA(object):
    def __init__(self, segments):
        # eg: $GNGGA,145159.000,3112.99824,N,12128.94944,E,1,08,4.2,94.0,M,0.0,M,,*48
        #    $  0 | 1-UTCTime |2-Latitude|3|4-Longitude|5|6| 7| 8 | 9 |10|
        #    6-Fix Status: =0-invalid  >0-location is valid
        #    7-Satellites Used
        #    8-Horizontal Dilution of Precision
        #    9-Altitude
        #    11-Height Above Geoid
        self.data_ok = False
        try:
            # UTC Time
            self.utc_string = segments[1]
            if self.utc_string:
                self.hours = int(self.utc_string[0:2])
                self.minutes = int(self.utc_string[2:4])
                self.seconds = float(self.utc_string[4:])
            else:
                self.hours = 0
                self.minutes = 0
                self.seconds = 0.0
            # Satellites Used
            self.satellites_used = int(segments[7])
            # Fix Status
            self.fix_stat = int(segments[6])
            if self.fix_stat > 0:
                # location is valid
                try:
                    # Horizontal Dilution of Precision
                    self.hdop = float(segments[8])
                except (ValueError, IndexError):
                    self.hdop = 0.0
                # Longitude / Latitude
                try:
                    # Latitude
                    self.lat_string = segments[2]
                    self.lat_h = segments[3]
                    self.lat = parseLatLng(self.lat_string)
                    if self.lat_h.upper() == "S":
                        # N:North +, S:South -
                        self.lat = -self.lat
                    # Longitude
                    self.lng_string = segments[4]
                    self.lng_h = segments[5]
                    self.lng = parseLatLng(self.lng_string)
                    if self.lng_h.upper() == 'W':
                        # E:East +, W:West -
                        self.lng = -self.lng
                    self.latlng_ok = True
                except ValueError:
                    self.latlng_ok = False
                # Altitude / Height Above Geoid
                try:
                    self.altitude = float(segments[9])
                    self.geoid_height = float(segments[11])
                except ValueError:
                    self.altitude = 0.0
                    self.geoid_height = 0.0
                print("Longitude, Latitude, Altitude [%f, %f, %f]" % (
                    self.lng, self.lat, self.altitude))
            else:
                self.latlng_ok = False
            self.data_ok = True
        except (ValueError, IndexError):
            self.data_ok = False


class RMC(object):
    def __init__(self, segments):
        # eg: $GNRMC,145159.000,A,3112.99824,N,12128.94944,E,0.00,294.14,221020,,,A,V*0A
        #    $  0 | 1-UTCTime |2|3-Latitude|4|5-Longitude|6| 7 |   8   |  9  |
        #    2-Data Valid Flag: A-Valid, V-Invalid
        #    7-Speed in knot (1 knot = 1 mile/hour = 1.852 km/hour)
        #    8-Course: range[0-360), North=0, East=90, South=180, West=270
        #    9-Date String: Day / Month / Year(2 Digital)
        self.data_ok = False
        try:
            # UTC Time
            self.utc_string = segments[1]
            if self.utc_string:
                self.hours = int(self.utc_string[0:2])
                self.minutes = int(self.utc_string[2:4])
                self.seconds = float(self.utc_string[4:])
            else:
                self.hours = 0
                self.minutes = 0
                self.seconds = 0.0
            try:
                date_string = segments[9]
                if date_string:  # Possible date stamp found
                    day = int(date_string[0:2])
                    month = int(date_string[2:4])
                    year = int(date_string[4:6])
                    self.date = (day, month, year)
                else:  # No Date stamp yet
                    self.date = (0, 0, 0)
                self.datetime = parseDatetime(self.date, self.hours, self.minutes, self.seconds)
            except ValueError:  # Bad Date stamp value present
                self.datetime = None
            # Fix Status
            self.data_valid_flag = segments[2]
            if self.data_valid_flag == 'A':
                # location is valid
                # Longitude / Latitude
                try:
                    # Latitude
                    self.lat_string = segments[3]
                    self.lat_h = segments[4]
                    self.lat = parseLatLng(self.lat_string)
                    if self.lat_h.upper() == "S":
                        # N:North +, S:South -
                        self.lat = -self.lat
                    # Longitude
                    self.lng_string = segments[5]
                    self.lng_h = segments[6]
                    self.lng = parseLatLng(self.lng_string)
                    if self.lng_h.upper() == 'W':
                        # E:East +, W:West -
                        self.lng = -self.lng
                    self.latlng_ok = True
                except ValueError:
                    self.latlng_ok = False
                # Speed
                try:
                    self.spd_knt = float(segments[7])
                except ValueError:
                    self.spd_knt = 0.0
                self.speed = self.spd_knt * 1.852
                # Course
                try:
                    if segments[8]:
                        self.course = float(segments[8])
                    else:
                        self.course = 0.0
                except ValueError:
                    self.course = 0.0
                print("Longitude, Latitude, Speed(km/h), Course [%f, %f, %f, %f]" % (
                    self.lng, self.lat, self.speed, self.course))
                print("----------------------------------------------------------------------------------")
                print("speed:{}".format(self.speed))
                print("----------------------------------------------------------------------------------")
                if self.datetime:
                    print("Location Datetime: ", self.datetime)
            else:
                self.latlng_ok = False
            self.data_ok = True
        except (ValueError, IndexError):
            self.data_ok = False

def parse_gga(line):
    print(line, end='')
    segments = line.split(",")
    ggaData = GGA(segments)
    return ggaData


def parse_rmc(line):
    print(line, end='')
    segments = line.split(",")
    rmcData = RMC(segments)
    return rmcData

def print_obj(obj):
    maps = {}
    for item in obj.__dict__.items():
        if item[0] == "datetime":
            maps[item[0]] = item[1].timestamp()
        else:
            maps[item[0]] = item[1]
    fileName='../gps.txt'
    with open(fileName,'w')as file:
        file.write(json.dumps(maps))


def parse(line):
    c = line.split(",", 2)
    if c[0].endswith("GGA"):
        # print("parsing_GGA...")
        print_obj(parse_gga(line))
    if c[0].endswith("RMC"):
        # print("parsing_RMC...")
        print_obj(parse_rmc(line))


s = serial.Serial(deviceName, 9600, timeout=1.0)
# change baud to 115200
# change baud to 115200
s.write(b'$PCAS01,5*19\r\n')
# store settings
s.write(b'$PCAS00*01\r\n')

time.sleep(1)
# hot reset
s.write(b'$PCAS10,0*1C\r\n')
s.close()

# reOpen in baud 115200
s = serial.Serial(deviceName, 115200, timeout=1.0)

time.sleep(1)
s.flushInput()

sio = io.TextIOWrapper(io.BufferedRWPair(s, s))
while True:
    line = sio.readline()
    parse(line)
