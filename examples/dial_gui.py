from dynamikontrol import Module
from PyQt5.QtWidgets import *
import sys

class Dial(QWidget):
    def __init__(self, module):
        QWidget.__init__(self)
        self.module = module

        self.dial = QDial()
        self.dial.setRange(-150, 150)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.dialMoved)

        layout = QGridLayout()
        layout.addWidget(self.dial)
        self.setLayout(layout)

        self.setGeometry(500, 500, 500, 500)

    def dialMoved(self):
        self.module.motor.angle(self.dial.value())
        print(f'Dial value {self.dial.value()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = Dial(Module())
    screen.show()

    sys.exit(app.exec_())
