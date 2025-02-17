"""
Модуль в котором содержаться потоки Qt
"""

import time
import psutil
import requests
from PySide6 import QtCore, QtWidgets


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # TODO Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.delay = None  # TODO создайте атрибут класса self.delay = None, для управлением задержкой получения данных

    def setDelay(self, delay):
        self.delay = delay

    def run(self) -> None:  # TODO переопределить метод run
        if self.delay is None:  # TODO Если задержка не передана в поток перед его запуском
            self.delay = 1  # TODO то устанавливайте значение 1

        while True:  # TODO Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # TODO с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # TODO с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # TODO с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # TODO с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    # TODO Пропишите сигналы, которые считаете нужными
    weatherInfoRecieved = QtCore.Signal(dict)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.lat = lat
        self.lon = lon

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 2
        self.__status = None

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay

    def setStatus(self, status: bool):
        self.__status = status

    def getStatus(self):
        return self.__status

    def setLat(self, lat: float):
        self.lat = lat
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=true"

    def setLon(self, lon: float):
        self.lon = lon
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=true"

    def run(self) -> None:
        # TODO настройте метод для корректной работы
        self.setStatus(True)

        while self.__status:
            response = requests.get(self.__api_url)
            self.weatherInfoRecieved.emit(response.json())
            time.sleep(self.__delay)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    w = WeatherHandler(1, 2)
    w.setStatus(True)
    w.setLat(22)
    w.lat = 33
    print(w.lat)
    w.weatherInfoRecieved.connect(lambda data: print(data))
    w.start()

    app.exec()

    # app = QtWidgets.QApplication()
    #
    # s = SystemInfo()
    # s.systemInfoReceived.connect(lambda data: print(data))
    # s.start()
    #
    # app.exec()








