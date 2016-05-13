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
    parser.add_argument('--predicted', help="conllu file")
    parser.add_argument('--gold', help="conllu file")
    parser.add_argument('--lang', help="")

    args = parser.parse_args()

    #try:

    header = ["proj_pred", "proj_gold", "leaf_viol_pred", "leaf_viol_gold", "posAcc", "UAS"]

    if True:
        vals = []
        rdr = CoNLLReader()
        predicted_sentences = []
        gold_sentences = []

        if args.predicted:
            predicted_sentences = rdr.read_conll_u_8cols(args.predicted)

        if args.gold:
            gold_sentences = rdr.read_conll_u(args.gold)


        numwords = sum([len(s.nodes()[1:]) for s in predicted_sentences])
        #print([int(s.is_fully_projective()) for s in predicted_sentences])
        proj_pred=sum([int(s.is_fully_projective()) for s in predicted_sentences])
        proj_gold=sum([int(s.is_fully_projective()) for s in gold_sentences])
        punct_non__proj_pred=sum([int(s.punct_proj_violations()) for s in predicted_sentences])
        punct_non__proj_gold=sum([int(s.punct_proj_violations()) for s in gold_sentences])


        leaf_violations_pred=sum([s.leaf_violations()[0] for s in predicted_sentences])
        leaf_violations_gold=sum([s.leaf_violations()[0] for s in gold_sentences])
        wrongPOSgoodHeadscore = wrongPOSgoodHead(predicted_sentences,gold_sentences)
        posAcc_accum=sum([POSAcc(p,g) for p,g in zip(predicted_sentences,gold_sentences)]) / numwords
        UAS_accum=sum([UAS(p,g) for p,g in zip(predicted_sentences,gold_sentences)]) / numwords
        prelength=edgelengths(predicted_sentences)
        goldlength=edgelengths(gold_sentences)
        avgprelength = np.std(prelength)
        avggoldlength = np.std(goldlength)

        vals.append(wrongPOSgoodHeadscore)
        vals.append(avgprelength)
        vals.append(avggoldlength)
        vals.append(proj_pred / len(predicted_sentences))
        vals.append(proj_pred / len(predicted_sentences))
        vals.append(proj_gold /  len(gold_sentences))
        vals.append(punct_non__proj_pred / numwords)
        vals.append(punct_non__proj_gold / numwords)
        vals.append(leaf_violations_pred/numwords)
        vals.append(leaf_violations_gold/numwords)
        vals.append(KLdivFromMACRO_POS_from_Training(predicted_sentences))
        vals.append(KLdivFromMACRO_POS_from_Training(gold_sentences))
        vals.append(posAcc_accum)
        vals.append(UAS_accum)
        lineout = " ".join([args.lang]+["{0:.2f}".format(x) for x in vals])
    #except:
    #    lineout = "_\t_"
    print(lineout)

if __name__ == "__main__":
    main()