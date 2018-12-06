#!/bin/sh 
#########################################################################################
##   usage : source ComparisonRecipe.sh inputfile foldername channel tag -s(or empty)  ##
##           source ComparisonRecipe.sh final_nomianl.root TestOct19 tt mjj            ##
##           source ComparisonRecipe.sh htt_input.root TestOct19 tt mjj --svn          ##
#########################################################################################

# Unrolling
if [ -z ${5} ]; then
    python Unroll_2Drelaxed.py ${1} ${3} 
else
    python Unroll_2Drelaxed.py ${1} ${3} ${5}
fi


# now prepare to run the limits:
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/bin
#MorphingSM2017 --output_folder=${2} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false
MorphingSM2017_dataDriven --output_folder=${2} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true --shape_systematics=false --jetfakes=true
# add MC stat uncertainties:                                                                                                                                   
sh _do_mc_Stat.sh  output/${2}
cd output/${2}

# Make workspace
combineTool.py -M T2W -i {cmb,${3}}/* -o workspace.root --parallel 18
combineTool.py -M T2W -i ${3}/125/htt_${3}_3_13TeV.txt -o workspace_${3}_vbf.root --parallel 18
combineTool.py -M T2W -i ${3}/125/htt_${3}_2_13TeV.txt -o workspace_${3}_boosted.root --parallel 18
combineTool.py -M T2W -i ${3}/125/htt_${3}_1_13TeV.txt -o workspace_${3}_0jet.root --parallel 18
combineTool.py -M T2W -m 125 -P CombineHarvester.HTTSM2017.muVmuF:muVmuF -i ${3}/125/combined.txt.cmb -o muVmuF_Workspace_${3}.root

cp ../../../scripts/texName.json .
cp ../../../scripts/plot1DScan.py .


# Run on mjj and save outputs with name "*_title"
combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 3 ${3}/125/workspace.root -n inclusive -t -1 --expectSignal=1 
combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 3 ${3}/125/workspace_${3}_vbf.root -n vbf -t -1 --expectSignal=1 
combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 3 ${3}/125/workspace_${3}_boosted.root -n boosted -t -1 --expectSignal=1 
combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 3 ${3}/125/workspace_${3}_0jet.root -n 0jet -t -1 --expectSignal=1 


#combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muf --floatOtherPOIs=0 -M MultiDimFit -m 125 --points 51 -n run_muF_fixed_muV
#combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muV --floatOtherPOIs=0 -M MultiDimFit -m 125 --points 51 -n run_muV_fixed_muF