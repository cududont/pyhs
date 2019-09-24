import pymem
import pymem.process
from time import sleep


pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll

dwLocalPlayer = (0xCF7A3C)
m_hActiveWeapon = (0x2EF8)
dwEntityList = (0x4D09EF4)
m_iItemDefinitionIndex = (0x2FAA)
m_iFOV = (0x31E4)
m_bIsScoped = (0x3910)

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
                
        except Exception as e:
            print(e)



        