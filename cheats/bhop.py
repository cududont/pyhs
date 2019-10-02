import keyboard
import pymem
import pymem.process
from time import sleep
from cheats.offsets import *

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll

def bh(mfv):
    while True:
        dohop = mfv[4]
        sleep(0.001)
        if dohop == True:
            try:
                lp = pym.read_int(client + dwLocalPlayer)
                jump = (client + dwForceJump)
                ground = pym.read_int(lp + m_fFlags)
                
                if keyboard.is_pressed("space") and ground == 257:
                        pym.write_int(jump, int(5))
                        sleep(0.18)
                        pym.write_int(jump, int(4))
                else:
                    sleep(0.001)

            except:
                pass
        else:
            sleep(1)
            
