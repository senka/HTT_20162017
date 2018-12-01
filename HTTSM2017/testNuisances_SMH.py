print "starting!"

#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array

import operator
import sys
filename_1 = sys.argv[-1]

filename_out=filename_1.replace(".root","")
filename_out=filename_out+"_problematicNuisances_skim.root"

islog=1
unrollSV=1

file=ROOT.TFile(filename_1,"r")
file1=ROOT.TFile(filename_out,"recreate")

file.cd()
dirList = gDirectory.GetListOfKeys()

print "going into dirs..."

outputFile_txt="summary_nuisances_problems.txt"
outputFile_txt=outputFile_txt.replace(".txt","_"+filename_1.replace(".root","")+".txt")

f = open(outputFile_txt, 'w')


for k1 in dirList:
    print "\t ===================>  DIR : ", k1.GetName()
    h1 = k1.ReadObj()
    nom=k1.GetName()

#    if (nom=="tt_vbf" or nom=="tt_vbf_qcd_cr"):
#      continue
	

    file1.mkdir(nom)
    
    h1.cd()
    histoList = gDirectory.GetListOfKeys()
    name_last=""
           
    for k2 in histoList:
        if (k2.GetName()!=name_last):
            
            h2 = k2.ReadObj()
            h3=h2.Clone()
            h3.SetName(k2.GetName())

            
            #            print " histo: ",h3.GetName()
            # find Up histograms, and identify Down and nominal histogram
            if "Up" in h3.GetName() :
#                print " histo: ",h3.GetName()
                #print "  ====> ZJ 3prong up"
                
                savePlot=0
                bin_problem=-1
                name_Up=h3.GetName()
                name_Down=name_Up.replace("13TeVUp","13TeVDown")
                h_Down=h1.Get(name_Down)

                sep1 = '_CMS'
                sep2 = '_BR'
                sep3 = '_prop'
                sep4 = '_rate'
                sep5 = '_pdf'
                sep6 = '_QCDScale'
                sep7 = '_QCD_Extr'
                sep8 = '_WHigh'
                sep9 = '_WSF'
                sep10 = '_lumi'
                # find the name of mean histogram:
                name_Mean=name_Up
                name_Mean=name_Mean.split(sep1, 1)[0]
                name_Mean=name_Mean.split(sep2, 1)[0]
                name_Mean=name_Mean.split(sep3, 1)[0]
                name_Mean=name_Mean.split(sep4, 1)[0]
                name_Mean=name_Mean.split(sep5, 1)[0]
                name_Mean=name_Mean.split(sep6, 1)[0]
                name_Mean=name_Mean.split(sep7, 1)[0]
                name_Mean=name_Mean.split(sep8, 1)[0]
                name_Mean=name_Mean.split(sep9, 1)[0]
                name_Mean=name_Mean.split(sep10, 1)[0]
                h_Mean=h1.Get(name_Mean)
