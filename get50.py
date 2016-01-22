

C=56
c=0

import argparse
parser = argparse.ArgumentParser(description="get 50 sentences, then die")
parser.add_argument('--infile', help="parsed-and-label input format")
args = parser.parse_args()

import sys
for line in open(args.infile).readlines():
    line=line.strip()
    if line:
        line = line.split("\t")
        line = "\t".join(line[:8])+"\t_\t_"
        print(line)
    else:
        print()
        c+=1
    if c >= C:
        sys.exit()
