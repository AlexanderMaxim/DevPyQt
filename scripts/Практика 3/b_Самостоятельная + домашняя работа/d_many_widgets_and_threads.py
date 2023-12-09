"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from PySide6 import QtWidgets

import b_systeminfo_widget
import c_weatherapi_widget

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        self.sysInfo = b_systeminfo_widget.CpuRamLoadInfo(self)
        self.weatherInfo = c_weatherapi_widget.WeatherInfo(self)

        vSpacer1 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        vSpacer2 = QtWidgets.QSpacerItem(0, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        l_sysInfo = QtWidgets.QVBoxLayout()
        l_sysInfo.addItem(vSpacer1)
        l_sysInfo.addWidget(self.sysInfo)
        l_sysInfo.addItem(vSpacer2)

        l = QtWidgets.QHBoxLayout()
        l.addWidget(self.weatherInfo)
        l.addLayout(l_sysInfo)

        self.setLayout(l)

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
