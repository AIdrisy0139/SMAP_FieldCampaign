import pandas as pd
import os

def renameFiles():
    src = "./Sync/"
    dst = "./ProcData/"
    textFiles = os.listdir(src)
    
    for file in textFiles:
        print(file)
        length = len(file)
        newFileName = file[:length-3] +"csv"
        print(newFileName)
        os.rename(src+file,dst+newFileName)
renameFiles()