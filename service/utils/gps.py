import json

class gps():
    def __init__(self,file_path):
        self.gps_file = file_path
    
    def get_gps_data(self):
        file_object = open(self.gps_file,'r')
        try:
            all_the_text = file_object.read()
            if all_the_text:
                return json.loads(all_the_text)
            else:
                return {}
        finally:
            file_object.close()

