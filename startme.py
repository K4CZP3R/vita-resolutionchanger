from k4czp3r_psvitares import VitaResFinder
from debug import Debug
vrf = VitaResFinder()

debug=Debug()

main_loop=True

while main_loop:
    debug.clearScreen()
    input_action=vrf.askForAction() #1. info decompiling, 2. res search, 3.
    try: int(input_action)
    except: debug.printError("Selection is not valid!")
    if int(input_action) is 1:
        vrf.showDecompileHelp()
    elif int(input_action) is 2:
        vrf.resSearchMain()  
    elif int(input_action) is 3:
        vrf.newResolution()
    elif int(input_action) is 4:
        vrf.knownResGames()
    elif int(input_action) is 0:
        break
    else:
        debug.printError("Selection not valid!")

    debug.letWait()
debug.print("Thanks for using it!")
debug.print("K4CZP3R, 2018")