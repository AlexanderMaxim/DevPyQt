"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.__initSignals()

    def __initUi(self):

        self.knob = QtWidgets.QDial()
        self.cbox = QtWidgets.QComboBox()
        self.cbox.insertItems(0, ['oct', 'hex', 'bin', 'dec'])
        self.LCDNum = QtWidgets.QLCDNumber()
        self.LCDNum.setDigitCount(7)
        self.LCDNum.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)

        l_v = QtWidgets.QVBoxLayout()
        l_v.addWidget(self.cbox)
        l_v.addWidget(self.LCDNum)

        l_h = QtWidgets.QHBoxLayout()
        l_h.addWidget(self.knob)
        l_h.addLayout(l_v)

        l_main = QtWidgets.QVBoxLayout()
        l_main.addLayout(l_h)
        l_main.addWidget(self.slider)

        l_main.installEventFilter(self)

        self.setLayout(l_main)

        self.__load()

    def __initSignals(self):
        self.knob.valueChanged.connect(self.onKnobValueChanged)
        self.slider.valueChanged.connect(lambda: self.knob.setValue(self.slider.value()))
        self.cbox.currentTextChanged.connect(self.onKnobValueChanged)

    def onKnobValueChanged(self):
        self.slider.setValue(self.knob.value())
        self.LCDNum.display(self.knob.value())
        if self.cbox.currentText() == 'oct':
            self.LCDNum.setMode(QtWidgets.QLCDNumber.Oct)
            # self.LCDNum.setOctMode()
            print(f'Новое значение dial = {oct(self.knob.value())} ({self.cbox.currentText()})')
        if self.cbox.currentText() == 'hex':
            self.LCDNum.setMode(QtWidgets.QLCDNumber.Hex)
            # self.LCDNum.setHexMode()
            print(f'Новое значение dial = {hex(self.knob.value())} ({self.cbox.currentText()})')
        if self.cbox.currentText() == 'bin':
            self.LCDNum.setMode(QtWidgets.QLCDNumber.Bin)
            # self.LCDNum.setBinMode()
            print(f'Новое значение dial = {bin(self.knob.value())} ({self.cbox.currentText()})')
        if self.cbox.currentText() == 'dec':
            self.LCDNum.setMode(QtWidgets.QLCDNumber.Dec)
            # self.LCDNum.setDecMode()
            print(f'Новое значение dial = {self.knob.value()} ({self.cbox.currentText()})')

        self.__save()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> bool:
        if (event.key() == ord('+') or event.key() == ord('=')) and self.knob.value() < 99:
            self.knob.setValue(self.knob.value() + 1)
        if event.key() == ord('-') and self.knob.value() > 0:
            self.knob.setValue(self.knob.value() - 1)

        return super(Window, self).keyPressEvent(event)

    def __load(self):
        settings = QtCore.QSettings('KnobSettings')
        knobValue = settings.value('knobValue', '')
        cboxText = settings.value('cboxText', '')
        LCDNumMode = settings.value('LCDNumMode', '')

        self.knob.setValue(int(knobValue))
        self.slider.setValue(int(knobValue))
        self.cbox.setCurrentText(str(cboxText))
        self.LCDNum.display(int(knobValue))
        self.LCDNum.setMode(LCDNumMode)

    def __save(self):
        settings = QtCore.QSettings('KnobSettings')
        settings.setValue('knobValue', self.knob.value())
        settings.setValue('cboxText', self.cbox.currentText())
        settings.setValue('LCDNumMode', self.LCDNum.mode())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
