"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
from PySide6 import QtWidgets
from a_threads import SystemInfo

class CpuRamLoadInfo(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(210, 100)

        self.CpuRamLoadInfoThread = SystemInfo()
        self.CpuRamLoadInfoThread.start()

        self.initUi()
        self.initSignals()


    def initUi(self):
        labelDelay = QtWidgets.QLabel('Интервал обновления, с:')
        self.spinBoxDelay = QtWidgets.QSpinBox()
        self.spinBoxDelay.setMinimum(1)

        l_delay = QtWidgets.QHBoxLayout()
        l_delay.addWidget(labelDelay)
        l_delay.addWidget(self.spinBoxDelay)

        lableCPU = QtWidgets.QLabel('CPU: ')
        lableCPU.setFixedWidth(30)
        self.lineEditCPU = QtWidgets.QLineEdit()
        self.lineEditCPU.setReadOnly(True)

        l_cpu = QtWidgets.QHBoxLayout()
        l_cpu.addWidget(lableCPU)
        l_cpu.addWidget(self.lineEditCPU)

        lableRAM = QtWidgets.QLabel('RAM: ')
        lableRAM.setFixedWidth(30)
        self.lineEditRAM = QtWidgets.QLineEdit()
        self.lineEditRAM.setReadOnly(True)

        l_ram = QtWidgets.QHBoxLayout()
        l_ram.addWidget(lableRAM)
        l_ram.addWidget(self.lineEditRAM)

        l = QtWidgets.QVBoxLayout()
        l.addLayout(l_delay)
        l.addLayout(l_cpu)
        l.addLayout(l_ram)

        self.setLayout(l)

    def initSignals(self):
        self.CpuRamLoadInfoThread.systemInfoReceived.connect(lambda data: self.lineEditCPU.setText(str(data[0])))
        self.CpuRamLoadInfoThread.systemInfoReceived.connect(lambda data: self.lineEditRAM.setText(str(data[1])))
        self.spinBoxDelay.valueChanged.connect(self.CpuRamLoadInfoThread.setDelay)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = CpuRamLoadInfo()
    window.show()

    app.exec()