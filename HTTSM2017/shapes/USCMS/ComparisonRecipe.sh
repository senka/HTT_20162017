#!/bin/sh 
############################################################
##   usage : source ComparisonRecipe.sh outputname title  ##
############################################################

# Unrolling
python Unroll_2Drelaxed.py
# now prepare to run the limits:
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/bin
MorphingSM2017 --output_folder=${1} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false
# add MC stat uncertainties:                                                                                                                                   
sh _do_mc_Stat.sh  output/${1}
cd output/${1}
combineTool.py -M T2W -i {cmb,tt}/* -o workspace.root --parallel 18
cp ../../../scripts/texName.json .
cp ../../../scripts/plot1DScan.py .


# Run on mjj and save outputs with name "*_title"
combine -M MultiDimFit -m 125 --algo grid --points 101 --rMin 0 --rMax 2 cmb/125/workspace.root -n nominal_${2} -t -1 --expectSignal=1

