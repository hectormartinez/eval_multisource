
from lib.conll import CoNLLReader
from collections import Counter

def getPosDist(sents):
    C = Counter()
    for s in sents:
        for n in s.nodes()[1:]:
            C[s.node[n]["cpostag"]]+=1

    total = sum(C.values())
    for k in C.keys():
        C[k]/=total
    return C

rdr = CoNLLReader()
Acc = Counter()
langs = "ar bg cs da de en es eu fa fi fr he hi hr id it nl pl pt sl sv".split()
langs = langs[:3]
for lang in langs:
    filepattern="/Users/hector/data/parse-holy-data/parse/goldpos/"+lang+"-ud-train.conllu.delex"
    current_sentences = rdr.read_conll_u(filepattern)
    posdist = getPosDist(current_sentences)
    Acc = Acc + posdist

total = len(langs)
for k in Acc.keys():
    Acc[k]/=total
print(Acc)