#                print "\n histoUp  : ", name_Up, " integral: ",h3.Integral()
#                print " histoMean: ", name_Mean, " integral: ",h_Mean.Integral()
#                print " histoDown: ", name_Down, " integral: ",h_Down.Integral()
#                print " histoMean: ", name_Mean, " integral: ",h_Mean.Integral()
                
                
                #                name_mean=name_mean.replace("_CMS_scale_met_clustered_13TeV","")
                #                name_mean=name_mean.replace("_CMS_scale_met_unclustered_13TeV","")
                #                name_mean=name_mean.replace("Up","")
                #                name_mean=name_mean.replace("Down","")
                #                h_mean=h1.Get(name_mean)
                #                h_mean_c=h_mean.Clone()
                # now check Up/Down and mean bin-by-bin:
                #if "ZTT" in name_Mean or "EWKZ" in name_Mean:
                #    continue
                if (h_Mean.Integral()>0.):
                    print "\n histoUp  : ", name_Up, " integral:\t\t ",h3.Integral(), " /mean= ",h3.Integral()/h_Mean.Integral()
                    print " histoMean: ", name_Mean, " integral:\t\t\t\t\t ",h_Mean.Integral()
                    print " histoDown: ", name_Down, " integral:\t ",h_Down.Integral(), " /mean= ",h_Down.Integral()/h_Mean.Integral()
                else:
                    print "\n histoUp  : ", name_Up, " integral:\t\t ",h3.Integral()
                    print " histoMean: ", name_Mean, " integral:\t\t\t\t\t ",h_Mean.Integral()
                    print " histoDown: ", name_Down, " integral:\t ",h_Down.Integral()
                    
                if (name_Up==name_Mean or name_Down==name_Mean):
                    print "   =================> Up or Down has identical yield to nominal! "

                #for bin in range (0,h_Mean.GetNbinsX()+1):
                #for bin in range (0,h_Mean.GetNbins()+1):
                for binX in range (0,h_Mean.GetNbinsX()+1):
                    for binY in range (0,h_Mean.GetNbinsY()+1):
                        bin=h_Mean.GetBin(binX,binY)
                    
                        yield_Mean=h_Mean.GetBinContent(bin)
                        yield_Up=h3.GetBinContent(bin)
                        yield_Down=h_Down.GetBinContent(bin)
                        
                        relative_Up=0
                        relative_Down=0
                        if yield_Mean>0:
                            relative_Up=yield_Up/yield_Mean
                            relative_Down=yield_Down/yield_Mean
                        if yield_Mean>0 or yield_Up>0 or yield_Down>0:
                            print " bin ",bin," yields: ", yield_Down, " ", yield_Mean, " ", yield_Up
                            print " \t\t\t\t\t\t\t\t   relative: ",relative_Down*100.-100.," %, ", relative_Up*100.-100.," %"
                        
                        # problem conditions:
                        # if both Up/Down are on the same size of mean, if uncertainty is larger then 50%
                        if (((relative_Down*100.-100.)*(relative_Up*100.-100.)>0) or (abs(relative_Down*100.-100.)>50. or abs((relative_Up*100.-100.))>50. )) and not ( yield_Up==0 and yield_Mean==0 and yield_Down==0) and not (relative_Down==0 or relative_Up==0)  :
                            
                            #if ( ((relative_Down*100.-100.)*(relative_Up*100.-100.)>0 and (abs(relative_Down*100.-100.)>30. or abs((relative_Up*100.-100.))>30. ) ) or relative_Down<0. or relative_Up>2.) and not ( yield_Up==0 and yield_Mean==0 and yield_Down==0  ) and "origi" not in name_Mean and ( "WH_htt_0L1Zg" not in name_Mean):
                            #if ("ZH" in name_Mean or "WH" in name_Mean or "qqH_htt" in name_Mean) and "reweighted" not in name_Mean:
                            #    continue;
                            #if ("GGH" in name_Mean) and "reweighted" in name_Mean:
                            #    continue;
                            print "   =================> save ",(relative_Down*100.-100.), "*",(relative_Up*100.-100.)," = ", (relative_Down*100.-100.)*(relative_Up*100.-100.)
                            savePlot=1
                            bin_problem=bin
                            f.write('dir: %s histo: %s,%s, bin: %s, yields: %.3f,%.3f,%.3f,\t relative: %.3f , %.3f  \n'%(nom,name_Up,name_Mean, bin_problem,yield_Down,yield_Mean,yield_Up, relative_Down*100.-100., relative_Up*100.-100.))
                            
                            
                            #                name_Down=name_Up.replace("Up","Down")
                            #                h_Down=h1.Get(name_Down)
                            
                            
                        if savePlot==1:
                            
                            nom=k1.GetName()
                            dir_m_name=nom
                            file1.cd(dir_m_name)
                            
                            name_histo=h3.GetName()     
                            name_last=h3.GetName()
                            
                            h3.Write()
                            h_Mean.Write()
                            h_Down.Write()
                            
                            #                    f.write('dir: %s histo: %s, bin: %s \n'%(nom,name_Up, bin_problem))
                            
    h1.Close()

f.close()
