import sys
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
import socket

class Aromi(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size, on_top=False):
        super(Aromi,self).__init__()
        self.timer = QtCore.QTimer(self)

        self.img_path = img_path

        self.xy = xy

        self.size = size
        self.on_top = on_top

        self.initUI()
        self.show()
    
    def initUI(self):

        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()

        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w,h))

        movie.start()

        self.setGeometry(self.xy[0],self.xy[1],w,h)

    def mouseDoubleClickEvent(self, e):
        QtWidgets.qApp.quit()

class change_face():
    def __init__(self, category):
        self.category = category


    def select_face(self):
        s0 = Aromi('img\Aromi_normal.gif',xy = [0,0], size=1.0, on_top=True)
        s1 = Aromi('img\Aromi_happy.gif',xy = [0,0],size=1.0,on_top=True)
        s2 = Aromi('img\Aromi_sad.gif',xy = [0,0],size=1.0,on_top=True)
        s3 = Aromi('img\Aromi_embarrass.gif',xy = [0,0],size=1.0,on_top=True)
        select = [s0, s1, s2, s3]

        return select[self.category]
        # if Smile state, we should divide by 3 parts 1) normal->smile 2)smile 3)smile->normal

    def continue_face(self):
        s1 = Aromi('img\Aromi_happy.png',xy = [0,0],size=1.0,on_top=True)
        s2 = Aromi('img\Aromi_sad.png',xy = [0,0],size=1.0,on_top=True)
        s3 = Aromi('img\Aromi_embarrass.png',xy = [0,0],size=1.0,on_top=True)
        select = [None, s1, s2, s3]

        return select[self.category]

    def return_face(self):
        s1 = Aromi('img\Aromi_happy_reverse.gif',xy = [0,0],size=1.0,on_top=True)
        s2 = Aromi('img\Aromi_sad_reverse.gif',xy = [0,0],size=1.0,on_top=True)
        s3 = Aromi('img\Aromi_embarrass_reverse.gif',xy = [0,0],size=1.0,on_top=True)
        select = [None, s1, s2, s3]

        return select[self.category]

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    back_ground = Aromi('img\Aromi_black_background.png',xy = [0,0], size=1.0, on_top=True)
    state = 0
    while True:



        category = input('input :')

        if category == "k":
            sys.exit(app.exec())
            break
        else:
            category = int(category)

            if category > 3 or category < 0: #select[s0,s1,s2,s3]
                pass
            elif category == 0: # normal state
                if state == category:
                    facial = change_face(category).select_face()
                else:
                    facial = change_face(state-category).return_face()
                    state = category
            else: #else state
                if state == category:
                    facial = change_face(category).continue_face()

                else:
                    facial = change_face(category).select_face()
                    state = category

    sys.exit(app.exec())

#Improvements
# - video blink when changed video
# - we should be choose how to make face expression state when we make whole algorithm
# ex.(only gif or gif+png+gif(start,continue,end)) 
# *gif file is played only 14seconds