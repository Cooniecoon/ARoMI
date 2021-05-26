from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import time
# window widget code
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import QObject
import sys

# widget UI setting
class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.button_start = QPushButton('Start', self)
        self.button_cancel = QPushButton('Cancel', self)
        self.label_status = QLabel('status!!', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_cancel)
        layout.addWidget(self.label_status)

        self.setFixedSize(400, 200)
    @pyqtSlot(int)
    def updateStatus(self, status):
        self.label_status.setText('{}'.format(status))

# main loop
class Example(QObject):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.gui = Window()

        self.gui.show()

# 백그라운드에서 돌아갈 함수 class
class Worker(QObject):
    # 시그널 객체를 하나 생성합니다.
    sig_numbers = pyqtSignal(int)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @pyqtSlot()           # 버튼이 클릭시 시그널을 받아들이는 슬롯을 하나 마련합니다. 
    def startWork(self):
        _cnt = 0
        while _cnt < 10:
            _cnt += 1
            self.sig_numbers.emit(_cnt) # pyqtSignal 에 숫자데이터를 넣어 보낸다
            print(_cnt)                 # consol에서 어떻게 진행 되는지 보기 위해서 넣어준다
            time.sleep(1)

            
class Example(QObject):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.gui = Window()
        
        # 추가되는 코드입니다 
        self.worker = Worker()               # 백그라운드에서 돌아갈 인스턴스 소환
        self.worker_thread = QThread()       # 따로 돌아갈 thread를 하나 생성
        self.worker.moveToThread(self.worker_thread)# worker를 만들어둔 쓰레드에 넣어줍니다
        self.worker_thread.start()           # 쓰레드를 실행합니다.

        self._connectSignals()               # 시그널을 연결하기 위한 함수를 호출
        # 여기까지 추가되는 코드
        
        self.gui.show()
    
    # 시그널을 연결하기 위한 func.
    def _connectSignals(self):
        # gui 의 버튼을 클릭시 연결설정
        self.gui.button_start.clicked.connect(self.worker.startWork)
        # worker에서 발생한 signal(sig_numbers)의 연결 설정
        self.worker.sig_numbers.connect(self.gui.updateStatus)
        # cancel 버튼 연결 설정
        self.gui.button_cancel.clicked.connect(self.forceWorkerReset)

    # 쓰레드의 loop를 중단하고 다시 처음으로 대기 시키는 func.
    def forceWorkerReset(self):
        if self.worker_thread.isRunning():  # 쓰레드가 돌아가고 있다면 
            self.worker_thread.terminate()  # 현재 돌아가는 thread 를 중지시킨다
            self.worker_thread.wait()       # 새롭게 thread를 대기한후
            self.worker_thread.start()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Example(app)
    sys.exit(app.exec_())