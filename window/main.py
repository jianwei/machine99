import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from Ui_machine import Ui_MainWindow  #导入你写的界面类
import yaml

 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,config_yaml,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.data = self.get_yaml_data(config_yaml)
        self.set_defautl_value(self.data)
        self.pushButton.clicked.connect(self.save)

    def save(self):
        position_val = self.comboBox.currentText()
        position_val =1 if position_val=="左边" else 2
        self.data["other"]['position'] = position_val
        distaice_long = self.lineEdit.text()
        self.data["other"]['distaice_long'] = distaice_long
        with open('../config.yaml', 'w') as f:
            yaml.dump(self.data, f)
        
    

    def set_defautl_value(self,data):
        #左右默认值
        position  =  data.get("other").get("position")
        items = ["左边", "右边"]
        self.comboBox.addItems(items)
        position_val =1 if int(position) ==1 else 2
        self.comboBox.setCurrentIndex(position_val-1)
        #陇间距
        distaice_long  =  data.get("other").get("distaice_long")
        self.lineEdit.setText(str(distaice_long))

    
    def get_yaml_data(self,config_yaml):
        with open(config_yaml, encoding='utf-8') as file:
            content = file.read()
            data = yaml.load(content, Loader=yaml.FullLoader)
            return data
        
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow("../config.yaml")
    myWin.show()
    sys.exit(app.exec_())    