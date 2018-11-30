# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This pacakge requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development). The CombineHarvester framework is  compatible with the CMSSW 7_4_X and 8_1_X series releases.

A new full release area can be set up and compiled in the following steps:

    export SCRAM_ARCH=slc6_amd64_gcc530
    scram project CMSSW CMSSW_8_1_0
    cd CMSSW_8_1_0/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git clone git@github.com:KState-HEP-HTT/CombineHarvester.git CombineHarvester
    scram b


Now run the limits:

unroll 2D histos into 1D unrolled histos (input file: "final_nominal.root", output file: "htt_tt.inputs-sm-13TeV-2D.root" used as input for the limits!)

    cd CombineHarvester/HTTSM2017/shapes/USCMS/
    python Unroll_2Drelaxed.py inputfile channel (--svn)

now prepare to run the limits:
    
    cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/bin

read in all used histos and uncertainties and make root and txt datacards:
    
    MorphingSM2017 --output_folder="TestJune26" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false
    
for FF+embedded w/o shape systematics:

    MorphingSM2017_dataDriven --output_folder="TestJune26" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true --shape_systematics=false --jetfakes=true

(naming convention:"embedded","JetFakes" for tt and "jetFakes" for mt/et)

add MC stat uncertainties:
    
    sh _do_mc_Stat.sh  output/TestJune26
    cd output/TestJune26

combine txt cards and make workspace (with POI r=higgs signal strength):
    
    combineTool.py -M T2W -i {cmb,tt}/* -o workspace.root --parallel 18
    cp ../../../scripts/texName.json .
    cp ../../../scripts/plot1DScan.py .

now also make workspace (example for tt channel) where the POI is muV and muf (muV=signal strength of VBF and VH; muf=signal strength of ggH). Input: combined txt datacard tt/125/combined.txt.cmb. Output: tt/125/muVmuF_Workspace_tt.root
    
    combineTool.py -M T2W -m 125 -P CombineHarvester.HTTSM2017.muVmuF:muVmuF -i tt/125/combined.txt.cmb -o muVmuF_Workspace_tt.root
    
run limits (on workspace with POI r):
        
        # run the expected limits:
    combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 2 cmb/125/workspace.root -n nominal -t -1 --expectSignal=1
        # run the expected limits without systematics, stat uncertainties only:
    combine -M MultiDimFit -m 125 --algo grid --points 51 --rMin 0 --rMax 2 cmb/125/workspace.root -n nominal_S0 -t -1 --expectSignal=1 -S 0
        # make plots:
    python ./plot1DScan.py --main higgsCombinenominal.MultiDimFit.mH125.root --POI r -o cms_output_plot_r --others 'higgsCombinenominal_S0.MultiDimFit.mH125.root:Stat Unc Only:3'
    
run limits (on workspace with POI muV and muf):

        # run the expected limits for muV with floating muf:
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muV --floatOtherPOIs=1 -M MultiDimFit -m 125 --points 51 -n run_muV
        # run the expected limits for muf with floating muV:
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muf --floatOtherPOIs=1 -M MultiDimFit -m 125 --points 51 -n run_muF
        # run the expected limits for muV with floating muf, without systematics, stat uncertainties only:    
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muV --floatOtherPOIs=1 -M MultiDimFit -m 125 --points 51 -n run_muV_S0 -S 0
        # run the expected limits for muf with floating muV, without systematics, stat uncertainties only: 
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muf --floatOtherPOIs=1 -M MultiDimFit -m 125 --points 51 -n run_muF_S0 -S 0
        # run the expected limits for muV with muf fixed to 1:
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muV --floatOtherPOIs=0 -M MultiDimFit -m 125 --points 51 -n run_muV_fixed_muF
        # run the expected limits for muf with muV fixed to 1:
    combine --setParameterRanges muV=0.0,2.0:muf=0.0,2.0 tt/125/muVmuF_Workspace_tt.root --algo=grid -t -1 --setParameters muV=1.,muf=1. --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P muf --floatOtherPOIs=0 -M MultiDimFit -m 125 --points 51 -n run_muF_fixed_muV
        # make plots:
    python ./plot1DScan.py --main higgsCombinerun_muV.MultiDimFit.mH125.root --main-label Expected_nominal --POI muV -o plot_muV --y-max 8. --others 'higgsCombinerun_muV_S0.MultiDimFit.mH125.root:S0:3'
    python ./plot1DScan.py --main higgsCombinerun_muV.MultiDimFit.mH125.root --main-label Expected_nominal --POI muV -o plot_muV_fixedmuF --y-max 8. --others 'higgsCombinerun_muV_fixed_muF.MultiDimFit.mH125.root:muF_fixed:3'
    python ./plot1DScan.py --main higgsCombinerun_muF.MultiDimFit.mH125.root --main-label Expected_nominal --POI muf -o plot_muF --y-max 8. --others 'higgsCombinerun_muF_S0.MultiDimFit.mH125.root:S0:3'
    python ./plot1DScan.py --main higgsCombinerun_muF.MultiDimFit.mH125.root --main-label Expected_nominal --POI muf -o plot_muF_fixedmuV --y-max 8. --others 'higgsCombinerun_muF_fixed_muV.MultiDimFit.mH125.root:muF_fixed:3'



