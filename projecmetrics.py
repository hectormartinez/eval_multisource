from lib.conll import CoNLLReader
import argparse
import networkx as nx
from collections import Counter
import numpy as np
from scipy.stats import entropy
from decimal import *
getcontext().prec = 2

def POSAcc(system_s,gold_s):
    acc = 0
    for nidx in gold_s.nodes()[1:]:
        if system_s.node[nidx]["cpostag"] == gold_s.node[nidx]["cpostag"]:
            acc+=1
    return acc


def edgelengths(sentences):
    lengths = []
    for s in sentences:
        for h,d in s.edges():
            lengths.append(abs(h-d))
    return np.array(lengths)



def UAS(system_s,gold_s):
    return len(set(system_s.edges()).intersection(set(gold_s.edges())))


def wrongPOSgoodHead(predicted_sentences, gold_sentences):
    countgoodhead = 0
    countbadpos = 0
    for s,g in zip(predicted_sentences,gold_sentences):
        for n in s.nodes():
            if n != 0:
                try:
                    if g.node[n]["cpostag"] == s.node[n]["cpostag"]: #!= g.node[n]["cpostag"]:
                        countbadpos+=1
                        if s.head_of(n) != g.head_of(n):
                            countgoodhead+=1
                except:
                    pass
    return countgoodhead / countbadpos


def KLdivFromMACRO_POS_from_Training(sents):
    MacroPOsDist=Counter({'NOUN': 0.2637511016542025, 'ADP': 0.1295411345716877, 'PUNCT': 0.12057483791479968, 'VERB': 0.10416704856859009, 'ADJ': 0.10366326097738032, 'PRON': 0.053725080252980555, 'CONJ': 0.05107121395420389, 'PROPN': 0.039729567468023315, 'ADV': 0.03287340016104059, 'X': 0.026019326609917365, 'NUM': 0.021924172500282422, 'PART': 0.0171283774675168, 'DET': 0.013278021211586602, 'SCONJ': 0.00962250165799281, 'AUX': 0.008996545864941845, 'INTJ': 0.003261950965451286, 'SYM': 0.0006724581994021862})
    C = Counter()
    for k in MacroPOsDist.keys():
        C[k]=1
    for s in sents:
        for n in s.nodes()[1:]:
            C[s.node[n]["cpostag"]]+=1



    total = sum(C.values())
    for k in C.keys():
        C[k]/=total

    trainmacro=[]
    testdist=[]
    for k in MacroPOsDist.keys():
        testdist.append(C[k])
        trainmacro.append(MacroPOsDist[k])
    trainmacro = np.array(trainmacro)
    testdist = np.array(testdist)
    return entropy(trainmacro,testdist)

def main():
    parser = argparse.ArgumentParser(description="""Convert conllu to conll format""")
    parser.add_argument('--infile', help="conllu file")
    parser.add_argument('--lang', help="")

    args = parser.parse_args()

    #try:

    header = ["proj_pred", "proj_gold", "leaf_viol_pred", "leaf_viol_gold", "posAcc", "UAS"]

    if True:
        vals = []
        rdr = CoNLLReader()
        predicted_sentences = []
        gold_sentences = []

        if args.infile:
            gold_sentences = rdr.read_conll_u_8cols(args.infile)


        numwords = sum([len(s.nodes()[1:]) for s in predicted_sentences])
        #print([int(s.is_fully_projective()) for s in predicted_sentences])

        for idx,s in enumerate(gold_sentences):
            print(idx,s.is_fully_projective())



if __name__ == "__main__":
    main()