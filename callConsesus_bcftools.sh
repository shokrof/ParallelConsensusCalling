
if [[ $1 == '--h' ]]
then
    echo "./callConsesus_bcftools.sh  <input fasta file> <vcf file> <output fasta file>"
    echo "works with bcftools 1.3 and samtools 1.3"
    exit
fi

ref=$1
vcf=$2
out_ref=$3



###Prepare###
#############

clean=false
if [[ ${vcf: -3} != ".gz" ]]
then
    tmpfile=$(mktemp /tmp/callConsesus_bcftools.XXXXXX.vcf.gz)
    bgzip -c $vcf > $tmpfile
    vcf=$tmpfile
    clean=true
fi
if [ ! -f $vcf.tbi ]; then
    tabix $vcf
fi


###Command####
##############
cat $ref | bcftools consensus $vcf > $out_ref
 

if [[ clean ]]
then
    rm  -f $tmpfile
fi
