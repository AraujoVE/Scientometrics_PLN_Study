import os
import networkx as nx
from node2vec import Node2Vec
from time import sleep

def node2Vec(graph,path):
    print("\tnode2vec start")
    node2vec = Node2Vec(graph, dimensions=128, walk_length=30, num_walks=200, workers=1)
    print("\tnode2vec fit start")
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print("\tnode2vec save start")
    model.wv.save_word2vec_format(path+".txt")
    return

def saveOccuranceArray(dir, corpus):
    occuranceGraph = nx.Graph()
    occuranceGraph.add_nodes_from(corpus)
    
    files = [dir+"/"+i for i in os.listdir(dir) if i.split('.')[-1] == 'txt']
    print(dir,", initialized")
    for file in files:
        print("\t",file,", initialized")
        with open(file, 'r') as f:
            words = f.read().strip().split()
            word2 = words[0] 
            for i in range(len(words)-1):
                word1 = word2
                word2 = words[i+1]
                occuranceGraph.add_edge(word1, word2)
    print("Pre node2vec")
    node2Vec(occuranceGraph,dir+"/node2vec")
    print("Post node2vec")
    with open("./Texts/embeddingsDone.csv","a") as f:
        f.write(dir.split('/')[-2]+",")

    return


def main():
    dirs = [i for i in os.listdir("./Texts") if os.path.isdir("./Texts/"+i)]
    corpus = [i for i in open('./Texts/corpusWords.csv', 'r', encoding='utf-8').read().strip().split(',')]
    embbededs = [i for i in open('./Texts/embeddingsDone.csv', 'r', encoding='utf-8').read().strip().strip(',').split(',')]
    for dir in dirs:
        if dir not in embbededs:
            print(dir,", initialized")
            saveOccuranceArray("./Texts/"+dir+"/Normalized", corpus)
            sleep(120)
        else:
            print(dir,", skipped")

    return
main()