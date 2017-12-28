from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys


# 重载函数，并定义信号，以便主程序处理
class MyLineEdit(QtWidgets.QLineEdit):
    inp_text_signal = QtCore.pyqtSignal(str)  # 定义信号

    def __init__(self, parent):
        super(MyLineEdit, self).__init__(parent)

    def mouseDoubleClickEvent(self, e):
        print('mouse double clicked')

    def mousePressEvent(self, e):
        print('mousePressEvent')

    def focusInEvent(self, e):
        print('focusInEvent')

    def focusOutEvent(self, e):
        self.inp_text_signal.emit("移出")  # 发送信号

    def moveEvent(self, e):
        print('moveEvent')

    def leaveEvent(self, e):  # 鼠标离开label
        print('leaveEvent')

    def enterEvent(self, e):  # 鼠标移入label
        print('enterEvent')

    def mouseMoveEvent(self, e):
        print('mouseMoveEvent')


class TestDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.statusLabel = MyLineEdit(self)
        self.statusLabel.setGeometry(QtCore.QRect(95, 220, 151, 41))
        self.statusLabel.setText("hello label")
        self.statusLabel.inp_text_signal.connect(self.sfocus)  # 绑定槽函数

    def sfocus(self, str):
        print(str)
        QMessageBox.warning(self,
                            "警告",
                            "用户名或密码错误！",
                            QMessageBox.No)
        self.close()


app = QtWidgets.QApplication(sys.argv)
dialog = TestDialog()
dialog.show()
sys.exit(app.exec_())