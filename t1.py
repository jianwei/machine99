import math

def main(data):
    centerx = int(data[0].get("screenSize")[0]/2)
    print("centerx:",centerx)
    for item in data:
        center = item.get("center")
        print(center)



if __name__ == '__main__':
    data =[{"point":[[292,162],[323,162],[292,188],[323,188]],"name":"corn","time":1669181435.16307,"center":[307.5,175.0],"centerx":307.5,"centery":175.0,"screenSize":[640,480]},{"point":[[132,159],[163,159],[132,186],[163,186]],"name":"corn","time":1669181435.1622827,"center":[147.5,172.5],"centerx":147.5,"centery":172.5,"screenSize":[640,480]},{"point":[[523,154],[557,154],[523,182],[557,182]],"name":"corn","time":1669181435.162673,"center":[540.0,168.0],"centerx":540.0,"centery":168.0,"screenSize":[640,480]},{"point":[[147,106],[176,106],[147,129],[176,129]],"name":"corn","time":1669181435.1629987,"center":[161.5,117.5],"centerx":161.5,"centery":117.5,"screenSize":[640,480]},{"point":[[299,102],[329,102],[299,124],[329,124]],"name":"corn","time":1669181435.1629217,"center":[314.0,113.0],"centerx":314.0,"centery":113.0,"screenSize":[640,480]},{"point":[[500,96],[528,96],[500,120],[528,120]],"name":"corn","time":1669181435.1625562,"center":[514.0,108.0],"centerx":514.0,"centery":108.0,"screenSize":[640,480]}]





    main(data)


