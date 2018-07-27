#!/usr/bin/env python
import ROOT
import re
from array import array

islog=1

def add_lumi():
    lowX=0.7
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.08)
    lumi.SetTextFont (   42 )
    lumi.AddText("2016, 20.1 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.11
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.1)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.18
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
	if islog:
	   output = ROOT.TLegend(0.12, 0.05, 0.92, 0.25, "", "brNDC")
           output.SetNColumns(5)
	else:
           output = ROOT.TLegend(0.55, 0.3, 0.92, 0.75, "", "brNDC")
	   output.SetNColumns(2)
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        #output.SetFillStyle(0)
        output.SetFillColor(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output

ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)

c=ROOT.TCanvas("canvas","",0,0,1800,600)
c.cd()

file=ROOT.TFile("final_nominal.root","r")
file1D=ROOT.TFile("htt_tt.inputs-sm-13TeV-2D.root","recreate")

adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

categories=["tt_0jet","tt_boosted","tt_vbf"] # input dir names
cat=["tt_0jet","tt_boosted","tt_vbf"] # outout dir names
processes=["data_obs","ZTT","W","QCD","ZL","ZJ","TTT","TTJ","VVT","VVJ","EWKZ","ggH125","VBF125","WH125","ZH125"] # input histos
processes_plot_bkg=["ZTT","W","QCD","ZL","ZJ","TTT","TTJ","VVT","VVJ","EWKZ"] # bkg processes for plot
processes_plot_signal=["ggH125","VBF125"] # signal processes for plot
ncat=3

for i in range (0,ncat): # loop over categories
    mydir=file1D.mkdir(cat[i])

    print "=================>>>  category: ", categories[i]
    for i_histo in processes: # loop over input histos (processes)
        print " histo: ", i_histo
        histo2D=file.Get(categories[i]).Get(i_histo)
        histo2D_d=file.Get(categories[i]).Get(i_histo)
        histo2D_u=file.Get(categories[i]).Get(i_histo)

        nx=histo2D.GetXaxis().GetNbins()
        ny=histo2D.GetYaxis().GetNbins()

        histo=ROOT.TH1F("histo","histo",nx*ny,0,nx*ny)
        histo_u=ROOT.TH1F("histo_u","histo_u",nx*ny,0,nx*ny)
        histo_d=ROOT.TH1F("histo_d","histo_d",nx*ny,0,nx*ny)

        histo.SetName(histo2D.GetName())
        histo_u.SetName(histo2D_u.GetName())
        histo_d.SetName(histo2D_d.GetName())
        
        
        l=0
        for j in range(1,nx+1):
            for k in range(1,ny+1):
	        l=l+1
                n = histo2D.GetBin(j,k);
                histo.SetBinContent(l,histo2D.GetBinContent(n))
                histo.SetBinError(l,histo2D.GetBinError(n))
                histo_u.SetBinContent(l,histo2D_u.GetBinContent(n))
                histo_u.SetBinError(l,histo2D_u.GetBinError(n))
                histo_d.SetBinContent(l,histo2D_d.GetBinContent(n))
                histo_d.SetBinError(l,histo2D_d.GetBinError(n))

        mydir.cd()
        histo.Write()
        histo_u.Write()
        histo_d.Write()            

# now make nice unrolled plots:
