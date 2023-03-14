from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QStackedLayout,
)
from PyQt5.QtGui import QPixmap, QPainter



class AviaHorizont(QWidget):
    """
    Класс авиагоризонта
    Используется для отображения виджета с тангажом и креном
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)
        self.cren = 0
        self.tang = 0

    #Импортируем изображения в pixmap
        self.scale_pixmap = QPixmap("image/scale.png")
        self.upper_pixmap = QPixmap("image/upper.png")
        self.under_pixmap = QPixmap("image/under.png")
        self.alpha_pixmap =QPixmap("image/alpha.png")
        self.reactangle = QRect(0, 0, 500, 500)

    #Создаем label в который помещается конечное изображение
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

    #Создаем начальный вид виджета
        res_pixmap = self.alpha_pixmap.copy()

        self.draw_widget(res_pixmap,self.upper_pixmap)
    

    #создаем layout в котором будет помещаться label c изображением
        mainlayout = QStackedLayout()
        mainlayout.addWidget(self.label)
        self.setLayout(mainlayout)

    #описываем методы класса
    def trans_form(self):
        """поворачивает горизонт и обновляет виджет"""
        alpha_pixmap = self.alpha_pixmap.copy()
        result_pixmap = self.alpha_pixmap.copy()
        upper_pixmap = self.upper_pixmap.copy() 
        
        painter_rotate = QPainter(alpha_pixmap)
        painter_rotate.translate(self.reactangle.center())
        painter_rotate.rotate(self.cren)
        painter_rotate.translate(-self.reactangle.center())
        painter_rotate.drawPixmap(0, 0, upper_pixmap)
        painter_rotate.end()
        
        self.draw_widget(result_pixmap,alpha_pixmap)

    def set_cren(self, cren):
        """обновляет значение переменной крена"""
        self.cren = cren
        self.trans_form()

    def set_tang(self, tang):
        """обновляет значение переменной тангажа"""
        self.tang = int(tang/2)
        self.trans_form()

    def draw_widget(self, result_pixmap, edited_upper_pixmap):
        """сбор картинок в одно целое"""
        painter = QPainter(result_pixmap)
        painter.drawPixmap(self.reactangle, self.under_pixmap, 
                           QRect(0, 500+self.tang, 500, 500))
        painter.drawPixmap(self.reactangle, edited_upper_pixmap, 
                           QRect(0, 0, 500, 500))
        painter.drawPixmap(self.reactangle, self.scale_pixmap, 
                           QRect(0, 0, 500, 500))
        painter.end()
        self.label.setPixmap(result_pixmap)

            