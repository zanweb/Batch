from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tm import *



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # class MainWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # super(MainWindow, self).__init__()
        # self.MyCombo = QComboBox()Ui_MainWindowf
        self.setupUi(self)
        # self.filter = Filter()
        # self.pushButton.enterEvent(QtWidgets.QMouseEventTransition).connect(self.do_enter)
        self.pushButton.setMouseTracking(True)
        self.pushButton = MyPushbutton(self.centralwidget)
        self.pushButton.setGeometry(QRect(400, 100, 93, 100))
        # self.pushButton.mouseMoveEvent(QtCore.QEvent.MouseMove).connect(self.do_focus)
        # self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        # self.connect(self.pushButton, SIGNAL("clicked()"), self.do_enter)
        self.pushButton1 = MyPushbutton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(100, 100, 93, 100))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2 = MyPushbutton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(200, 100, 93, 100))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton3 = MyPushbutton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(300, 100, 93, 100))
        self.pushButton3.setObjectName("pushButton3")



    def do_enter(self):
        print('Enter')

    # def do_focus(self, event):
    #     if event == QtCore.QEvent.FocusIn:
    #         print('FocusIn')
    #     if event == QtCore.QEvent.FocusOut:
    #         print('FocusOut')
    #     if event == QtCore.QEvent.MouseMove:
    #         print('MouseMove')

    # def focusInEvent(self, QMouseEvent):
    #     if Qt.LeftButton:
    #         print('I am focus！')
    #         QMouseEvent.accept()

    # def mouseReleaseEvent(self, QMouseEvent):
    #     # self.m_drag = False
    #     self.setCursor(QCursor(Qt.ArrowCursor))
    #
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.m_drag = True
    #         self.m_DragPosition = event.globalPos() - self.pos()
    #         event.accept()
    #         self.setCursor(QCursor(Qt.OpenHandCursor))
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     # print('Mouse Move')
    #     if Qt.RightButton:
    #         print('I am left button')
    #         QMouseEvent.accept()
    #     elif Qt.LeftButton:
    #         print('I am right Button')
    #         QMouseEvent.accept()
    #
    # def leaveEvent(self, e):  # 鼠标离开label
    #     print('leaveEvent')
    #
    # def enterEvent(self, e):  # 鼠标移入label
    #     print('enterEvent')
# class Filter(QtWidgets):
#     msg = QtCore.pyqtSignal(int)


# class QPushButton(QtWidgets.QPushButton):
class QPushButton(QtWidgets.QPushButton):
    inp_text_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        # super().__init__()

        super(QPushButton, self).__init__()

    def leaveEvent(self, event):  # 鼠标离开label
        print('button leaveEvent')

    def enterEvent(self, event):  # 鼠标移入label
        print('button enterEvent')
        # QPushButton.enterEvent(self, event)
        self.setStyleSheet("background-color:red;")
        self.setSizePolicy()
        # self.size(self.sizeHint())
        self.resize((200, 30))
        self.repaint()
        self.update()
        return QtWidgets.QPushButton.enterEvent()


class MyPushbutton(QtWidgets.QPushButton):
    inp_text_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super(MyPushbutton, self).__init__(parent)

    def focusInEvent(self, QFocusEvent):
        self.setStyleSheet("background-color:green;")
        print('Focus in')

    def focusOutEvent(self, QFocusEvent):
        print('Focus out')

    def mouseMoveEvent(self, *args, **kwargs):
        print('Mouse move')

    def leaveEvent(self, e):  # 鼠标离开label
        self.setStyleSheet("background-color:lightgray;")
        # self.resize(self.sizeHint())
        self.resize(QSize(93, 100))
        print('leaveEvent')

    def enterEvent(self, e):  # 鼠标移入label
        try:
            self.setStyleSheet("background-color:blue;")
            self.resize(QSize(100, 106))
            print('enterEvent')
        except Exception as ev:
            print(ev)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_show = MainWindow()
    main_show.show()

    sys.exit(app.exec_())