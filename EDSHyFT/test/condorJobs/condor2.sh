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
	for option in "--pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_nominal" \
                      "--pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --noMET --addDirs --outname $OUTPATH/${dir}_noMETCut" \
		      "--pileupReweight up --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_PUup" \
		      "--pileupReweight down --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_PUdown" \
		      "--btagSys up --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_Btag110" \
		      "--btagSys down --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_Btag090" \
                      "--btagSys up2 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_Btag120" \
                      "--btagSys down2 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_Btag080" \
                      "--lftagSys up --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_LFtag110" \
                      "--lftagSys down --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_LFtag090" \
                      "--lftagSys up2 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_LFtag120" \
                      "--lftagSys down2 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_LFtag080" \
              "--metSys up --jetSmear=0.0 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_METRES110" \
		      "--metSys down --jetSmear=0.0 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_METRES090" \
		      "--jecSys up --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_JESup" \
		      "--jecSys down --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_JESdown" \
                      "--jetSmear 0.0 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_JER000" \
		      "--jetSmear 0.2 --pileupReweight nominal --PUWeights 3DEleHad --minJets 3 --jetPt 35.0 --addDirs --outname $OUTPATH/${dir}_JER020"; do
	    if test $counter -eq $PROCESS; then
		echo "python shyft_fwlite.py --lepType $LEPTYPE --files $INPATH/$dir/res/shyftDump_\*.root $option"
		python shyft_fwlite.py --lepType $LEPTYPE --files $INPATH/$dir/res/shyftDump_\*.root $option
	    fi
	    let "counter+=1"
	done
	else
	    if test $counter -eq $PROCESS; then
		echo "python shyft_fwlite.py --lepType $LEPTYPE --useData 1 --minJets 3 --jetPt 35.0 --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_nominal"
		python shyft_fwlite.py --lepType $LEPTYPE --useData 1 --minJets 3 --jetPt 35.0 --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_nominal
                echo "python shyft_fwlite.py --lepType $LEPTYPE --useData 1 --minJets 3 --jetPt 35.0 --noMET --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_noMETCut"
                python shyft_fwlite.py --lepType $LEPTYPE --useData 1 --minJets 3 --jetPt 35.0 --noMET --addDirs --files $INPATH/$dir/res/shyftDump_\*.root --outname $OUTPATH/${dir}_noMETCut
	    fi
	    let "counter+=1"
	fi
	
    fi
done
