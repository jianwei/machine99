import functools


def cmpy(a, b):
    return b.get("centery")-a.get("centery")


def cmp_item_x(a, b):
    return b.get("centerx")-a.get("centerx")


class points ():
    def __init__(self):
        self.angle = 90  # 摄像头 90度视野
        self.line_diff = 20
        self.line_number = 1
        pass

    def format(self, data):
        return self.split_line(data)

    def split_line(self, data):
        data.sort(key=functools.cmp_to_key(cmpy))
        lineList = []
        for item in data:
            isAdded = False
            if (len(lineList) < 1):
                lineList.append([item])
                isAdded = True
            else:
                centerY = item.get("centery")
                for itemLine in lineList:
                    lineY = itemLine[0].get("centery")
                    if (float(lineY-self.line_diff) <= float(centerY) <= float(lineY+self.line_diff)):
                        itemLine.append(item)
                        isAdded = True
            if (not isAdded):
                lineList.append([item])
        sort_list = []
        for item in lineList:
            item.sort(key=functools.cmp_to_key(cmp_item_x))
            sort_list.append(item)
        return sort_list

    def get_turn_point_x(self, data):
        data = self.split_line(data)
        turn_data_list = data[:2]
        screenSize = turn_data_list[0][0].get("screenSize")
        center_pointer = screenSize[0]/2  # 640px中间
        # print("screenSize:",screenSize)
        for item in turn_data_list:
            length = len(item)
            center_0 = item[0].get("centerx")
            # print(item[0])
            # 只有1颗
            if length == 1:
                center_pointer = center_0
            else:
                center_end = item[length-1].get("centerx")
                print("center_0:{},center_end:{}".format(center_0,center_end))
                center_pointer = (center_0+center_end)/2
        return center_pointer

    def get_turn_point_y(self, data):
        data = self.split_line(data)
        max_y = 0
        first_line = data[0]
        for item2 in first_line:
            point = item2.get("point")
            y = point[2][1]
            max_y = y if  y>max_y else  max_y
        # print("max_y",max_y)
        return max_y
    
