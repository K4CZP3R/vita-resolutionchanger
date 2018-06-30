from colorama import init, Fore, Back
import os
import time


class Debug:
    def __init__(self):
        init(autoreset=True)
    def print(self,content,color=Fore.GREEN):
        color_0=Fore.RED
        color_1=Fore.GREEN
        date_2=time.strftime('%x %X')
        color_3=color_0
        color_4=color
        text_5=str(content)

        print("{0}[{1}{2}{3}] {4}{5}".format(color_0,color_1,date_2,color_3,color_4,text_5))
    def ask(self,question):
        init(autoreset=True)
        question_0=str(question)
        tmp=input("[?] {0}: ".format(question_0))
        return tmp
    def printError(self,error):
        color_0=Fore.RED
        color_1=Fore.GREEN
        date_2=time.strftime('%x %X')
        color_3=color_0
        color_4=Fore.RED
        text_5=str(error)

        print("ERROR: {0}[{1}{2}{3}] {4}{5}".format(color_0,color_1,date_2,color_3,color_4,text_5))
        input("Press enter to continue...")
    def letWait(self):
        input("Press enter to continue")
    def clearScreen(self):
        x=os.system("cls")
        #x=os.system("clear")