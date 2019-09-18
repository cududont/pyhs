from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QComboBox, QSlider
from PyQt5.QtCore import QRect, Qt
from threading import Thread
import sys
import pickle
import pymem
import pymem.process
from time import sleep
import keyboard


#offsets
dwGlowObjectManager = (0x5248228)
dwEntityList = (0x4D07DD4)
m_iTeamNum = (0xF4)
m_iGlowIndex = (0xA40C)
dwLocalPlayer = (0xCF5A4C)

app = QApplication(sys.argv)


try: #hook to csgo
    pym = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll
except:
    import ctypes
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'CS:GO Was Not Detected', 'pyhs', 48)
    exit()
    


def apply(): #save color scheme and toggle key
    global key, cscheme, fov
    text = gui.line.text()
    pickle.dump(text, open("data//togglekey.dat", "wb"))
    key = text
    cscheme = gui.ls.currentText()
    pickle.dump(cscheme, open("data//colorscheme.dat", "wb"))
    fov = gui.slider.value()
    pickle.dump(fov, open("data//fov.dat", "wb"))
    
    


class main(QMainWindow): #ui class
    def __init__(self):
        super().__init__()
        self.initUI()
        self.restore()
    
    def restore(self): #restore the settings to the ui after launch
        tkey = pickle.load(open("data//togglekey.dat", "rb"))
        colorscheme = pickle.load(open("data//colorscheme.dat", "rb"))
        fovres = pickle.load(open("data//fov.dat", "rb"))
        self.line.setText(tkey)
        self.ls.setCurrentText(colorscheme)
        self.slider.setValue(fovres)
        
    
    def initUI(self):
        self.setGeometry(0, 0, 210, 200)
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

        #trg = QLabel("Triggerbot", self)
        #trg.move(5, 140)
        #trg.setFont(font)

        self.btn = QPushButton(self)
        self.btn.setText("Apply")
        self.btn.setFont(QFont("Calibri", 10))
        self.btn.resize(199, 30)
        self.btn.move(5, 150)
        self.btn.clicked.connect(apply)

        dev = QLabel(self)
        dev.setText("Developed by cududont")
        dev.setFont(QFont("Calibri", 10))
        dev.resize(130, 30)
        dev.move(5, 175)

        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(80, 80, 80), 3))
        
        painter.drawLine(45,16,200,16)
        painter.drawLine(93,97,200,97)
        #painter.drawLine(75,156,200,156)
        

gui = main()
gui.show()

key = pickle.load(open("data//togglekey.dat", "rb"))
cscheme = pickle.load(open("data//colorscheme.dat", "rb"))
fov = pickle.load(open("data//fov.dat", "rb"))

#color vars 
ctcolorr = 0
ctcolorb = 0
ctcolorg = 0
tcolorr = 0
tcolorb = 0
tcolorg = 0


def newthread(): #create a new thread for glowfunc
    nt = Thread(target=glowfunc)
    nt.daemon = True
    nt.start()

def newthread2(): #thread for fov func
    global nt2
    nt2 = Thread(target=fovfunc)
    nt2.daemon = True
    nt2.start()

def fovfunc():
    from cheats.fov import startfov
    startfov(fov)


def glowfunc(): #the glow
    while True:
        sleep(0.001)
        if keyboard.is_pressed(key):
            sleep(0.1)
            while True:
                try:
                    glow = pym.read_int(dwGlowObjectManager + client)
                    lp = pym.read_int(dwLocalPlayer + client)
                    lpt = pym.read_int(lp + m_iTeamNum) #local player's team

                    if lpt == 2: #t
                        if cscheme == "Red & Blue":
                            ctcolorr = 1
                            ctcolorb = 0
                            ctcolorg = 0
                            tcolorr = 0
                            tcolorb = 1
                            tcolorg = 0

                        else:

                            ctcolorr = 1
                            ctcolorb = 0
                            ctcolorg = 0.4
                            tcolorr = 0
                            tcolorb = 0
                            tcolorg = 1

                    elif lpt == 3: #ct
                        if cscheme == "Red & Blue":
                            ctcolorr = 0
                            ctcolorb = 1
                            ctcolorg = 0
                            tcolorr = 1
                            tcolorb = 0
                            tcolorg = 0

                        else:
                            
                            ctcolorr = 0
                            ctcolorb = 0
                            ctcolorg = 1
                            tcolorr = 1
                            tcolorb = 0
                            tcolorg = 0.4
                       
                    for i in range(1, 32):
                        player = pym.read_int(client + dwEntityList + i * 0x10)

                        if player:
                            team = pym.read_int(player + m_iTeamNum)
                            playerglow = pym.read_int(player + m_iGlowIndex)

                            if team == 2: #t
                                pym.write_float(glow + playerglow * 0x38 + 0x4, float(tcolorr)) #Red
                                pym.write_float(glow + playerglow * 0x38 + 0xC, float(tcolorb)) #Blue
                                pym.write_float(glow + playerglow * 0x38 + 0x8, float(tcolorg)) #Green
                                pym.write_float(glow + playerglow * 0x38 + 0x10, float(1)) #Opacity
                                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1)) 
                            
                            elif team == 3: #ct
                                pym.write_float(glow + playerglow * 0x38 + 0x4, float(ctcolorr)) #Red
                                pym.write_float(glow + playerglow * 0x38 + 0xC, float(ctcolorb)) #Blue
                                pym.write_float(glow + playerglow * 0x38 + 0x8, float(ctcolorg)) #Green
                                pym.write_float(glow + playerglow * 0x38 + 0x10, float(1)) #Opacity
                                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1))      
                    
                                
                except pymem.exception.MemoryReadError:
                    ctcolorr = 0
                    ctcolorb = 0
                    ctcolorg = 0
                    tcolorr = 0
                    tcolorb = 0
                    tcolorg = 0
            
                if keyboard.is_pressed(key):
                    sleep(0.1)
                    break

newthread()
newthread2()
    
sys.exit(app.exec_())
