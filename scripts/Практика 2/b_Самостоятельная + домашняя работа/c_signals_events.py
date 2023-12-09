"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


import time
from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.__initSignals()

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        """
        Событие изменения положения окна

        :param event: QtGui.QMoveEvent
        :return: None
        """

        print(f'{time.ctime()} >>> Старая позиция: {event.oldPos()}')
        print(f'{time.ctime()} >>> Новая позиция: {event.pos()}')
        print('-----')

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """

        print(f'{time.ctime()} >>> Новый размер окна: {event.size().toTuple()}')
        print('-----')

    def __initUi(self) -> None:
        """
        Инициализация UI

        @return: None
        """

        #Перемещение по углам + центр

        self.pushButtonLT = QtWidgets.QPushButton('Лево/Верх')
        self.pushButtonLT.setFixedHeight(50)
        self.pushButtonRT = QtWidgets.QPushButton('Право/Верх')
        self.pushButtonRT.setFixedHeight(50)

        l_windowPushButtonsTop = QtWidgets.QHBoxLayout()
        l_windowPushButtonsTop.addWidget(self.pushButtonLT)
        l_windowPushButtonsTop.addWidget(self.pushButtonRT)

        self.pushButtonCenter = QtWidgets.QPushButton('Центр')
        self.pushButtonCenter.setFixedHeight(50)

        self.pushButtonLB = QtWidgets.QPushButton('Лево/Низ')
        self.pushButtonLB.setFixedHeight(50)
        self.pushButtonRB = QtWidgets.QPushButton('Право/Низ')
        self.pushButtonRB.setFixedHeight(50)

        l_windowPushButtonsBottom = QtWidgets.QHBoxLayout()
        l_windowPushButtonsBottom.addWidget(self.pushButtonLB)
        l_windowPushButtonsBottom.addWidget(self.pushButtonRB)

        # Перемещение по координатам

        self.labelX = QtWidgets.QLabel('X')
        self.labelX.setFixedWidth(20)
        self.spinBoxX = QtWidgets.QSpinBox()
        self.spinBoxX.setMinimum(0)

        self.labelY = QtWidgets.QLabel('Y')
        self.labelY.setFixedWidth(20)
        self.spinBoxY = QtWidgets.QSpinBox()
        self.spinBoxY.setMinimum(0)

        self.pushButtonMooveItMooveIt = QtWidgets.QPushButton('Переместить')
        self.pushButtonMooveItMooveIt.setFixedHeight(25)

        l_coordsSettings = QtWidgets.QHBoxLayout()
        l_coordsSettings.addWidget(self.labelX)
        l_coordsSettings.addWidget(self.spinBoxX)
        l_coordsSettings.addWidget(self.labelY)
        l_coordsSettings.addWidget(self.spinBoxY)

        l_coords = QtWidgets.QVBoxLayout()
        l_coords.addLayout(l_coordsSettings)
        l_coords.addWidget(self.pushButtonMooveItMooveIt)

        gr_windowCoords = QtWidgets.QGroupBox('Переместить в координаты:')
        gr_windowCoords.setLayout(l_coords)
        gr_windowCoords.setFixedHeight(80)

        vSpacer = QtWidgets.QSpacerItem(0, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Группа с настройками положения (левая колонка)
        l_windowPos = QtWidgets.QVBoxLayout()
        l_windowPos.addLayout(l_windowPushButtonsTop)
        l_windowPos.addWidget(self.pushButtonCenter)
        l_windowPos.addLayout(l_windowPushButtonsBottom)
        l_windowPos.addWidget(gr_windowCoords)
        l_windowPos.addItem(vSpacer)

        gr_windowPos = QtWidgets.QGroupBox('Перемещение окна:')
        gr_windowPos.setLayout(l_windowPos)
        gr_windowPos.setFixedWidth(190)

        # Область с логом
        self.plainTextEditLog = QtWidgets.QPlainTextEdit()
        self.plainTextEditLog.setMinimumSize(460, 360)

        self.pushButtonGetData = QtWidgets.QPushButton('Получить данные окна')
        self.pushButtonGetData.setFixedHeight(25)

        l_log = QtWidgets.QVBoxLayout()
        l_log.addWidget(self.plainTextEditLog)
        l_log.addWidget(self.pushButtonGetData)

        gr_log = QtWidgets.QGroupBox('Лог:')
        gr_log.setLayout(l_log)

        #Основной слой

        l_main = QtWidgets.QHBoxLayout()
        l_main.addWidget(gr_windowPos)
        l_main.addWidget(gr_log)

        self.setLayout(l_main)

    def __initSignals(self):
        """
        Инициализация сигналов

        @return:
        """
        self.pushButtonLT.clicked.connect(self.onPushButtonLTClicked)
        self.pushButtonRT.clicked.connect(self.onPushButtonRTClicked)
        self.pushButtonLB.clicked.connect(self.onPushButtonLBClicked)
        self.pushButtonRB.clicked.connect(self.onPushButtonRBClicked)
        self.pushButtonCenter.clicked.connect(self.onPushButtonCenterClicked)
        self.pushButtonMooveItMooveIt.clicked.connect(self.onPushButtonMooveItMooveItClicked)
        self.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)

    def getActiveScreen(self) -> QtGui.QScreen:
        """
        Функция определения активного (текущего) монитора, на котором отображается окно программы

        @return: QtGui.QScreen
        """
        screens = QtCore.QCoreApplication.instance().screens()

        screenBoarders = [i.availableSize().width() for i in screens]
        for i in range(1, len(screenBoarders)):
            screenBoarders[i] += screenBoarders[i - 1]

        currentScreen = QtGui.QScreen

        for num, pos in enumerate(screenBoarders):
            if self.pos().x() < pos:
                currentScreen = screens[num]
                break

        return currentScreen

    def getScreenEndPoints(self) -> dict:
        """
        Функция определения конечных координат (px) мониторов

        @return: словарь
        """
        screens = QtCore.QCoreApplication.instance().screens()

        screensEndPointX = [i.availableSize().width() for i in screens]
        for i in range(1, len(screensEndPointX)):
            screensEndPointX[i] += screensEndPointX[i - 1]
        screensEndPointY = [i.availableSize().height() for i in screens]

        screenEndCoords = {}
        for pos, screen in enumerate(screens):
            screenEndCoords[screen] = (screensEndPointX[pos], screensEndPointY[pos])

        return screenEndCoords

    @QtCore.Slot()
    def onPushButtonLTClicked(self) -> None:
        currentScreen = self.getActiveScreen()
        screenEndCoords = self.getScreenEndPoints()[currentScreen]
        self.move(screenEndCoords[0] - currentScreen.availableSize().width(), 0)

    @QtCore.Slot()
    def onPushButtonRTClicked(self) -> None:
        currentScreen = self.getActiveScreen()
        screenEndCoords = self.getScreenEndPoints()[currentScreen]
        self.move(screenEndCoords[0] - self.width(), 0)

    @QtCore.Slot()
    def onPushButtonLBClicked(self) -> None:
        currentScreen = self.getActiveScreen()
        screenEndCoords = self.getScreenEndPoints()[currentScreen]
        self.move(screenEndCoords[0] - currentScreen.availableSize().width(), screenEndCoords[1] -
                  self.height())
        # Работает криво! На WIN10 из доступной высоты надо как-то вычесть высоту панели задач... У меня не получилось.

    @QtCore.Slot()
    def onPushButtonRBClicked(self) -> None:
        currentScreen = self.getActiveScreen()
        screenEndCoords = self.getScreenEndPoints()[currentScreen]
        self.move(screenEndCoords[0] - self.width(), screenEndCoords[1] - self.height())
        # Работает криво! На WIN10 из доступной высоты надо как-то вычесть высоту панели задач... У меня не получилось.

    @QtCore.Slot()
    def onPushButtonCenterClicked(self) -> None:
        currentScreen = self.getActiveScreen()
        screenEndCoords = self.getScreenEndPoints()[currentScreen]
        self.move(screenEndCoords[0] - currentScreen.size().width() / 2 - self.width() / 2,
                  (screenEndCoords[1] - self.height()) / 2)

    @QtCore.Slot()
    def onPushButtonMooveItMooveItClicked(self):
        self.move(self.spinBoxX.value(), self.spinBoxY.value())

    @QtCore.Slot()
    def onPushButtonGetDataClicked(self) -> None:
        app = QtCore.QCoreApplication.instance()
        screens = app.screens()
        currentScreen = self.getActiveScreen()

        log_str = f'Лог от "{time.ctime()}"\n'
        log_str += f'* Кол-во экранов: {len(screens)}\n'
        log_str += f'* Текущее основное окно: {app}\n'
        log_str += f'* Активный экран: {currentScreen}\n'
        log_str += f'* Разрешение активного экрана, px: {currentScreen.size().width()}x{currentScreen.size().height()}\n'
        log_str += f'* Размер окна, px: {self.width()}x{self.height()}\n'
        log_str += f'* Минимальный размер окна, px: {self.minimumWidth()} x {self.minimumHeight()}\n'
        log_str += f'* Текущее положение (координаты) окна, px: {self.pos().x()}x{self.pos().y()}\n'
        log_str += f'* Координаты центра приложения, px: {self.width() / 2 + self.pos().x()}x' \
                   f'{self.height() / 2 + self.pos().y()}\n'
        log_str += f'* Состояние окна: {app.applicationState()}\n'
        log_str += '----------'

        self.plainTextEditLog.setPlainText(log_str)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
