import pymem
import pymem.process
from time import sleep

pym = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll


dwLocalPlayer = (0xCF7A4C)
dwForceAttack = (0x313B5F0)
m_iCrosshairId = (0xB3AC)

while True:
    lp = pym.read_int(dwLocalPlayer + client)
    entity = pym.read_int(lp + m_iCrosshairId)

    sleep(0.001)

    if entity > 0 and entity <= 64:
        pym.write_int(client + dwForceAttack, int(5))
    else:

        pym.write_int(client + dwForceAttack, int(4))

        
