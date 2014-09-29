#!/bin/bash

echo "input parameters: cluster, process, run path, input path, output path, data?, leptype " $1 $2 $3 $4 $5 $6

CLUSTER=$1
PROCESS=$2
RUNPATH=$3
INPATH=$4
OUTPATH=$5 
DATA=$6
LEPTYPE=1

cd $RUNPATH
source /uscmst1/prod/sw/cms/shrc uaf
eval `scramv1 runtime -sh`

counter=0

for dir in `ls $INPATH`; do
    echo "going here: "$dir
    if test -d $INPATH/$dir/res; then
	echo "directory   $INPATH/$dir/res   exists"
	if test $DATA -eq 0; then
    for option in "--metSys up --jetSmear 0.0 --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_METRES110" \
		      "--metSys down --jetSmear 0.0  --pileupReweight nominal --addDirs --outname $OUTPATH/${dir}_METRES090"; do
	    if test $counter -eq $PROCESS; then
		echo "python shyft_fwlite.py --lepType $LEPTYPE --files $INPATH/$dir/res/shyftDump_\*.root $option"
		python shyft_fwlite.py --lepType $LEPTYPE --files $INPATH/$dir/res/shyftDump_\*.root $option
	    fi
	    let "counter+=1"
	done
	else
	    if test $counter -eq $PROCESS; then
		echo "python shyft_fwlite.py --lepType $LEPTYPE --useData 1  --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_nominal"
		python shyft_fwlite.py --lepType $LEPTYPE --useData 1  --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_nominal
                echo "python shyft_fwlite.py --lepType $LEPTYPE --useData 1  --noMET --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_noMETCut"
                python shyft_fwlite.py --lepType $LEPTYPE --useData 1  --noMET --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_noMETCut
	    fi
	    let "counter+=1"
	fi
	
    fi
done
