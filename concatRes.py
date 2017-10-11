import sys


header=sys.stdin.readline().strip()
seq=sys.stdin.readline().strip()
lineLen=len(seq)

curRef=header[1:].split(":")[0]
print(">%s"%curRef)
print(seq)

seqReminder=''
for l in sys.stdin:
    if l[0]=='>':
        tmpref=l[1:].split(":")[0]
        if tmpref!=curRef:
            if seqReminder !='':
                print(seqReminder)
            curRef=tmpref
            print(">%s"%curRef)
    else:
        seqReminder+=l.strip()
        if len(seqReminder)>=lineLen:
            print(seqReminder[:lineLen])
            seqReminder=seqReminder[lineLen:]
if seqReminder!='':
    print(seqReminder)
