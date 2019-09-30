import pymem
import pymem.process
import keyboard
from time import sleep

#offsets
dwGlowObjectManager = (0x524A338)
dwEntityList = (0x4D09F04)
m_iTeamNum = (0xF4)
m_iGlowIndex = (0xA40C)
dwLocalPlayer = (0xCF7A4C)

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll


def startglow(mfv): #the glow
    while True:
        key = mfv[1]
        cscheme = mfv[2]
        if keyboard.is_pressed(key):
            sleep(0.1)
            while True:
                try:
                    sleep(0.001)
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

