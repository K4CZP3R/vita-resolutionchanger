from debug import Debug
import values
from pathlib import Path
import time
from colorama import Fore, Back
import binascii
class VitaResFinder:
    def __init__(self):
        self.debug = Debug()
        self.startLogo()
        self.startWarning()
        self.debug.letWait()
    def startLogo(self):
        self.debug.print("VitaResFinder, version:{0} by K4CZP3R".format(values.version))
    def startWarning(self):
        self.debug.print("THIS TOOL IS NOT NOOB-PROOF, It'll only work if you know what you are doing",color=Fore.RED)
    def askForAction(self):
        self.debug.print("Question \/ \nChoose option\n1. Help about decompiling bin to arm\n2. Search for resolution entry in arm code\n3. Get new resolution entry\n4. Show known mods\n0. Exit")
        tmp=self.debug.ask("Selection")
        return tmp
    
    def showDecompileHelp(self):
        self.debug.print("Decompile help selected!")
        help_lines=["=== basic info ===","To decompile eboot.bin to desired format you'll need:","1. Modified prx-tool (included)","2. (decrypted) eboot.bin [tested on maidumps eboots]","3. Default resolution of game (ex. 720x408)"]
        prxtool_help_lines=["=== prx-tool info ===","To decompile it, follow these steps:","1. Get eboot.bin of your game and copy it near prx-tool","2. Run following command","Where ebootbin, give path of eboot.bin","Where ebootout, give path of output (file needed for this script)","./prxtool -r 0x0 -i -b -w -n db.json ebootbin > ebootout","Then wait a couple of minutes (no progress bar)"]
        program_help_lines=['=== VitaResFinder ===',"After you have decompiled your eboot with prx-tool and you know default resolution of your game","You can choose option 2 in this program","After saving results of option 2, go to option 3 to generate new resolution"]


        for line in help_lines:
            self.debug.print(line)
        for line in prxtool_help_lines:
            self.debug.print(line)
        for line in program_help_lines:
            self.debug.print(line)
    def resSearchMain(self):
        self.debug.print("Resolution search selected!")
        input_eboot=str(self.debug.ask("Location of decompiled eboot.bin"))
        input_resx=str(self.debug.ask("Default width resolution (ex *720*x408)"))
        input_resy=str(self.debug.ask("Default height resolution (ex 720x*408*)"))
        input_armfunction=str(self.debug.ask("ARM fuction to search ({0})? ".format(values.default_armfunction)))
        if(len(input_armfunction)!=0):
            armfunction=input_armfunction
        else:
            armfunction=values.default_armfunction
        
        summary_lines=["=== summary ===","Eboot: {0}".format(input_eboot),"Resolution: {0}x{1}".format(input_resx,input_resy),"ARM Function: {0}".format(armfunction)]
        for line in summary_lines:
            self.debug.print(line)
        input_change=self.debug.ask("Want to change something? (path,resx,resy,armfunc,no)")
        if str(input_change) == "path": input_eboot=str(self.debug.ask("Location of decompiled eboot.bin"))
        if str(input_change) == "resx": input_resx=str(self.debug.ask("Default width resolution (ex *720*x408)"))
        if str(input_change) == "resy": input_resy=str(self.debug.ask("Default height resolution (ex 720x*408*)"))
        if str(input_change) == "armfunc": input_armfunction=str(self.debug.ask("ARM fuction to search ({0})? ".format(values.default_armfunction)))
        
        self.debug.print("Will perform checks on user input...")
        if not Path(input_eboot).is_file():
            self.debug.printError("Can't find {0}".format(input_eboot))
            return
        if len(input_resx) != 3 or len(input_resy) != 3:
            self.debug.printError("Resolution is too big/small")
            return
        action_resx="{0}{1}".format("#",str(hex(int(input_resx))).upper().replace('X','x'))
        action_resy="{0}{1}".format("#",str(hex(int(input_resy))).upper().replace('X','x'))
        self.debug.print("Ok, will search for those values: {0} and {2} ({1}x{3})".format(action_resx,input_resx,action_resy,input_resy))
        self.resSearchAction(input_eboot,armfunction,action_resx,action_resy)
    def resSearchAction(self,path,instr,resx,resy):
        resx=resx.lower()
        resy=resy.lower()
        instr=instr.lower()

        location_a=0
        location_b=0
        value_a=""
        value_b=""
        closeList=list()
        maxSpace=32
        count=0
        info=""
        line_color=Fore.GREEN

        self.debug.print("Opening file to read lines (will take a minute or 2)")
        f=open(path)
        f_lines=len(f.readlines())
        f.close()
        self.debug.print("File contains {0} lines".format(str(f_lines)))

        f=open(path)
        start_time=time.time()
        while count<f_lines:
            line=f.readline().strip('\n').lower()
            if instr in line:
                if resx in line or resy in line:
                    location_a=count
                    value_a=line
                    if((location_a-location_b)<maxSpace):
                        line_color=Fore.RED
                        if resx in value_a and resx in value_b:
                            info="{0} copy".format(resx)
                        elif resy in value_a and resy in value_b:
                            info="{0} copy".format(resy)
                        else:
                            closeList.append("//begin\nvalA: '{0}' [@{1}line]\nvalB: '{2}' [@{3}line]\n//end\n".format(str(value_a),str(location_a),str(value_b),str(location_b)))
                    else:
                        info=""
                        line_color=Fore.GREEN
                    print("{0}{1}     * [delta:{2}, line:{3}/{5}] {4}*".format(line_color,line,str(location_a-location_b),str(count),str(info),str(f_lines-count)))
                    location_b=location_a
                    value_b=value_a
            count=count+1
        end_time=time.time()-start_time
        self.debug.print("Took {0}s".format(str(end_time)))
        self.debug.print("Showing results, save them in pairs (valA,valB)")
        print(*closeList,sep='\n')
    def newResolution(self):
        self.debug.print("Resolution update selected!")
        input_eboot=str(self.debug.ask("Location of eboot.bin (NOT prxtooled EBOOT)"))
        info_lines=[" === Resolution change ===","To perform it you'll need:","valA and valB from option 2"]
        info_lines_example=["//valA example: ' 0x00196210: 0x72ccf45f '_..r' - movs.w     a3, #0x198' [@424324line]","//valB example: ' 0x0019620c: 0x7134f45f '_.4q' - movs.w     a2, #0x2d0' [@424323line]"]
        for line in info_lines:
            self.debug.print(line,color=Fore.YELLOW)
        for line in info_lines_example:
            self.debug.print(line,color=Fore.BLUE)
        resolution_info_lines=[" === Following resolutions are supported ===","960x544, 720x408, 640x368, 480x272"]
        for line in resolution_info_lines:
            self.debug.print(line)
        
        default_resx=self.debug.ask("What was the default width resolution? (ex *720*x408)")
        default_resy=self.debug.ask("What was the default height resolution? (ex 720x*408*)")
        default_resolution_lines=["=== Default resolutions ===","Width: {0}, search for value: {1}".format(str(default_resx),hex(int(default_resx))),"Height: {0}, search for value: {1}".format(str(default_resy),hex(int(default_resy)))]
        for line in default_resolution_lines:
            self.debug.print(line)
        
        supported_resolutions_lines=["=== Supported resolutions ===","960 | 544","720 | 408","640 | 368","480 | 272"]
        for line in supported_resolutions_lines:
            self.debug.print(line)
        new_resx=self.debug.ask("What is new width resolution (ex 640)")
        new_resy=self.debug.ask("What is new height resolution (ex 368)")
        update_resolution_lines=["Change in valA and valB: {0} to {1} and {2} to {3}".format(hex(int(default_resx)),hex(int(new_resx)),hex(int(default_resy)),hex(int(new_resy))),"Then, visit: http://armconverter.com and select x32 - ARM32/AArch32/ARMv7 Converter and then paste function of valA and then of valB","Get Thumb-2 HEX from this website"]
        update_resolution_lines_example=["//example: copy 'movs.w     a1, #0x198' to the site and get Thumb-2 HEX"]
        for line in update_resolution_lines:
            self.debug.print(line)
        for line in update_resolution_lines_example:
            self.debug.print(line,color=Fore.BLUE)
        
        offset_lines=["Get offset of height and width instruction (0xOFFSET)"]
        offset_lines_example=["//example: 0xOFFSET: 0xInstrOff '_..p' - movs.w     a1, #0x198"]
        for line in offset_lines:
            self.debug.print(line)
        for line in offset_lines_example:
            self.debug.print(line,color=Fore.BLUE)

        offset_width=self.debug.ask("Offset of width instruction")
        thumb2_width=self.debug.ask("Thumb2 HEX of width instruction")
        offset_height=self.debug.ask("Offset of height instruction")
        thumb2_height=self.debug.ask("Thumb2 HEX of height instruction")

        offset2_lines=["You have 2 methods","1. Patch it yourself using hxd","2. Let program patch it"]
        for line in offset2_lines:
            self.debug.print(line)
        
        input_selection=self.debug.ask("Selected method")
        if(int(input_selection) is 2):
            self.newResolutionPatch(input_eboot,offset_width,thumb2_width,offset_height,thumb2_height)
        else:
            offset3_lines=["Open hex editor (Edit hex, not characters!):","1. Go to {0} and enter {1}".format(offset_width,thumb2_width),"2. Go to {0} and enter {1}".format(offset_height,thumb2_height)]
            for line in offset3_lines:
                self.debug.print(line)
            self.debug.letWait()
        self.debug.print("All actions performed, copy patched eboot.bin and try to run game!")
    def newResolutionPatch(self,file,offset_w,thumb2_w,offset_h,thumb2_h):
        summary_lines=["Will patch {0} at offsets: {1} and {2} with values {3} and {4}".format(file,offset_w,offset_h,thumb2_w,thumb2_h)]
        for line in summary_lines:
            self.debug.print(line)
        #binascii.a2b_hex("THUMB2")
        offset_w=int(offset_w,16)
        offset_h=int(offset_h,16)
        self.debug.print("Writing thumb2 of width!")
        f=open(file,"r+b")
        f.seek(offset_w)
        f.write(binascii.a2b_hex(thumb2_w))
        f.close()
        self.debug.print("OK!")
        self.debug.print("Writing thumb2 of height!")
        f=open(file,"r+b")
        f.seek(offset_h)
        f.write(binascii.a2b_hex(thumb2_h))
        f.close()
        self.debug.print("OK!")
    def knownResGames(self):
        self.debug.print("Known games!")
        for x in range(0,len(values.known_games)):
            info="Game: '{0}' | mod for '{1}' | change (offset, value): '{2}' and '{3}'".format(values.known_games[x],values.known_mod[x],values.known_offsetandval_w[x],values.known_offsetandval_h[x])
            self.debug.print(info)