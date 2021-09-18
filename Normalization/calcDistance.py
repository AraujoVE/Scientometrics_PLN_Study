import os
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def getEmbedding(path,keyStr):
    with open(path,"r") as f:
        lines = f.readlines()[1:]
    keyStrEmb = {}
    for line in lines:
        splittedLine = line.strip().split()
        if splittedLine[0] in keyStr:
            keyStrEmb[splittedLine[0]] = np.array(splittedLine[1:],dtype=np.float)
    
    return np.array([keyStrEmb[keyStr[i]] for i in range(len(keyStr))])

def reducedCossineSim(emb,keyStrs):
    cosSim = np.array(cosine_similarity(emb))
    redCosSim = []
    for i in range(len(keyStrs) - 1):
        for j in range(i + 1, len(keyStrs)):
            redCosSim.append(cosSim[i,j])

    return np.array(redCosSim)

def getSimilarityEmbedding(path,keyStrs):
    emb = getEmbedding(path,keyStrs)
    return reducedCossineSim(emb,keyStrs)

def showAndSaveData(emb,keyStrPairs,dirs):
    barNames = dirs
    y_pos = np.arange(len(barNames))
    heights = [[emb[dirs[j]][i] for j in range(len(dirs))] for i in range(len(keyStrPairs))]

    for i in range(len(keyStrPairs)):
        fig, ax = plt.subplots()
        # Create bars
        ax.bar(y_pos, heights[i])

        # Create names on the x-axis
        plt.xticks(y_pos, barNames)

        # Show graphic
        fig.savefig("./figs/img_"+str(keyStrPairs[i])+".png")
        plt.close(fig)




def main():
    keyStrsDistanceEmbeddings = {}
    keyStrs = [i for i in open("./ChoosenStrs/Normalized/specialStrs.txt","r").read().strip().split()]
    keyStrPairs = []
    for i in range(len(keyStrs)-1):
        for j in range(i+1,len(keyStrs)):
            keyStrPairs.append(keyStrs[i]+"-"+keyStrs[j])
    
    dirs = [i for i in os.listdir("./Texts") if os.path.isdir("./Texts/"+i)]

    for i in range(len(dirs)):
        keyStrsDistanceEmbeddings[dirs[i]] = getSimilarityEmbedding("./Texts/"+dirs[i]+"/Normalized/node2vec.txt",keyStrs)
        break
    
    showAndSaveData(keyStrsDistanceEmbeddings,keyStrPairs,dirs)




main()