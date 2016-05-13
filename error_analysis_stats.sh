

echo "proj_pred proj_gold punctproj_pred punctproj_gold leaf_viol_pred leaf_viol_gold PosKLPred POSKLGold posAcc UAS"

for lang in ar bg cs da de en es eu fa fi fr he hi hr id it pl pt sl sv el et hu la qu ro sr
do
python treebank_stats.py --lang $lang --predicted ~/data/parse-holy-data/predicted/projpredpos/voted/$lang-ud-test.bible.pppos.ibm1.conll.$lang.corpus_bible.aligner_ibm1.trees_0.binary_0.similarity_0.unitvote_1.vote.model.out --gold ~/data/parse-holy-data/parse/goldpos/$lang-ud-test.conllu.delex
done


echo "proj_pred proj_gold punctproj_pred punctproj_gold leaf_viol_pred leaf_viol_gold PosKLPred POSKLGold posAcc UAS"

for lang in ar bg cs da de en es fa fi fr he hi hr id it nl pl pt sl sv el et hu qu ro ta
do
python treebank_stats.py --lang $lang --predicted ~/data/parse-holy-data/predicted/projpredpos/voted/$lang-ud-test.watchtower.pppos.ibm1.conll.$lang.corpus_watchtower.aligner_ibm1.trees_0.binary_0.similarity_0.unitvote_1.vote.model.out --gold ~/data/parse-holy-data/parse/goldpos/$lang-ud-test.conllu.delex
done
