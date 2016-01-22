import os
import unicodedata as ud
unicodefile="unicode.txt"
for punctname in ["'FULL STOP'","QUESTION","EXCLAMATION"]:
    for line in list(os.popen("grep "+punctname+" "+unicodefile)):
        nameparts = line.split(";")
        name=nameparts[1]
        type=nameparts[2]
        if type.startswith("P"):
            try:
                print(name+"\t"+ud.lookup(name))
            except:
                pass