"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

import time

from PySide6 import QtWidgets, QtGui

from a_threads import WeatherHandler


class WeatherInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.weatherTread = WeatherHandler(0, 0)

        self.initUi()
        self.initSignals()

    def initUi(self):
        self.lineEditLat = QtWidgets.QLineEdit()
        self.lineEditLat.setPlaceholderText('Широта (latitude)')
        self.lineEditLat.setValidator(QtGui.QRegularExpressionValidator('[-]?([1-8]?\d(\.\d+)?|90(\.0+)?)'))

        self.lineEditLon = QtWidgets.QLineEdit()
        self.lineEditLon.setPlaceholderText('Долгота (longitude)')
        self.lineEditLon.setValidator(QtGui.QRegularExpressionValidator('[-]?(((1[0-7]\d)|[1-9]?\d)(\.\d+)?|180(\.0+)?)'))

        labelDelay = QtWidgets.QLabel('Задержка обновления, с:')
        self.spinBoxDelay = QtWidgets.QSpinBox()
        self.spinBoxDelay.setMinimum(2)

        l_delay = QtWidgets.QHBoxLayout()
        l_delay.addWidget(labelDelay)
        l_delay.addWidget(self.spinBoxDelay)

        self.pushButtonGetData = QtWidgets.QPushButton('Получение \nданных')
        self.pushButtonGetData.setFixedSize(100, 100)

        hSpacer = QtWidgets.QSpacerItem(0, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.plainTextEditWeatherInfo = QtWidgets.QPlainTextEdit()

        l_gr = QtWidgets.QVBoxLayout()
        l_gr.addWidget(self.lineEditLat)
        l_gr.addWidget(self.lineEditLon)
        l_gr.addLayout(l_delay)

        gr = QtWidgets.QGroupBox()
        gr.setLayout(l_gr)
        gr.setFixedSize(210, 100)

        l_settings = QtWidgets.QHBoxLayout()
        l_settings.addWidget(gr)
        l_settings.addWidget(self.pushButtonGetData)
        l_settings.addItem(hSpacer)

        l = QtWidgets.QVBoxLayout()
        l.addLayout(l_settings)
        l.addWidget(self.plainTextEditWeatherInfo)

        self.setLayout(l)

    def initSignals(self):
        self.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)
        self.weatherTread.weatherInfoRecieved.connect(lambda data:
            self.plainTextEditWeatherInfo.appendPlainText(f'--- {time.ctime()} | '
                                                          f'{data["latitude"]}°, {data["longitude"]}° ---'
                  f'\n-Температура: {data["current_weather"]["temperature"]}'
                  f'\n-Скорость ветра: {data["current_weather"]["windspeed"]}'
                  f'\n-Направление ветра: {data["current_weather"]["winddirection"]}\n')
        )
        self.spinBoxDelay.valueChanged.connect(self.weatherTread.setDelay)
        self.lineEditLat.textChanged.connect(lambda data: self.weatherTread.setLat(data))
        self.lineEditLon.textChanged.connect(lambda data: self.weatherTread.setLon(data))

    def onPushButtonGetDataClicked(self):
        if self.weatherTread.getStatus():
            self.weatherTread.setStatus(False)

            self.lineEditLat.setEnabled(True)
            self.lineEditLon.setEnabled(True)
            self.spinBoxDelay.setEnabled(True)

            return

        self.lineEditLat.setEnabled(False)
        self.lineEditLon.setEnabled(False)
        self.spinBoxDelay.setEnabled(False)

        self.weatherTread.setStatus(True)

        self.weatherTread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = WeatherInfo()
    window.show()

    app.exec()
