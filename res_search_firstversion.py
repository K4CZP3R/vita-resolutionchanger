#First version of script, don't use it. Just use startme.py

from time import sleep, time
from colorama import Fore, Back, init
import os
hardcoded_filepath="jak3_eboot.txt"
hardcoded_sf1=""
hardcoded_sf2="#0x280"
hardcoded_sf3="#0x170"
hardcoded_maxspc=100

#define for later
filepath=""
maxspc=0
sf1=""
sf2=""
sf3=""
line_normalColor=Fore.GREEN
line_foundColor=Fore.RED
line_color=line_normalColor
locationa=0
valuea=""
locationb=0
valueb=""
info=""
count=0
closeList=list()


#on start clean and init of colorama
os.system("cls")
init(autoreset=True)

def askVars():
    global filepath, maxspc,sf1, sf2, sf3
    filepath=input("Filepath ({}): ".format(hardcoded_filepath))
    if(len(filepath) == 0):
        filepath=hardcoded_filepath
    
    maxspc=input("Max space between lines ({}): ".format(str(hardcoded_maxspc)))
    if(len(maxspc)==0):
        maxspc=hardcoded_maxspc

    sf1=input("Search filter 1 [function] ({}): ".format(hardcoded_sf1))
    if(len(sf1)== 0):
        sf1=hardcoded_sf1

    sf2=input("Search filter 2 [value] ({}): ".format(hardcoded_sf2))
    if(len(sf2)== 0):
        sf2=hardcoded_sf2

    sf3=input("Search filter 3 [value] ({}): ".format(hardcoded_sf3))
    if(len(sf3)== 0):
        sf3=hardcoded_sf3
def showIntro():
    print("Input file needs to be output of prxtool")
    print("In search filter 1 choose asm function (mov)")
    print("In another search filters enter resolution x and y (example: #0x198 or 408)")
def showSummary():
    print("Program will search in {0} using following filters {1},{2},{3} | max space: {4} \n{5}Default Color {6} Found Color".format(filepath,sf1,sf2,sf3,maxspc,line_normalColor,line_foundColor)) 

def showResults():
    print(*closeList,sep='\n')

showIntro()
askVars()
showSummary()

print("Opening... ({})".format(filepath))
f = open(filepath)
print("Counting lines... (might take a while)")
f_lines = len(f.readlines())
print("File contains {0} lines".format(str(f_lines)))
f.close()

f=open(filepath)
skiplines = input("Want to skip lines? n/lines: ")
if("n" not in skiplines):
    print("Skipping...")
    for x in range(0, int(skiplines)):
        f.readline()
    print("Skipped {0} lines".format(skiplines))

start_time=time()
while count<f_lines:
    line=f.readline().strip('\n')
    if sf1 in line:
        if sf2 in line or sf3 in line:
            locationa=count
            valuea=line
            if((locationa-locationb)<maxspc):
                line_color=line_foundColor
                if sf2 in valuea and sf2 in valueb:
                    info="{0} copy".format(sf2)
                elif sf3 in valuea and sf3 in valueb:
                    info="{0} copy".format(sf3)
                else:
                    closeList.append("===\nvaluea:{0} [@{1}] \nvalueb:{2} [@{3}]\n".format(str(valuea),str(locationa),str(valueb),str(locationb)))
            else:
                info=""
                line_color=line_normalColor
            
            print("{0}{1}     * [delta:{2}, line:{3}/{5}] {4}*".format(line_color,line,str(locationa-locationb),str(count),str(info),str(f_lines-count)))
            locationb=locationa
            valueb=valuea
    count=count+1
	
end_time=time()-start_time

print("Took {0}s".format(str(end_time)))
showResults()
			
                
                
