import textNormalization as tn
import os

'''
Program to normalize all files of all areas and sub-areas and also save the full corpus of texts
'''


def addToCorpus(dir, corpusWords):
    files = [dir+"/"+i for i in os.listdir(dir) if i.split('.')[-1] == 'txt']
    for file in files:
        with open(file, 'r') as f:
            text = f.read()
            words = text.split()
            for word in words:
                if word not in corpusWords:
                    corpusWords.append(word)

    return corpusWords


def writeCorpusWords(dir, corpusWords):
    with open(dir+"/corpusWords.csv", 'w') as f:
        text = ",".join(corpusWords)
        f.write(text)


def main():
    os.system("rm -r ./Texts")
    os.system("cp -r ../Texts ./Texts")
    dirs = [i for i in os.listdir("./Texts") if os.path.isdir("./Texts/"+i)]
    
    corpusWords = []
    for dir in dirs:
        print(dir)
        tn.normalizeDirFiles("./Texts/"+dir)
        print("Normalized")
        corpusWords = addToCorpus("./Texts/"+dir+"/Normalized", corpusWords)
    
    print(len(corpusWords))
    writeCorpusWords("./Texts",corpusWords)
    print("Corpus Words Written")

main()