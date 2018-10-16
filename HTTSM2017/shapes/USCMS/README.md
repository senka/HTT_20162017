# Quick comparison

## Instruction :
One can test whole procedure using two root files in exampleInputs.
For now I prepare this instruction turnning off all systematics.
0. Get old version of 'HttSystematics_SMRun2.cc' to turn off systematics. 

(This is just a temporary way to do for quick progress. I'll figure out better way to do this.)

```
export SCRAM_ARCH=slc6_amd64_gcc530
scram pro -n CombHarvester_8_1_0 CMSSW CMSSW_8_1_0
cd CombHarvester_8_1_0/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone git@github.com:KState-HEP-HTT/CombineHarvester.git CombineHarvester
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/src
rm HttSystematics_SMRun2.cc
wget https://raw.githubusercontent.com/senka/HTT_20162017/664628b737ddf1089d5d6a6ef70dbc364bb8eb5b/HTTSM2017/src/HttSystematics_SMRun2.cc
cd $CMSSW_BASE/src
scram b
```

1. Save input root file which is output of tt_analyzer.cc under this area and named ```final_nominal.root```.

```
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes/USCMS/
cp exampleInputs/2016VBFcat.root final_nominal.root
```

2. From the same place you stored final_nominal.root, unrolling, morphing and whole extra step can be done by running this script.

```source ComparisonRecipe.sh Test_2016VBF 2016```

3. Repeat sept 1 and 2 with your 2nd inputfile. 

```
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/shapes/USCMS/
cp exampleInputs/VBFenriched.root final_nominal.root
source ComparisonRecipe.sh Test_VBFenriched KSU
```

4. Compare plots nominal

```
cp ../Test_2016VBF/higgsCombinenominal_2016.MultiDimFit.mH125.root .
python ./plot1DScan.py --main higgsCombinenominal_2016.MultiDimFit.mH125.root --POI r -o cms_output_comparison  --main-label "2016analysis"  --others 'higgsCombinenominal_KSU.MultiDimFit.mH125.root:VBFenriched:2'
```