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
    git clone https://github.com/senka/HTT_20162017.git CombineHarvester
    scram b


Now run the limits:

    # unroll 2D histos into 1D unrolled histos (input file: "final_nominal.root", output file: "final_tautau_1D.root")
    cd CombineHarvester/HTTSM2017/shapes/USCMS/
    python Unroll_2Drelaxed.py

    # now prepare to run the limits:
    cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/bin
    # read in all used histos and uncertainties and make root and txt datacards:
    MorphingSM2017 --output_folder="TestJune26" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false
    # add MC stat uncertainties:
    sh _do_mc_Stat.sh  output/TestJune26
    cd output/TestJune26
    # combine txt cards and make workspace:
    combineTool.py -M T2W -i {cmb,tt}/* -o workspace.root --parallel 18
    cp ../../../scripts/texName.json .
    cp ../../../scripts/plot1DScan.py .
    # run the expected limits:
    combine -M MultiDimFit -m 125 --algo grid --points 101 --rMin 0 --rMax 10 cmb/125/workspace.root -n nominal -t -1 --expectSignal=1
    combine -M MultiDimFit --algo none --rMin 0 --rMax 10 cmb/125/workspace.root -m 125 -n bestfit --saveWorkspace -t -1 --expectSignal=1
    combine -M MultiDimFit --algo grid --points 101 --rMin 0 --rMax 10 -m 125 -n stat higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters all --fastScan  -t -1 --expectSignal=1
    # make plots:
    python ./plot1DScan.py --main higgsCombinenominal.MultiDimFit.mH125.root --POI r -o cms_output_freeze_All --others 'higgsCombinestat.MultiDimFit.mH125.root:Freeze all:2' --breakdown syst,stat


