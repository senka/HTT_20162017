#!/bin/bash
rm -rf ../../bin/output/*
mkdir ../../bin/output/combine
cp plot.sh ../../bin/output/combine/.

while [ -n "$1" ]; do # while loop starts
    case "$1" in
        -i)
            inputfolder="$2"
            echo "Input root files are in $2"
            shift
            ;;
        --)
            shift # The double dash which separates options from parameters
            break
            ;;
        *) echo "Option $1 not recognized : -fsa -sel -ch -ff -i" ;;
    esac
    shift
done

for i in `ls ${inputfolder}/*.root`; do
    export input="$iput $i"
    echo $input                                                                                                                                               
    fileName="${input%.*}"
    fileName="${fileName##*/}"
    cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes/USCMS
    source ComparisonRecipe.sh ${inputfolder}/${fileName}.root ${fileName} tt    
    cd ../combine
    mkdir ${fileName}
    #cp ../${fileName}/higgsCombinerun_muF_fixed_muV.MultiDimFit.mH125.root ${fileName}/muF.root
    cp ../${fileName}/higgsCombinerun_muV_fixed_muF.MultiDimFit.mH125.root ${fileName}/muV.root
    cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes/USCMS
    python stackPlotter_dev.py -i htt_tt.inputs-sm-13TeV-2D.root -v unroll -c tt -f -n 2016 -t ${fileName}
done
cd -
cd ../combine
cp ../../../scripts/texName.json .
cp ../../../scripts/plot1DScan.py .

