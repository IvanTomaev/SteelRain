from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
)


class InfoBlock(QWidget):
    """Виджет для вывода телеметрии"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,500)
        self.setStyleSheet('''border: 2px solid black;''')


        self.name_tags = list() #list with id labels
        self.value = ['**' for c in range(12)] #значения телеметрии
        
        #layout
        grid = QGridLayout()
        self.setLayout(grid)
        #список параметров и их позиции
        self.names = ['Altitude (m)','Battery (%)',
                    'Voltage (V)','Current (A)',
                    'Climb (m/s)','Speed (m/s)',
                    'Distance (m)','Time (s)',
                    'Roll (°)','Pitch (°)',
                    'Yaw (°)', 'temp (°C)']
        positions = [(i,j) for i in range(6) for j in range(2)]

        #создание лейблов, запись их id и расстановка по сетке
        for position, name in zip(positions, self.names):

            label = QLabel(name)
            label_value = QLabel()
            self.name_tags.append(label_value)

            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(label_value)
            grid.addLayout(vbox,  *position)
            grid.rowStretch(0)

        self.update_label()

    def update_value(self, income_list):
        """обновление значения телеметрии"""
        self.value = income_list
        self.update_label()

    def update_label(self):
        """обновление вывода телеметрии"""
        for i in range(12):
            self.name_tags[i].setText(self.value[i])



