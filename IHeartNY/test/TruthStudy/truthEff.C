#include "TROOT.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <vector>

using namespace std;


void SetPlotStyle();
void mySmallText(Double_t x,Double_t y,Color_t color,char *text); 
void myItalicText(Double_t x,Double_t y,Color_t color,char *text); 


void truthEff(TString option, bool doPart, TString pdf) {

  bool doElectron = true;

  TString path = "";
  TString muOrEl = "mu";
  TString DIR = "2Dhists";
  if (doElectron) {
    path = "_el";
    muOrEl = "el";
    DIR = "qcd_el";
  }

  SetPlotStyle();

  if ( !(option == "trigSF" || option == "eff" || option == "eff_nobtag")) {
    cout << "not a valid option! exiting..." << endl;
    return;
  }
  
  // full truth samlpes (aka denominator)
  TFile* f_true0    = new TFile("TT_max700_"+pdf+path+"_fullTruth.root");
  TFile* f_true700  = new TFile("TT_Mtt-700to1000_"+pdf+path+"_fullTruth.root");
  TFile* f_true1000 = new TFile("TT_Mtt-1000toInf_"+pdf+path+"_fullTruth.root");

  if (doPart) {
    TH1F* h_true0    = (TH1F*) f_true0->Get("ptPartTop");
    TH1F* h_true700  = (TH1F*) f_true700->Get("ptPartTop");
    TH1F* h_true1000 = (TH1F*) f_true1000->Get("ptPartTop");
  }
  else {
    TH1F* h_true0    = (TH1F*) f_true0->Get("ptGenTop");
    TH1F* h_true700  = (TH1F*) f_true700->Get("ptGenTop");
    TH1F* h_true1000 = (TH1F*) f_true1000->Get("ptGenTop");
  }
  h_true0->Sumw2();
  h_true700->Sumw2();
  h_true1000->Sumw2();

  // default samples with trigger (aka numerator) 
  TFile* f_trig0    = new TFile("../histfiles_"+pdf+"/"+DIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+pdf+"_2Dcut_nom.root");
  TFile* f_trig700  = new TFile("../histfiles_"+pdf+"/"+DIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+pdf+"_2Dcut_nom.root");
  TFile* f_trig1000 = new TFile("../histfiles_"+pdf+"/"+DIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+pdf+"_2Dcut_nom.root");

  if (doPart) {
    if (option=="eff") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptPartTop_passRecoParticle");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptPartTop_passRecoParticle");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptPartTop_passRecoParticle");
    }
    else if (option=="eff_nobtag") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptPartTop_passRecoNoBtagParticle");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptPartTop_passRecoNoBtagParticle");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptPartTop_passRecoNoBtagParticle");
    }
    else if (option=="trigSF") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptPartTop");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptPartTop");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptPartTop");
    }
  }
  else {
    if (option=="eff") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptGenTop_passRecoParton");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptGenTop_passRecoParton");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptGenTop_passRecoParton");
    }
    else if (option=="eff_nobtag") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptGenTop_passRecoNoBtagParton");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptGenTop_passRecoNoBtagParton");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptGenTop_passRecoNoBtagParton");
    }
    else if (option=="trigSF") {
      TH1F* hh_trig0    = (TH1F*) f_trig0->Get("ptGenTop");
      TH1F* hh_trig700  = (TH1F*) f_trig700->Get("ptGenTop");
      TH1F* hh_trig1000 = (TH1F*) f_trig1000->Get("ptGenTop");
    }
  }
  hh_trig0->Sumw2();
  hh_trig700->Sumw2();
  hh_trig1000->Sumw2();


  if (!doElectron) {
    TH1F* h_trig0 = (TH1F*) hh_trig0->Clone("tmp0");
    TH1F* h_trig700 = (TH1F*) hh_trig700->Clone("tmp700");
    TH1F* h_trig1000 = (TH1F*) hh_trig1000->Clone("tmp1000");
  }
  else {
    TH1F* h_trig0 = (TH1F*) h_true0->Clone("tmp0");
    h_trig0->Reset();
    TH1F* h_trig700 = (TH1F*) h_true700->Clone("tmp700");
    h_trig700->Reset();
    TH1F* h_trig1000 = (TH1F*) h_true1000->Clone("tmp1000");
    h_trig1000->Reset();

    for (int ib=1; ib<h_true0->GetNbinsX()+1; ib++) {
      h_trig0->SetBinContent(ib,hh_trig0->GetBinContent(ib+2));
      h_trig0->SetBinError(ib,hh_trig0->GetBinError(ib+2));
      h_trig700->SetBinContent(ib,hh_trig700->GetBinContent(ib+2));
      h_trig700->SetBinError(ib,hh_trig700->GetBinError(ib+2));
      h_trig1000->SetBinContent(ib,hh_trig1000->GetBinContent(ib+2));
      h_trig1000->SetBinError(ib,hh_trig1000->GetBinError(ib+2));
    }
  }


  // normalize to be able to switch together the three mass ranges
  float ttbar_xs = 245.8;
  if (pdf=="scaleup") ttbar_xs = 252.0;
  if (pdf=="scaledown") ttbar_xs = 237.4; 
  float lumi = 19.7*1000;

  float n_ttbar0 = 21675970.;
  float n_ttbar700 = 3082812.;
  float n_ttbar1000 = 1249111.;
  if (pdf=="scaleup") {
    n_ttbar0 = 14983686.;
    n_ttbar700 = 2243672.;
    n_ttbar1000 = 1241650.;
  }
  if (pdf=="scaledown") {
    n_ttbar0 = 14545715*89./102.;
    n_ttbar700 = 2170074.;
    n_ttbar1000 = 1308090.;
  }

  float eff_ttbar0 = 1.0;
  float eff_ttbar700 = 0.074;
  float eff_ttbar1000 = 0.015;
  if (pdf=="scaleup") {
    eff_ttbar700 = 0.074;
    eff_ttbar1000 = 0.014;
  }
  if (pdf=="scaledown") {
    eff_ttbar700 = 0.081;
    eff_ttbar1000 = 0.016;
  }


  h_true0->Scale(ttbar_xs*lumi*eff_ttbar0/n_ttbar0);
  h_true700->Scale(ttbar_xs*lumi*eff_ttbar700/n_ttbar700);
  h_true1000->Scale(ttbar_xs*lumi*eff_ttbar1000/n_ttbar1000);
  h_true0->Add(h_true700);
  h_true0->Add(h_true1000);

  h_trig0->Scale(ttbar_xs*lumi*eff_ttbar0/n_ttbar0);
  h_trig700->Scale(ttbar_xs*lumi*eff_ttbar700/n_ttbar700);
  h_trig1000->Scale(ttbar_xs*lumi*eff_ttbar1000/n_ttbar1000);
  h_trig0->Add(h_trig700);
  h_trig0->Add(h_trig1000);


  TH1F* h_sf = (TH1F*) h_true0->Clone("eff");
  h_sf->Clear();
  if (option.Contains("eff")) h_sf->Divide(h_trig0,h_true0,1.0,1.0,"B");
  else h_sf->Divide(h_true0,h_trig0,1.0,1.0,"B");
  
  h_sf->GetYaxis()->SetTitleOffset(1.1);
  if (option.Contains("eff")) h_sf->GetYaxis()->SetTitle("Efficiency");
  else h_sf->GetYaxis()->SetTitle("Correction factor");


  if (option.Contains("eff")) h_sf->SetAxisRange(0.0,0.15,"Y");
  else if (doPart && doElectron) h_sf->SetAxisRange(1.0,1.8,"Y");
  else if (doPart) h_sf->SetAxisRange(1.0,1.4,"Y");
  else if (doElectron) h_sf->SetAxisRange(1.2,2.2,"Y");
  else h_sf->SetAxisRange(1.0,2.0,"Y");


  TF1* fit = new TF1("fit", "pol1", 400,1200);
  h_sf->Fit("fit","R");
  // pol = a + x*b
  float a  = fit->GetParameter(0);
  float ea = fit->GetParError(0);
  float b  = fit->GetParameter(1);
  float eb = fit->GetParError(1);
  cout << "a = " << a << " +/- " << ea << ", b = " << b << " +/- " << eb << endl;

  TH1F* h_sf_smooth = (TH1F*) h_sf->Clone("sf_smooth");
  h_sf_smooth->Clear();

  for (int ib=0; ib<h_sf->GetNbinsX(); ib++) {
    float bc = a + h_sf_smooth->GetBinCenter(ib+1) * b;
    float ebc = sqrt(ea*ea + h_sf_smooth->GetBinCenter(ib+1)*eb*h_sf_smooth->GetBinCenter(ib+1)*eb);
    cout << "bin center = " << h_sf_smooth->GetBinCenter(ib+1) << ", bin content = " << bc << " +/- " << ebc << endl;
    h_sf_smooth->SetBinContent(ib+1, bc);
    h_sf_smooth->SetBinError(ib+1, ebc);
  }


  TCanvas c;
  h_sf->Draw("lep");
  h_sf_smooth->SetLineColor(4);
  h_sf_smooth->SetMarkerColor(4);
  h_sf_smooth->SetMarkerStyle(24);
  h_sf_smooth->Draw("lep,same");

  if (option=="eff") {
    mySmallText(0.4,0.42,1,"Total selection efficiency");
    mySmallText(0.4,0.36,1,"(events passing trigger & all selection cuts");
    mySmallText(0.4,0.30,1,"vs all semileptonic t#bar{t} #rightarrow #mu+jets)");
  }
  else if (option=="eff_nobtag") {
    mySmallText(0.4,0.42,1,"Total selection efficiency");
    mySmallText(0.4,0.36,1,"(events passing trigger & all selection cuts w/o btag");
    mySmallText(0.4,0.30,1,"vs all semileptonic t#bar{t} #rightarrow #mu+jets)");
  }
  else {
    mySmallText(0.22,0.36,1,"Correction factor");
    if (doPart) mySmallText(0.22,0.30,1,"(pass trigger+SHyFT vs pass particle-level)");
    else mySmallText(0.22,0.30,1,"(pass trigger+SHyFT vs pass parton)");
  }

  if (option=="trigSF") {
    cout << endl;
    for (int i=1; (int)i<h_sf->GetNbinsX()+1; i++) {
      if (doPart) cout << "trigSF_rp [";
      else cout << "trigSF [";
      cout  << h_sf->GetBinLowEdge(i) << "," << h_sf->GetBinLowEdge(i+1) << "]: " << h_sf->GetBinContent(i) << " +/- " << h_sf->GetBinError(i) << endl;
    }
  }

  if (option.Contains("eff")) cout << endl << "Overall SF = " << h_trig0->Integral()/h_true0->Integral() << endl << endl;
  else {
    if (doPart) cout << endl << "Overall trigSF_rp (";
    else cout << endl << "Overall trigSF (";
    cout << pdf << ") = " << h_true0->Integral()/h_trig0->Integral() << endl << endl;
  }

  TString outname = "truth"+path+"_"+option;
  if (doPart) outname += "_rp";
  c.SaveAs(outname+"_"+pdf+".png");
  c.SaveAs(outname+"_"+pdf+".eps");
  
}


