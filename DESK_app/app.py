import sys
from PyQt5.QtWidgets import (QApplication, QWidget, 
                             QPushButton, QSlider, 
                             QMainWindow, QVBoxLayout,
                             QHBoxLayout,)
from PyQt5.QtCore import Qt

from widgets import AviaHorizont, InfoBlock


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        
        horiz = AviaHorizont()
        block = InfoBlock()
        #элементы для теста##################################
        self.sld_cren = QSlider(Qt.Horizontal, self)
        self.sld_cren.setValue(0)
        self.sld_cren.setPageStep(1)                     
        self.sld_cren.setTickInterval(5)                      
        self.sld_cren.setRange(-360, 360)        
        self.sld_cren.setFocusPolicy(Qt.StrongFocus)
        self.sld_cren.setTickPosition(QSlider.TicksBothSides) 
        self.sld_cren.setSingleStep(1)        
        self.sld_cren.valueChanged[int].connect(horiz.set_cren)

        self.sld_tang = QSlider(Qt.Horizontal, self)
        self.sld_tang.setValue(0)
        self.sld_tang.setPageStep(1)                     
        self.sld_tang.setTickInterval(5)                      
        self.sld_tang.setRange(-360, 360)        
        self.sld_tang.setFocusPolicy(Qt.StrongFocus)
        self.sld_tang.setTickPosition(QSlider.TicksBothSides) 
        self.sld_tang.setSingleStep(1)        
        self.sld_tang.valueChanged[int].connect(horiz.set_tang)

        list1 = ['123123' for c in range(12)]
        list2 = ['dgegregtre' for c in range(12)]

        button1 = QPushButton('Button 1 manual')
        button2 = QPushButton('Button 2 manual')
        
        button1.clicked.connect(lambda x: block.update_value(list1))
        button2.clicked.connect(lambda x: block.update_value(list2))
        #####################################################

        hbox = QHBoxLayout()
        hbox.addStretch(0) 
        hbox.addWidget(horiz, alignment=Qt.AlignCenter)
        hbox.addWidget(block)
        hbox.addStretch(0) 

        vbox = QVBoxLayout()
        vbox.addWidget(self.sld_cren)
        vbox.addWidget(self.sld_tang)
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addLayout(hbox)
        
        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)

    def sld_update(self, value):
        self.sld.setValue(value)
        
        

app = QApplication(sys.argv)

window = MyWindow()
window.setFixedSize(1920,1080)
window.move(0, 0)
window.setWindowTitle('drone_info')
window.show()

sys.exit(app.exec_())