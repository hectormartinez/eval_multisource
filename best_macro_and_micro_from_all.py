
import os
scorefile="scores-delex-svm_mira.all"
import random
from collections import Counter
from decimal import *



train_langsizes=dict([x.strip().split("\t") for x in open("train_file_sentence_size.tsv").readlines()])


langs = "ar bg cs da de el en es et eu fa fi fr he hi hr hu id it la nl no pl pt qu ro sl sr sv ta".split()

trainlangs = "ar bg cs da de en es eu fa fi fr he hi hr id it nl pl pt sl sv".split(" ")
testlangs = "el et hu la qu ro sr ta".split(" ")

langs = trainlangs + testlangs

M = {}
for li in langs:
    M[li]={}
    for lj in langs:
        M[li][lj]=0

print(M) # M[train][test]

M = Counter()

#for line in open(scorefile).readlines()[1:]:

for langline,evaline in zip(os.popen("grep predict "+scorefile),os.popen("grep attachment "+scorefile)):
    langline = langline.strip().split(" ")
    evaline = evaline.strip().split(" ")
    ulas = float(evaline[9])
    test_lang = langline[0]
    train_lang = langline[1].split("/")[3].split(".")[3].replace("-ud-train","")
    M[(train_lang,test_lang)]=ulas


bestdict = {}
macrodict = {}

micro_acc = []
macro_acc = []
best_acc = []
micro_acc_test = []
macro_acc_test = []
best_acc_test = []



for test_lang in langs:
    current_test_list = []
    source_lang_names = []
    weights_for_source_langs = []
    for train_lang in langs:
        if test_lang != train_lang and train_lang in train_langsizes:
            current_test_list.append(M[train_lang,test_lang])
            source_lang_names.append(train_lang)
            weights_for_source_langs.append(float(train_langsizes[train_lang]))

    best_delex_uas = max(current_test_list)
    idx_best_delex = current_test_list.index(best_delex_uas)
    best_source_lang = source_lang_names[idx_best_delex]
    macro_avg_uas = sum(current_test_list)/(len(langs) -1)
    micro_avg_uas = sum([sentences*uas for sentences,uas in zip(weights_for_source_langs,current_test_list)]) / sum(weights_for_source_langs)

    best_acc.append(best_delex_uas)
    macro_acc.append(macro_avg_uas)
    micro_acc.append(micro_avg_uas)

    if test_lang not in train_langsizes:
        best_acc_test.append(best_delex_uas)
        macro_acc_test.append(macro_avg_uas)
        micro_acc_test.append(micro_avg_uas)

    print(test_lang,"&",round(best_delex_uas,2),best_source_lang,"&",round(macro_avg_uas,2),"&",round(micro_avg_uas,2),"\\\\")

print("all languages","&",round(sum(best_acc)/len(best_acc),2),"&",round(sum(macro_acc)/len(macro_acc),2),"&",round(sum(micro_acc)/len(micro_acc),2),"\\\\")
print("only test languages","&",round(sum(best_acc_test)/len(best_acc_test),2),"&",round(sum(macro_acc_test)/len(macro_acc_test),2),"&",round(sum(micro_acc_test)/len(micro_acc_test),2),"\\\\")
