import pymem
import pymem.process
from time import sleep
from cheats.offsets import *

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll

def antif(mfv):
    while True:
        sleep(0.01)
        enan = mfv[5]
        if enan == True:  
            try:
                lp = pym.read_int(client + dwLocalPlayer)
                flashdur = pym.read_int(lp + m_flFlashDuration)

                if flashdur > 0:
                    pym.write_int(lp + m_flFlashDuration, int(0))
                else:
                    pass

            except:
                pass
        else:
            sleep(0.1)

