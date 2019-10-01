from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QComboBox, QSlider, QCheckBox
from PyQt5.QtCore import QRect, Qt
from threading import Thread
import sys
import pickle
import pymem
import pymem.process


app = QApplication(sys.argv)

fov = pickle.load(open("data//fov.dat", "rb"))
key = pickle.load(open("data//togglekey.dat", "rb"))
cscheme = pickle.load(open("data//colorscheme.dat", "rb"))
tbkey = pickle.load(open("data//tbkey.dat", "rb"))
enbh = pickle.load(open("data//enbh.dat", "rb"))

mfv = [fov, key, cscheme, tbkey, enbh]
mfv[0] = fov
mfv[1] = key
mfv[2] = cscheme
mfv[3] = tbkey
mfv[4] = enbh


try: #hook to csgo
    pym = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll
except:
    import ctypes
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'CS:GO Was Not Detected', 'pyhs', 48)
    exit()
    


def apply(): #set new params and dump them
    text = gui.line.text()
    pickle.dump(text, open("data//togglekey.dat", "wb"))
    key = text
    cscheme = gui.ls.currentText()
    pickle.dump(cscheme, open("data//colorscheme.dat", "wb"))
    fov = gui.slider.value()
    pickle.dump(fov, open("data//fov.dat", "wb"))
    tbkey = gui.line2.text()
    pickle.dump(tbkey, open("data//tbkey.dat", "wb"))

    if gui.ebbh.isChecked() == True:
        enbh = True
    else:
        enbh = False

    pickle.dump(enbh, open("data//enbh.dat", "wb"))
    print(enbh)

    mfv[0] = fov
    mfv[1] = key
    mfv[2] = cscheme
    mfv[3] = tbkey
    mfv[4] = enbh
    

class main(QMainWindow): #ui class
    def __init__(self):
        super().__init__()
        self.initUI()
        self.restore()
    
    def restore(self): #restore the settings to the ui after launch
        tkey = pickle.load(open("data//togglekey.dat", "rb"))
        colorscheme = pickle.load(open("data//colorscheme.dat", "rb"))
        fovres = pickle.load(open("data//fov.dat", "rb"))
        tbkeyd = pickle.load(open("data//tbkey.dat", "rb"))
        enbhd = pickle.load(open("data//enbh.dat", "rb"))

        self.line.setText(tkey)
        self.ls.setCurrentText(colorscheme)
        self.slider.setValue(fovres)
        self.line2.setText(tbkeyd)

        if enbhd == True:
            self.ebbh.setChecked(True)
        else:
            self.ebbh.setChecked(False)

        
    
    def initUI(self): #init the ui
        self.setGeometry(0, 0, 210, 310)
        self.setWindowTitle("pyhs")
        self.setWindowIcon(QIcon("assets//ico.png"))

        font = QFont("Calibri", 11)
        font.setBold(True)

        gl = QLabel("Glow", self)
        gl.move(5, 0)
        gl.setFont(font)
       
        schm = QLabel("Color Scheme: ", self)
        schm.move(5, 25)
        schm.setFont(QFont("Calibri", 11))

        self.ls = QComboBox(self)
        self.ls.setGeometry(QRect(103, 30, 100, 21))
        self.ls.setObjectName("comboBox")
        self.ls.addItem("Red & Blue")
        self.ls.addItem("Orange & Green")
        self.ls.setFont(QFont("Calibri", 9))
        
        t = QLabel("Toggle Key: ", self)
        t.move(5, 50)
        t.setFont(QFont("Calibri", 11))

        self.line = QLineEdit(self)
        self.line.resize(120, 21)
        self.line.move(83, 55)
        self.line.setFont(QFont("Calibri", 10))

        fv = QLabel("FOV Changer", self)
        fv.move(5, 80)
        fv.setFont(font)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setTickInterval(30)
        self.slider.setTickPosition(2)
        self.slider.move(15,110)
        self.slider.setMaximum(150)
        self.slider.setMinimum(90)
        self.slider.resize(180,20)
        self.slider.setSingleStep(0)
        
        v = QLabel("90°", self)
        v.move(15, 120)
        v.setFont(QFont("Calibri", 8))

        v2 = QLabel("120°", self)
        v2.move(98, 120)
        v2.setFont(QFont("Calibri", 8))
        
        v3 = QLabel("150°", self)
        v3.move(180, 120)
        v3.setFont(QFont("Calibri", 8))

        trg = QLabel("Triggerbot", self)
        trg.move(5, 140)
        trg.setFont(font)

        tbb = QLabel("Toggle Key: ", self)
        tbb.move(5, 170)
        tbb.setFont(QFont("Calibri", 11))

        self.line2 = QLineEdit(self)
        self.line2.resize(120, 21)
        self.line2.move(83, 175)
        self.line2.setFont(QFont("Calibri", 10))

        ebt = QLabel("Bhop", self)
        ebt.move(5, 200)
        ebt.setFont(font)

        self.ebbh = QCheckBox("Enable Bhop", self)
        self.ebbh.move(10, 225)
        self.ebbh.setFont(QFont("Calibri", 11))
        
        self.btn = QPushButton(self)
        self.btn.setText("Apply")
        self.btn.setFont(QFont("Calibri", 10))
        self.btn.resize(199, 30)
        self.btn.move(5, 260)
        self.btn.clicked.connect(apply)

        dev = QLabel(self)
        dev.setText("Developed by cududont")
        dev.setFont(QFont("Calibri", 10))
        dev.resize(130, 30)
        dev.move(5, 285)

        
    def paintEvent(self, event): #draw lines to to seperate ui
        painter = QPainter(self)
        painter.setPen(QPen(QColor(80, 80, 80), 3))
        
        painter.drawLine(45,16,200,16)
        painter.drawLine(93,97,200,97)
        painter.drawLine(75,156,200,156)
        painter.drawLine(45,215,200,215)
        

gui = main()
gui.show()


def newthread(): #create a new thread for glowfunc
    from cheats.glow import startglow
    nt = Thread(target=startglow, args=(mfv,), daemon = True)
    nt.start()
   

def newthread2(): #thread for fov func
    from cheats.fov import startfov
    nt2 = Thread(target=startfov, args=(mfv,), daemon = True) 
    nt2.start()

def newthread3(): #thread for triggerbot
    from cheats.triggerbot import tb
    nt3 = Thread(target=tb, args=(mfv,), daemon = True) 
    nt3.start()

def newthread4(): #thread for triggerbot
    from cheats.bhop import bh
    nt4 = Thread(target=bh, args=(mfv,), daemon = True) 
    nt4.start()

newthread()
newthread2()
newthread3()
newthread4()


sys.exit(app.exec_())