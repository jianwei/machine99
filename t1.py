def main(data):
    points = []
    for line in data:
        for item in line:
            points.append(float(item.get("centerx")))
    get_px_diff(points)


def get_px_diff(points):
    print(points)
    length = len(points)
    diff_points = []
    for i in range(length):
        item = points[i]
        print(item)
        if (i != (length-1)) : 
            diff_points.append(abs(points[i+1]-points[i]))
    print(diff_points)
    pass




if __name__ == '__main__':
    data =[[{"point":[[518,153],[536,153],[518,169],[536,169]],"name":"corn","time":1669086705.1543727,"center":[527.0,161.0],"centerx":527.0,"centery":161.0,"screenSize":[640,480]},{"point":[[384,155],[402,155],[384,171],[402,171]],"name":"corn","time":1669086705.1492438,"center":[393.0,163.0],"centerx":393.0,"centery":163.0,"screenSize":[640,480]},{"point":[[293,159],[315,159],[293,175],[315,175]],"name":"corn","time":1669086705.1488655,"center":[304.0,167.0],"centerx":304.0,"centery":167.0,"screenSize":[640,480]},{"point":[[203,160],[225,160],[203,177],[225,177]],"name":"corn","time":1669086705.148215,"center":[214.0,168.5],"centerx":214.0,"centery":168.5,"screenSize":[640,480]},{"point":[[59,161],[87,161],[59,183],[87,183]],"name":"corn","time":1669086705.1540048,"center":[73.0,172.0],"centerx":73.0,"centery":172.0,"screenSize":[640,480]}]]
    main(data)