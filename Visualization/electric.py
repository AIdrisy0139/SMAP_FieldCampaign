import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def excel(stepSize):
    '''
        Params:
            -stepSize: How many rows to be averaged (60 Rows ~~ 5 Minutes)


        -Obtain all .txt files from input files directory
        -Rename to .csv files
        -Load them using pd.readcsv
        -Open a new file to store the average values ("allAvgOut.csv")
        -Calculate Averages
        -Output into allAvgOut.csv
    '''
    print("excel")

    #Read in all the files in the ./inputfiles directory
    fileNames = os.listdir("./inputfiles")
    fileNames.sort()
    
    #Iterate through all the elements in fileNames renaming them from .txt to .csv
    for file in fileNames: 
        length = len(file)
        newFileName = file[:length-3]+"csv"
        path = "./inputfiles/"
        os.rename(path+file,path+newFileName)
    
    #Read in the new file names
    fileNames = os.listdir("./inputfiles")
    fileNames.sort()
    file = open("./output/allAvgOut.csv","w+")#w+ truncates file to 0 bytes and then writes
    
    #Iterate through all of the files,load  them, calculate the averages, and write to a new csv ("allAvgOut.csv")
    for name in fileNames:

        print(name)
        df = pd.read_csv("./inputfiles/"+name)
        orgData = df.values
        data = np.array([orgData.T[0],orgData.T[20],orgData.T[21]]).T #Makes a NP array of the 3 columns we need [Date,TskyV,TskyH]
        #data[0] : Datetime
        #data[1] : Tsky-V
        #data[2] : Tsky-H
        length = data.shape[0]
        for i in range(0,length,stepSize):#Get the first index in the nth substet
            tmpSumV=0
            tmpSumH=0
            for j in range(i,i+stepSize):#Calc Sum of the stepSize subset
                if j<length: #Because J can be higher than length in this loop
                    row = data[j]
                    tmpSumV+= row[1]
                    tmpSumH+=row[2]
            #Calc Average
            avgV = tmpSumV/stepSize
            avgH = tmpSumH/stepSize
            writeString = "{},{},{}\n".format(data[i][0],avgV,avgH)
            file.write(writeString)
    file.close()#Flushes the txt buffer and closes the file

def clean():
    '''
        Purpose: Remove outliers in the data

    '''
    print("clean")
    #TODO: How to identify Outliers?
    df = pd.read_csv("./output/allAvgOut.csv")
    data = df.values
    length = data.shape[0]

    #Removing Outliers
    cleanData = np.array([[0,0,0]])#For vStack to work
    for i in range(0,length):
        #Add the conditionals for outliers here
        # i = x value and data.T[X][i] is the y Value
        #Do notihing if you want to exclude the point, vstack it to cleanData if you want the points
        if(i<250):
            print("0del")
        if (data.T[1][i]>200 and (i>4000)):
            print("87")
        elif(data.T[1][i]>240 and (0<i<800)):
            print("89")
        elif (data.T[1][i]>150):
            cleanData = np.vstack((cleanData,data[i]))
    
    cleanData = np.delete(cleanData,0,axis=0)#Removes initial [0,0,0]
    
    pd.DataFrame(cleanData).to_csv("./output/cleanData.csv",header=None,index=None)



#Global Helper Variables to pass info between formatFunc and plot
counter = 0
numTick=[]
nameTick=[]
def formatFunc(value,tick_number):
    #README: https://jakevdp.github.io/PythonDataScienceHandbook/04.10-customizing-ticks.html
    #print("Format Function")
    global counter #index representing which quarter we're in?
    global numTick
    global nameTick
    intVal = int(value)
    #print("counter: {}, numTick: {}, nameTick: {}".format(counter,numTick,nameTick))
    if(counter<len(numTick)):#Ensure that index in range gets checked first
        if intVal == numTick[counter]:
            final = nameTick[counter]
            counter +=1
            return final
    #print(intVal)

def plot():
    '''
        -Load in allAvgOut.csv
        -Set up xticks to have 4 tick marks
        -Show the date at those ticks
    '''
    print("plot")
    df = pd.read_csv("./output/cleanData.csv")
    data = df.values
    length = data.shape[0]
    stepInt = int(length/4) #HOw many ticks you want
    #print(data.shape[0])
    
    #Generate tick Array from the data
    global nameTick
    tickArray=[]
    for i in range(0,length,stepInt): 
        tickArray.append(data[i][0].split(" ")[0])
    tickArray.append(data[length-1][0].split(" ")[0])
    print("Tick Arr : {}".format(tickArray))
    nameTick = tickArray 

    #Generate corresponding numerical values for the ticks
    global numTick
    tickNumArray = list(range(0,length,stepInt))
    tickNumArray.append(length)#Because range exlcudes the upper boound
    print(list(tickNumArray))
    numTick = tickNumArray
    
    #This is all the plotting code, most of it is self explanitory with reading the PLT documentation
    #Link that explains the formattor functions https://jakevdp.github.io/PythonDataScienceHandbook/04.10-customizing-ticks.html
    fig, ax = plt.subplots(figsize=(12,4.5))
    fig.suptitle("Canopy Brightness Temperature (Harvard Forest)")
    ax.set_ylabel("Brightness (K)")#plt.ylabel("Brightness (K)")
    ax.set_xlabel("Time")#plt.xlabel("Time")
    ax.xaxis.set_label_coords(.5,-.1)#Position label so it doesnt block xtickss
    ax.xaxis.set_major_locator(plt.MultipleLocator(stepInt )) 
    ax.xaxis.set_major_formatter(plt.FuncFormatter(formatFunc))

    ax.plot(np.arange(length),data.T[2]) #H
    ax.plot(np.arange(length),data.T[1])# V
    plt.legend(["Tsvk-H","Tsky-V"])
    #print((data[int(length/4)][0]).split(" ")[0] )
    print("counter: {}, numTick: {}, nameTick: {}".format(counter,numTick,nameTick))
    plt.show()
    #plt.savefig("figure.png")
    #FIXME: RESIZING ISSUE

excel(60)
clean()
plot()