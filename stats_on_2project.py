from lib.conll import CoNLLReader
import argparse
import networkx as nx
from collections import Counter
import numpy as np
from scipy.stats import entropy
from decimal import *
getcontext().prec = 2

POSLIST = "ADJ ADP ADV AUX CONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".split(" ")
EDGELENGTHS = [2,3,4,5,6,7,8,9,10]


def main():
    parser = argparse.ArgumentParser(description="""Convert conllu to conll format""")
    parser.add_argument('--infile', help="conllu file", default="/Users/hmartine/proj/eval_multisource/data/2project/watchtower/en.2proj.conll.head1000")

    args = parser.parse_args()

    #try:

    DEPCHILDCOUNTER=Counter()
    GAPDEGREECOUNTER=Counter()
    PROJCOUNTER=Counter()

    header = ["proj_pred", "proj_gold", "leaf_viol_pred", "leaf_viol_gold", "posAcc", "UAS"]
    vals = []
    rdr = CoNLLReader()
    predicted_sentences = []
    gold_sentences = []

    if args.infile:
        gold_sentences = rdr.read_conll_2006_dense(args.infile)

    numwords = sum([len(s.nodes()[1:]) for s in predicted_sentences])
    #print([int(s.is_fully_projective()) for s in predicted_sentences])

    for idx,s in enumerate(gold_sentences):

        local_isproj = s.is_fully_projective()
        localdependentcounter,gapdegreecounter = s.non_projectivity_edge_info()
        PROJCOUNTER.update([local_isproj])
        DEPCHILDCOUNTER+=localdependentcounter
        GAPDEGREECOUNTER+=gapdegreecounter

    projpercent=round(PROJCOUNTER[True]/sum(PROJCOUNTER.values()),2)
    deppercent=[round(DEPCHILDCOUNTER[posname]/sum(DEPCHILDCOUNTER.values()),2) for posname in POSLIST]
    edgelenths = [round(GAPDEGREECOUNTER[l]/sum(GAPDEGREECOUNTER.values()),2) for l in EDGELENGTHS]
    otherlength = round(sum([GAPDEGREECOUNTER[l]/sum(GAPDEGREECOUNTER.values()) for l in GAPDEGREECOUNTER.keys() if l not in EDGELENGTHS]),2)
    #print(Counter(PROJLIST),DEPCHILDCOUNTER.most_common(),GAPDEGREECOUNTER.most_common())
    print("\t".join([str(x) for x in ["",projpercent]+deppercent+edgelenths+[otherlength]]))


if __name__ == "__main__":
    main()