void SetPlotStyle() {

  // from ATLAS plot style macro

  // use plain black on white colors
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetStatColor(0);
  gStyle->SetHistLineColor(1);

  gStyle->SetPalette(1);

  // set the paper & margin sizes
  gStyle->SetPaperSize(20,26);
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.16);
  gStyle->SetPadLeftMargin(0.16);

  // set title offsets (for axis label)
  gStyle->SetTitleXOffset(1.4);
  gStyle->SetTitleYOffset(1.4);

  // use large fonts
  gStyle->SetTextFont(42);
  gStyle->SetTextSize(0.05);
  gStyle->SetLabelFont(42,"x");
  gStyle->SetTitleFont(42,"x");
  gStyle->SetLabelFont(42,"y");
  gStyle->SetTitleFont(42,"y");
  gStyle->SetLabelFont(42,"z");
  gStyle->SetTitleFont(42,"z");
  gStyle->SetLabelSize(0.05,"x");
  gStyle->SetTitleSize(0.05,"x");
  gStyle->SetLabelSize(0.05,"y");
  gStyle->SetTitleSize(0.05,"y");
  gStyle->SetLabelSize(0.05,"z");
  gStyle->SetTitleSize(0.05,"z");

  // use bold lines and markers
  gStyle->SetMarkerStyle(20);
  gStyle->SetMarkerSize(1.2);
  gStyle->SetHistLineWidth(2.);
  gStyle->SetLineStyleString(2,"[12 12]");

  // get rid of error bar caps
  gStyle->SetEndErrorSize(0.);

  // do not display any of the standard histogram decorations
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

}


void mySmallText(Double_t x,Double_t y,Color_t color,char *text) {
  Double_t tsize=0.044;
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
void myItalicText(Double_t x,Double_t y,Color_t color,char *text) {
  Double_t tsize=0.044;
  TLatex l;
  l.SetTextFont(52);
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}


