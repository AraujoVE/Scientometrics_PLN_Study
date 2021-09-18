import numpy as np
import matplotlib.pyplot as plt
from pca import pca
import pltColorMarker
import os

def createArray(path,keyStrs):
    strsQtty = {}
    arrayKeys = np.zeros(len(keyStrs)**2).reshape((len(keyStrs),len(keyStrs))) 
    
    with open(path, 'r') as f:
        text = f.read()
    textSize = len(text.split())
    for str in keyStrs:
        strsQtty[str] = text.count(str)#/textSize
    for i in range(len(keyStrs)):
        for j in range(len(keyStrs)):
            arrayKeys[i,j] = min(strsQtty[keyStrs[i]],strsQtty[keyStrs[j]])

    return arrayKeys

def getKeyStrs(path):
    with open(path) as f:
        keyStrs = f.read().split()
    return keyStrs


# i//(arrayLen+1) = 0 + 1
# i%(arrayLen+1) = 1
# i%(arrayLen+1) = 2
# i%(arrayLen+1) = 3


def padronizeToPca(array):
    arrayLen = len(array)
    newArray = np.zeros((arrayLen)*(arrayLen-1))
    for i in range(arrayLen):
        for j in range(arrayLen):
            if i != j:
                vecPos = i*arrayLen + j
                vecPos -= vecPos//(arrayLen+1) + 1
                newArray[vecPos] = array[i,j]
    return newArray

#9*0 + 1 - 1 = 0
#9*1 + 2 - 1 = 10
#9*2 + 3 - 1 = 20
#9*3 + 4 - 1 = 30

'''

'''

def plotPoints(pcaArray,arrayNames):
    fig, ax = plt.subplots()

    for i in range(len(arrayNames)):
        ax.scatter(pcaArray[i,0], pcaArray[i,1], c=pltColorMarker.getColor(i), marker=pltColorMarker.getMarker(i), label=arrayNames[i])
    ax.legend()
    plt.show()

def main(textsDirPath, keysPath):
    keyStrs = getKeyStrs(keysPath)
    textFilesNames = os.listdir(textsDirPath)
    arrayKeys = []
    arrayNames = []
    for textPath in textFilesNames:
        arrayNames.append(textPath.split('.')[0])
        arrayKeys.append(padronizeToPca(createArray(textsDirPath+'/'+textPath, keyStrs)))
    arrayKeys = np.asarray(arrayKeys)
    pcaArray = pca(arrayKeys)
    plotPoints(pcaArray, arrayNames)


main('./Texts/Normalized','./ChoosenStrs/Normalized/specialStrs.txt')

#a = np.asarray([[64.0,580.0,29.0],[66.0,570.0,33.0],[68.0,590.0,37.0],[69.0,660.0,46.0],[73.0,600.0,55.0]])