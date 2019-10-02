import pymem
import pymem.process
from time import sleep
from cheats.offsets import *

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll

def startfov(fovL):
    while True:
        try:
            fovSET = fovL[0]
            lp = pym.read_int(dwLocalPlayer + client)
            
            wpn = pym.read_int(lp + m_hActiveWeapon)
            wpnindex = wpn & 0xFFF
            wpnentity = pym.read_int(client + (wpnindex -1) * 0x10 + dwEntityList)
            wpnid = pym.read_int(wpnentity + m_iItemDefinitionIndex)
            
            if wpnid == 9 or wpnid == 40 or wpnid == 11 or wpnid == 38:
                pass

            else:
                pym.write_int(lp + m_iFOV, int(fovSET))
                
        except pymem.exception.MemoryReadError:
            pass



        