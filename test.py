import json

# b = {"c":1}
bb = b'[{"point": [[200, 182], [291, 182], [200, 240], [291, 240]], "name": "box", "time": 1667272063.4156375, "center": [245.5, 211.0], "centerx": 245.5, "centery": 211.0, "screenSize": [640, 480]}, {"point": [[84, 242], [164, 242], [84, 327], [164, 327]], "name": "box", "time": 1667272063.4161322, "center": [124.0, 284.5], "centerx": 124.0, "centery": 284.5, "screenSize": [640, 480]}, {"point": [[105, 176], [192, 176], [105, 245], [192, 245]], "name": "box", "time": 1667272063.4165049, "center": [148.5, 210.5], "centerx": 148.5, "centery": 210.5, "screenSize": [640, 480]}, {"point": [[178, 267], [267, 267], [178, 340], [267, 340]], "name": "box", "time": 1667272063.4168823, "center": [222.5, 303.5], "centerx": 222.5, "centery": 303.5, "screenSize": [640, 480]}, {"point": [[301, 213], [373, 213], [301, 285], [373, 285]], "name": "box", "time": 1667272063.4172862, "center": [337.0, 249.0], "centerx": 337.0, "centery": 249.0, "screenSize": [640, 480]}, {"point": [[338, 180], [418, 180], [338, 230], [418, 230]], "name": "box", "time": 1667272063.417679, "center": [378.0, 205.0], "centerx": 378.0, "centery": 205.0, "screenSize": [640, 480]}]'
# d = json.dumps(b)
# c=str(b)
# c = json.loads(d)
cc = json.loads(bb)

# print(d,type(d),c,type(c))
print(type(bb),cc)

 