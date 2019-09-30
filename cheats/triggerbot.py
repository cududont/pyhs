import pymem
import pymem.process
from time import sleep
import keyboard

dwLocalPlayer = (0xCF7A4C)
dwForceAttack = (0x313B5F0)
m_iCrosshairId = (0xB3AC)
m_iTeamNum = (0xF4)
dwEntityList = (0x4D09F04)

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll

def tb(mfv):
    while True:
        tbkey = mfv[3]
        sleep(0.001)
        if keyboard.is_pressed(tbkey):
            sleep(0.1)
            while True:
                try:
                    sleep(0.001)

                    lp = pym.read_int(dwLocalPlayer + client)
                    chid = pym.read_int(lp + m_iCrosshairId)

                    if chid > 0 and chid <= 64:
                        entity = pym.read_int(client + dwEntityList + (chid -1) * 0x10)

                        entityteam = pym.read_int(entity + m_iTeamNum)
                        lpteam = pym.read_int(lp + m_iTeamNum)

                        if entityteam != lpteam:
                            pym.write_int(client + dwForceAttack, int(5))
                        else:
                            pym.write_int(client + dwForceAttack, int(4))
                            
                    else:
                        pym.write_int(client + dwForceAttack, int(4))

                except:
                    pass

                if keyboard.is_pressed(tbkey):
                    sleep(0.2)
                    break
                        




