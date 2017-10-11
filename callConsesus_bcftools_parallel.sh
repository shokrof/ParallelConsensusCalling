
if [[ $1 == '--h' ]]
then
    echo "./callConsesus_bcftools_parallel.sh  <input fasta file> <vcf file> <no of threads> <output fasta file>"
    echo "works with bcftools 1.3 and samtools 1.3 and parallel gnu"
    exit
fi

ref=$1
vcf=$2
no_threads=$3
out_ref=$4



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
tmpfile2=$(mktemp /tmp/callConsesus_bcftools.XXXXXX)

python divideVcf.py <(bgzip -dc $vcf) $no_threads $tmpfile2

cat $tmpfile2 | parallel --gnu -k "samtools faidx $ref  {} |  ~/tools/bcftools-1.3/bcftools consensus $vcf" | python concatRes.py > $out_ref


 

####Clean#####
##############
rm  -f $tmpfile $tmpfile2

