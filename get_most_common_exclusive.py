
from collections import Counter
biblefile="clean/bible/sv.s"
watchfile="clean/watchtower/sv.s"


b = []
w = []

def getwords(tuplelist):
    return ", ".join([x for x,y in tuplelist])

for l in open(biblefile).readlines():
    l=l.strip().lower()
    b.extend(l.split(" "))

for l in open(watchfile).readlines():
    l=l.strip().lower()
    w.extend(l.split(" "))


b_and_w = set(b).intersection(set(w))
#print([x for x in b if x not in b_and_w])
B = Counter([x for x in b if x not in b_and_w])
W = Counter([x for x in w if x not in b_and_w])
print(getwords(B.most_common()[:40]))
print(getwords(W.most_common()[:50]))

