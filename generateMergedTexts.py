import os
import Normalization.textNormalization as tn



'''
Merge the texts of the sub-areas into main areas
'''

def joinTexts(readPath,writePath):
    texts = [i for i in os.listdir(readPath) if i.split(".")[-1] == "txt"]

    with open(writePath, "w") as f:
        for text in texts:
            with open(readPath + "/" + text, "r") as t:
                f.write(t.read())
    

def main():
    mainAreas = [i for i in os.listdir("./Texts") if os.path.isdir("./Texts/" + i)]
    generalTexts = "./Normalization/GeneralTexts"
    os.mkdir(generalTexts)
    for area in mainAreas:
        joinTexts("./Texts/"+area,generalTexts+"/"+area+".txt")
    tn.normalizeDirFiles(generalTexts)
main()