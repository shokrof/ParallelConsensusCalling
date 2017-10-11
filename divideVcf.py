import sys,re

MAX_SEQ=10000000

def intersects(point,startRange,endRange):
    return (point>=startRange and point<=endRange)

def main(arg):
    vcfFilename=arg[0]
    noChunks=int(arg[1])
    outRegionsFilename=arg[2]
    
    inputVcf=open(vcfFilename,'r')

    
    contigsLen=[]
    totalLength=0
    l=inputVcf.readline() 
    while l[0]=='#':
        check=re.match('##contig=<ID=([^,]*),length=([0-9]*)>',l.strip())
        if check:
            ctg,length=check.groups()
            contigsLen.append([ctg,int(length)])
            totalLength+=int(length)
        l=inputVcf.readline()
    
    if totalLength%noChunks==0:
        chunkLength=int(float(totalLength)/float(noChunks))
    else:
        chunkLength=int(float(totalLength)/float(noChunks-1))

    chunks=[]
    i=0
    pos=0
    while i< len(contigsLen):
        if pos+chunkLength <= contigsLen[i][1]:
            chunks.append([contigsLen[i][0],pos,pos+chunkLength])
            pos+=chunkLength+1
        else:
            if pos<contigsLen[i][1]:
                chunks.append([contigsLen[i][0],pos,contigsLen[i][1]])
            pos=0
            i+=1

    start=0
    end=0
    prevChrom=''
    i=0
    for line in inputVcf:
        line=line.strip().split('\t')
        chrom,pos,ref=line[0],int(line[1]),line[3]
        currend=pos+len(ref)+1
        while  i < len(chunks) :
            rightChunk= chrom == chunks[i][0]
            rightChunk&=intersects(pos,chunks[i][1],chunks[i][2])
            
            c=chunks[i]
            if rightChunk:
                break
#            print("chunk is %s:%d-%d and v(%d,%d) right= %d"%(c[0],c[1],c[2],pos,currend,rightChunk))
            i+=1
        if i<len(chunks)-1 and  intersects( chunks[i][2
] , pos ,currend):
            chunks[i][2]=currend+1
            chunks[i+1][1]=currend+2
 
        #  if end-start > MAX_SEQ or chrom!=prevChrom:
        #     if prevChrom =='':
        #         start=end
        #     elif prevChrom==chrom:
        #         outputList.write("%s:%d-%d\n"%(prevChrom,start,end))
        #         start=end
        #     elif prevChrom !=chrom:
        #         outputList.write("%s:%d-%d\n"%(prevChrom,start,contigsLen[chrom]))
        #         start=0
 
        #     prevChrom=chrom
        #     end=currend
        # else:
        #     end=currend
        #    outputList.write("%s:%d-%d\n"%(prevChrom,start,contigsLen[chrom]))

        with open(outRegionsFilename,'w') as outputList:
            for c in chunks:
                outputList.write("%s:%d-%d\n"%(c[0],c[1],c[2]))


        
    


if __name__ == '__main__':
    main(sys.argv[1:])
