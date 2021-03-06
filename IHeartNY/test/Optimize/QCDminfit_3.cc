/*
QCDminfit_3.cc performs a maximum likelihood fit in the MET distribution to determine the 
amount of QCD background. The fit parameters are the number of top (ttbar + single top), 
w+jets, and QCD events in the sample. These are used to normalize the respective templates
in order to fit the MET distribution in data. Templates are taken from the MET histograms 
produced by optimize_topxs.py, scaled and combined as necessary, and normalized to 1. 
The QCD template may be further modified by subtracting the MC sidebands. The fit may be 
performed for the MET_0tag or MET_btag (0 or >=1 btags) MET plots.

The fit is performed using a direct interface with TMinuit, where the function TMinuit 
minimizes is fcn = -2*log(L). The factor of -2 allows for easy insertion of constraints, 
through adding quadratic terms to fcn.
For more info on TMinuit see root.cern.ch/root/html/TMinuit.html .

The inputs to be changed when running the program are found in lines 68, 69, 70, 89, 
and 90. 
Line 68 gives the rebinning factor (number of bins in the original histogram to be 
combined before the fit)
Line 69 gives the new binsize (in GeV)
Line 70 gives the new number of bins
Line 89 specifies whether MC sidebands are subtracted from the data sideband to give the
QCD template.
Line 90 specifies whether to fit the 0 or >=1 btag MET dist.

*/

#include <iostream>
#include <cstdlib>
#include <cmath>
#include <string>
#include <vector>

#include <TMinuit.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TROOT.h>
#include <TF1.h>
#include <TAxis.h>
#include <TLine.h>
#include <TMath.h>
#include <THStack.h>
#include <sstream>
#include "TLatex.h"
#include "TText.h"
#include "TLegend.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TH1D.h"
#include "TH1.h"

//#include "tdrstyle.C"

using namespace std;
// Declare pointer to data as global (not elegant but TMinuit needs this).
vector<int> data_Vec; //input data
vector<double> top_Vec; //ttbar+stop template from MC
vector<double> wjets_Vec; //wjets template from MC
vector<double> qcd_Vec; //qcd template from data driven method

double L = 19748; //UPDATED (in pb)

int Ntotal; //Total # of events -- define as global, currently rewritten for each Njets bin
int nbins = 40;
double xmin = 0.;
double xmax = 400.;

// Rebinning factor, giving number of bins to combine into one (1 means no rebinning).
int binfac = 1;
TString binsize = "10";      // 10 * binfac
TString numberofbins = "40"; // 40 / binfac

TString numberoftags;
double numEvent[3]; //set it global use to set limit in fcn

// Helper functions
void fcn(int& npar, double* deriv, double& f, double par[], int flag);
void getData(int binfac, bool btag);
double* getTemp(int binfac, bool btag, bool dosub);
double* getWeightArray();

TText* doPrelim(float luminosity, float x, float y);

//-------------------------------------------------------------------------
int QCDminfit_3() {

  cout << "Beginning QCD normalization..." << endl;

  // User inputs
  bool dosub = true;
  bool btag = false;

  int nbins_new = nbins / binfac;
  cout << "New # of bins is " << nbins_new << endl;
  if (btag) {
    cout << "Fitting MET_btag" << endl;
    numberoftags = "btag";
  }
  else {
    cout << "Fitting MET_0tag" << endl;
    numberoftags = "0tag";
  }

  getData(binfac, btag);
  double * ini_val = getTemp(binfac, btag, dosub);
  
  // Initialize minuit, set initial values etc. of parameters.
  const int npar = 3; // the number of parameters
  TMinuit minuit(npar);
  minuit.SetFCN(fcn);
  // SetPrintLevel: 1 verbose, 0 normal, -1 quiet
  minuit.SetPrintLevel(1);
  minuit.SetErrorDef(0.5); //because is NLL
  
  int ierflg = 0;
  string parName[npar] = {"top", "wjets", "qcd"};
  double par[npar];
  
  //for(int i=0; i<npar; i++){
    // use the MC estimations for the normalization start values,
    // but correct if out of range.
    //if (ini_val[i] < 0.) {
    //  par[i] = 0.;
    //  numEvent[i] = 0.;
    //}
    
    //else if (ini_val[i] >= Ntotal) {
    //  par[i] = Ntotal - 1.;
    //  numEvent[i] = Ntotal - 1.;
    //}
    
    //else {
    //  par[i] = ini_val[i];
    //  numEvent[i] = ini_val[i];
    //}
  //}
  par[0] = 0.3 * Ntotal;
  par[1] = 0.3 * Ntotal;
  par[2] = 0.4 * Ntotal;
  numEvent[0] = 0.3 * Ntotal;
  numEvent[1] = 0.3 * Ntotal;
  numEvent[2] = 0.4 * Ntotal;

  for(int i=0; i<npar; i++){
    // optimize parameters with initial value of par[i], moving in increments
    // of 1., between 0 and Ntotal
    minuit.mnparm(i, parName[i], par[i], 1., 0, Ntotal, ierflg);
  }
  
  // 1 standard
  // 2 try to improve minimum (slower)
  double arglist[10];
  arglist[0]=2;
  double arglist2[10];
  arglist[0]=10000;
  arglist[1]=2.;
  double arglist3[10];
  arglist[0]=10000;
  arglist[1]=2;
  minuit.mnexcm("SET STR",arglist,1,ierflg);
  minuit.mnexcm("MIGRAD",arglist2,2,ierflg);
  minuit.mnexcm("MINOS", arglist3,3,ierflg);
  // minuit.Migrad();
  
  double outpar[npar], err[npar];
  
  for (int i=0; i<npar; i++){
    minuit.GetParameter(i,outpar[i],err[i]);
  }
  
  // Plot the result.
  TH1F* result = new TH1F("result", "", nbins_new, xmin, xmax);
  TH1F* data = new TH1F("data", "", nbins_new, xmin, xmax);
  
  //top, wjets, and qcd contribution
  TH1F* his_Con[3];
  TH1F* his_Temp[3];
  TString sample_names_array[3] = {"top", "wjets", "qcd"};
  
  for(int i=0; i<3; i++){
    his_Con[i] = new TH1F(sample_names_array[i]+"_Con", "", nbins_new, xmin, xmax);
    his_Temp[i] = new TH1F(sample_names_array[i]+"_Temp", "", nbins_new, xmin, xmax);
  }
  
  THStack* hs = new THStack("hs","stacked histograms");
  
  for (int i=0; i<nbins_new; i++){
    
    data->SetBinContent(i+1, data_Vec[i]);
    
    double mean, top_con, wjets_con, qcd_con;
    
    top_con = outpar[0]*top_Vec[i];
    wjets_con = outpar[1]*wjets_Vec[i];
    qcd_con = outpar[2]*qcd_Vec[i];
    
    mean = top_con + wjets_con + qcd_con;
    result->SetBinContent(i+1, mean); //fitting results
    his_Con[0]->SetBinContent(i+1, top_con);
    his_Con[1]->SetBinContent(i+1, wjets_con);
    his_Con[2]->SetBinContent(i+1, qcd_con);
    his_Temp[0]->SetBinContent(i+1, top_Vec[i]);
    his_Temp[1]->SetBinContent(i+1, wjets_Vec[i]);
    his_Temp[2]->SetBinContent(i+1, qcd_Vec[i]);
    
  }
    
  double pplus, pminus, pparab, pgcc;
  minuit.mnerrs(2, pplus, pminus, pparab, pgcc);

  //print out the results
  cout << " When fitting MET_" << numberoftags << ", the fitting results were" << endl;
  cout << " \t top \t wjets \t qcd"<<endl;

  cout <<" Before fit "<< ini_val[0]<<" \t "<<ini_val[1]<<" \t "<<ini_val[2]<<std::endl;
  cout <<" After fit "<<outpar[0]<<" +- "<<err[0]<<" \t "<<outpar[1]<<" +- "<<err[1]<<" \t "
       <<outpar[2]<<" +- "<<err[2]<<endl;
  cout <<" MINOS errors are +"<<pplus<<", -"<<pminus<<", "<<pparab<<" parabolic and "<<pgcc<<" gcc"<<endl;
  
  //make template plots
  TCanvas* canvasTemp = new TCanvas("canvasTemp", "canvasTemp", 700, 500);
  
  his_Temp[0]->SetLineColor(kRed+1);
  his_Temp[1]->SetLineColor(kGreen-3);
  his_Temp[2]->SetLineColor(kOrange);
  
  his_Temp[0]->SetLineWidth(5);
  his_Temp[1]->SetLineWidth(5);
  his_Temp[2]->SetLineWidth(5);
  
  gStyle->SetOptStat(0);
  his_Temp[0]->SetTitle("");
  his_Temp[0]->Draw();
  double topmax = his_Temp[0]->GetMaximum();
  double wjetmax = his_Temp[1]->GetMaximum();
  double qcdmax = his_Temp[2]->GetMaximum();
  double tmpmax1 = max(topmax, wjetmax);
  double tmpmax2 = max(tmpmax1, qcdmax);
  his_Temp[0]->SetMaximum(1.2 * tmpmax2);
  his_Temp[0]->GetXaxis()->SetTitleSize(0.05);
  
  his_Temp[1]->Draw("same");
  his_Temp[2]->Draw("same");
  
  TLegend* legTemp = new TLegend(0.53, 0.45, 0.73, 0.8);
  legTemp->SetBorderSize(0);
  legTemp->SetTextFont(42);
  legTemp->SetFillColor(0);
  legTemp->AddEntry(his_Temp[0], " Top", "L");
  legTemp->AddEntry(his_Temp[1], " WJets", "L");
  legTemp->AddEntry(his_Temp[2], " QCD", "L");
  
  legTemp->SetTextSize(0.045);
  legTemp->Draw("same");
  TText* textPrelimA = doPrelim(L/1000, 0.525, 0.915);
  textPrelimA->Draw();
  textPrelimA->SetTextFont(42);

  canvasTemp->Update();
  canvasTemp->SaveAs("Temp_"+numberofbins+"b_"+numberoftags+".png");

  //make fit plot
  TCanvas* canvasFit = new TCanvas("canvasFit", "canvasFit", 700, 500);
  
  his_Con[0]->SetFillColor(kRed+1);
  his_Con[1]->SetFillColor(kGreen-3);
  his_Con[2]->SetFillColor(kYellow);
  
  hs->Add(his_Con[2]);
  hs->Add(his_Con[1]);
  hs->Add(his_Con[0]);
  result->SetLineStyle(1); // 1 = solid, 2 = dashed, 3 = dotted
  result->SetLineColor(kBlue); // black (default)
  result->SetLineWidth(3);
  
  data->Sumw2();
  data->SetMarkerStyle(20);
  data->SetMarkerSize(1.2);
  data->SetLineWidth(1);
  
  hs->SetTitle("");
  double h_max = data->GetMaximum();
  double f_max = result->GetMaximum();
  double comb_max = max(h_max, f_max);
  hs->Draw();
  hs->SetMaximum(1.2*comb_max);
  hs->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  hs->GetYaxis()->SetTitle("Number of Events / "+binsize+" GeV");
  hs->GetXaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleOffset(1.4);
  result->Draw("same");
  data->Draw("same");
  
  TLegend* legFit = new TLegend(0.56, 0.5, 0.86, 0.82);
  legFit->SetBorderSize(0);
  legFit->SetTextFont(42);
  legFit->SetFillColor(0);
  legFit->AddEntry(data , " Data", "LPE");
  legFit->AddEntry(result , " Fit", "L");
  legFit->AddEntry(his_Con[0], " Top", "F");
  legFit->AddEntry(his_Con[1], " WJets", "F");
  legFit->AddEntry(his_Con[2], " QCD", "F");
  legFit->SetTextSize(0.04);
  legFit->Draw("same");
  
  TText* textPrelimB = doPrelim(L/1000, 0.525, 0.915);
  textPrelimB->Draw();
  textPrelimB->SetTextFont(42);
  gPad->RedrawAxis();
  
  canvasFit->Update();
  canvasFit->SaveAs("Fit_"+numberofbins+"b_"+numberoftags+".png");

  cout << "To exit, quit ROOT from the File menu of the plot" << endl;
  return 0;
  
}

//-------------------------------------------------------------------------
double* getWeightArray(){

  double xs_array[10], nE_array[10];
  double* weight_array = new double[10];

  xs_array[0] = 245.8; //TTjets 0-700
  nE_array[0] = 21675970;
  xs_array[1] = 245.8; //TTjets 700-1000
  nE_array[1] = 3082812;
  xs_array[2] = 245.8; //TTjets 1000-Inf
  nE_array[2] = 1249111;
  xs_array[3] = 11.1; //St_tW
  nE_array[3] = 497658;
  xs_array[4] = 11.1; //St_tWB
  nE_array[4] = 493460;
  xs_array[5] = 56.4; //St_t
  nE_array[5] = 3758227;
  xs_array[6] = 30.7; //St_tB
  nE_array[6] = 1935072;
  xs_array[7] = 3.79; //St_s
  nE_array[7] = 259961;
  xs_array[8] = 1.76; //St_sB
  nE_array[8] = 139974;
  xs_array[9] = 36703.2; //Wjets
  nE_array[9] = 57709905;

  weight_array[0] = xs_array[0]*L/nE_array[0]; //TTjets 0-700
  weight_array[1] = xs_array[1]*L*0.074/nE_array[1]; //TTjets 700-1000
  weight_array[2] = xs_array[2]*L*0.014/nE_array[2]; //TTjets 1000-Inf
  weight_array[3] = xs_array[3]*L/nE_array[3]; //St_tW
  weight_array[4] = xs_array[4]*L/nE_array[4]; //St_tWB
  weight_array[5] = xs_array[5]*L/nE_array[5]; //St_t
  weight_array[6] = xs_array[6]*L/nE_array[6]; //St_tB
  weight_array[7] = xs_array[7]*L/nE_array[7]; //St_s
  weight_array[8] = xs_array[8]*L/nE_array[8]; //St_sB
  weight_array[9] = xs_array[9]*L/nE_array[9]; //Wjets
  
  return weight_array;

}



// function to read in the data from a histogram
void getData(int binfac, bool btag){

  int nbins_new = nbins / binfac;
  TH1D* h_data = new TH1D("data", "data", nbins, xmin, xmax);
  TFile* datafile = TFile::Open("SingleMu_optimize_mu_Run2012_nom.root", "READ");
  if (btag) {
    h_data = (TH1D*) gDirectory->Get("MET_btag");
  }
  else {
    h_data = (TH1D*) gDirectory->Get("MET_0tag");
  }
  h_data->Rebin(binfac);

  // Write histogram to data vector, calc total # of events
  for(int ibin=0; ibin<nbins_new; ibin++){
    int nn = h_data->GetBinContent(ibin+1);
    data_Vec.push_back(nn);
    Ntotal += nn;
  }
  cout << "Number of data events: " << h_data->Integral() << endl;

}

// Function to produce the top, wjets, and QCD templates
// Function to produce the top, wjets, and QCD templates
double* getTemp(int binfac, bool btag, bool dosub){

  double* ini_val = new double[3];
  TString top_array[9] = {"TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "T_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "T_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom",
			   "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_nom"};
  TString qcd_array[11] = {"SingleMu_optimize_mu_Run2012_qcd",
			   "TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "T_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "T_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_optimize_mu_qcd",
			   "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_optimize_mu_qcd"};

  TString shortnames[10] = {"TTbar_m0to700", "TTbar_m700to1000", "TTbar_m1000toInf",
			    "St_tW", "St_tWB", "St_t", "St_tB", "St_s", "St_sB", "WJets"};

  TString sample_com_array[3] = {"top", "wjets", "qcd"};
  TH1D** top_his_array = new TH1D*[9];
  TH1D** qcd_his_array = new TH1D*[11];
  TH1D** his_com_array = new TH1D*[3];
  TFile* top_file_array[9];
  TFile* qcd_file_array[11];

  double* weight = getWeightArray();
  int nbins_new = nbins / binfac;

  for(int i=0; i<3; i++){
    his_com_array[i] = new TH1D(sample_com_array[i], sample_com_array[i], nbins_new, xmin, xmax);
  }
  
  // Get top template
  for(int i=0; i<9; i++){
    top_file_array[i] = TFile::Open(top_array[i]+".root", "READ");
    if (btag) {
      top_his_array[i] = (TH1D*) gDirectory->Get("MET_btag");
    }
    else {
      top_his_array[i] = (TH1D*) gDirectory->Get("MET_0tag");
    }
    top_his_array[i]->Rebin(binfac);
    double nraw = top_his_array[i]->Integral();
    top_his_array[i]->Scale(weight[i]);
    double nscale = top_his_array[i]->Integral();
    his_com_array[0]->Add(top_his_array[i]);
    cout << "Contribution from " << shortnames[i] << " is " << nraw << " before normalization and " 
	 << nscale << " after." << endl;
  }

  // Get wjets template
  TFile* wjetsfile = TFile::Open("WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_optimize_mu_nom.root", "READ");
  if (btag) {
    his_com_array[1] = (TH1D*) gDirectory->Get("MET_btag");
  }
  else {
    his_com_array[1] = (TH1D*) gDirectory->Get("MET_0tag");
  }
  double nraw = his_com_array[1]->Integral();
  his_com_array[1]->Scale(weight[9]);
  double nscale = his_com_array[1]->Integral();
  his_com_array[1]->Rebin(binfac);
  cout << "Contribution from wjets is " << nraw << " before normalization and " << nscale << " after." << endl;

  // Get qcd template
  qcd_file_array[0] = TFile::Open(qcd_array[0]+".root", "READ");
  if (btag) {
    qcd_his_array[0] = (TH1D*) gDirectory->Get("MET_btag");
  }
  else {
    qcd_his_array[0] = (TH1D*) gDirectory->Get("MET_0tag");
  }
  qcd_his_array[0]->Rebin(binfac);
  his_com_array[2]->Add(qcd_his_array[0]);
  cout << "There are " << qcd_his_array[0]->Integral() << " events in the data sideband " << endl;
  if (dosub) {
    for(int i=0; i<10; i++){
      qcd_file_array[i+1] = TFile::Open(qcd_array[i+1]+".root", "READ");
      if (btag) {
	qcd_his_array[i+1] = (TH1D*) gDirectory->Get("MET_btag");
      }
      else {
	qcd_his_array[i+1] = (TH1D*) gDirectory->Get("MET_0tag");
      }
      qcd_his_array[i+1]->Rebin(binfac);
      double nraw = qcd_his_array[i+1]->Integral();
      qcd_his_array[i+1]->Scale(weight[i]);
      double nscale = qcd_his_array[i+1]->Integral();
      his_com_array[2]->Add(qcd_his_array[i+1], -1);
      cout << "Contribution from " << shortnames[i] << " in sideband is " << nraw << " before normalization and " 
	   << nscale << " after." << endl;    
    }
  }

  // Make breakdown plots 
  TH1F** top_cont_array = new TH1F*[2];
  TString top_cont_names[2] = {"topttbar", "topstop"};
  for(int i=0; i<2; i++){
    top_cont_array[i] = new TH1F(top_cont_names[i], top_cont_names[i], nbins_new, xmin, xmax);
  }
  int colors[4] = {400, 632, 616, 416};

  top_cont_array[0]->Add(top_his_array[0]);
  top_cont_array[0]->Add(top_his_array[1]);
  top_cont_array[0]->Add(top_his_array[2]);
  top_cont_array[1]->Add(top_his_array[3]);
  top_cont_array[1]->Add(top_his_array[4]);
  top_cont_array[1]->Add(top_his_array[5]);
  top_cont_array[1]->Add(top_his_array[6]);
  top_cont_array[1]->Add(top_his_array[7]);
  top_cont_array[1]->Add(top_his_array[8]);


  TCanvas* canvasTop = new TCanvas("canvasTop", "canvasTop", 700, 500);
  THStack* topcont = new THStack("topcont","top contributions");

  for (int i = 0; i<2; i++) {
    top_cont_array[i]->SetFillColor(colors[i+1]);
    topcont->Add(top_cont_array[i]);
  }
  topcont->SetTitle("Contributions to top template");
  topcont->Draw();
  topcont->GetXaxis()->SetTitle("missing E_{T} (GeV)");
  topcont->GetXaxis()->SetTitleSize(0.05);

  TLegend* leg1 = new TLegend(0.56, 0.5, 0.86, 0.82);
  leg1->SetBorderSize(0);
  leg1->SetTextFont(42);
  leg1->SetFillColor(0);
  leg1->AddEntry(top_cont_array[0], " TTJets", "F");
  leg1->AddEntry(top_cont_array[1], " Single top", "F");
  leg1->SetTextSize(0.04);
  leg1->Draw("same");
  
  TText* textPrelim1 = doPrelim(L/1000, 0.525, 0.915);
  textPrelim1->Draw();
  textPrelim1->SetTextFont(42);
  gPad->RedrawAxis();

  canvasTop->Update();
  canvasTop->SaveAs("TopComp_"+numberofbins+"b_"+numberoftags+".png");

  TCanvas* canvasTopNorm = new TCanvas("canvasTopNorm", "canvasTopNorm", 700, 500);
  gStyle->SetOptStat(0);

  double tempmax = 0.;
  for (int i = 0; i<2; i++){
    if (top_cont_array[i]->Integral() > 0.){
      top_cont_array[i]->Scale(1./top_cont_array[i]->Integral());
    }
    top_cont_array[i]->SetLineColor(colors[i+1]);
    top_cont_array[i]->SetLineWidth(5);
    if (top_cont_array[i]->GetMaximum() > tempmax){
      tempmax = top_cont_array[i]->GetMaximum();
    }
  }

  top_cont_array[0]->Draw();
  top_cont_array[0]->GetXaxis()->SetTitleSize(0.05);
  top_cont_array[0]->SetMaximum(1.2 * tempmax);
  top_cont_array[0]->SetTitle("Contributions to top template");
  top_cont_array[1]->Draw("same");

  TLegend* leg2 = new TLegend(0.56, 0.5, 0.86, 0.82);
  leg2->SetBorderSize(0);
  leg2->SetTextFont(42);
  leg2->SetFillColor(0);
  leg2->AddEntry(top_cont_array[0], " TTJets", "L");
  leg2->AddEntry(top_cont_array[1], " Single top", "L");
  leg2->SetTextSize(0.04);
  leg2->Draw("same");

  TText* textPrelim2 = doPrelim(L/1000, 0.525, 0.915);
  textPrelim2->Draw();
  textPrelim2->SetTextFont(42);
  gPad->RedrawAxis();

  canvasTopNorm->Update();
  canvasTopNorm->SaveAs("TopTemp_"+numberofbins+"b_"+numberoftags+".png");

  if (dosub) {
    TH1F** qcd_cont_array = new TH1F*[4];
    TString qcd_cont_names[4] = {"qcdraw", "qcdttbar", "qcdstop", "qcdwjets"};
    for(int i=0; i<4; i++){
      qcd_cont_array[i] = new TH1F(qcd_cont_names[i], qcd_cont_names[i], nbins_new, xmin, xmax);
    }
    
    qcd_cont_array[0]->Add(qcd_his_array[0]);
    qcd_cont_array[1]->Add(qcd_his_array[1]);
    qcd_cont_array[1]->Add(qcd_his_array[2]);
    qcd_cont_array[1]->Add(qcd_his_array[3]);
    qcd_cont_array[2]->Add(qcd_his_array[4]);
    qcd_cont_array[2]->Add(qcd_his_array[5]);
    qcd_cont_array[2]->Add(qcd_his_array[6]);
    qcd_cont_array[2]->Add(qcd_his_array[7]);
    qcd_cont_array[2]->Add(qcd_his_array[8]);
    qcd_cont_array[2]->Add(qcd_his_array[9]);
    qcd_cont_array[3]->Add(qcd_his_array[10]);

    TCanvas* canvasQCD = new TCanvas("canvasQCD", "canvasQCD", 700, 500);
    THStack* QCDcont = new THStack("QCDcont","QCD contributions");

    for (int i = 0; i<4; i++) {
      qcd_cont_array[i]->SetFillColor(colors[i]);
      QCDcont->Add(qcd_cont_array[i]);
    }
    QCDcont->SetTitle("Contributions to qcd template");
    QCDcont->Draw();
    QCDcont->GetXaxis()->SetTitle("missing E_{T} (GeV)");
    QCDcont->GetXaxis()->SetTitleSize(0.05);

    TLegend* leg3 = new TLegend(0.56, 0.5, 0.86, 0.82);
    leg3->SetBorderSize(0);
    leg3->SetTextFont(42);
    leg3->SetFillColor(0);
    leg3->AddEntry(qcd_cont_array[0], " Data sideband", "F");
    leg3->AddEntry(qcd_cont_array[1], " TTJets sb", "F");
    leg3->AddEntry(qcd_cont_array[2], " Single top sb", "F");
    leg3->AddEntry(qcd_cont_array[3], " W+Jets sb", "F");
    leg3->SetTextSize(0.04);
    leg3->Draw("same");

    TText* textPrelim3 = doPrelim(L/1000, 0.525, 0.915);
    textPrelim3->Draw();
    textPrelim3->SetTextFont(42);
    gPad->RedrawAxis();

    canvasQCD->Update();
    canvasQCD->SaveAs("QCDComp_"+numberofbins+"b_"+numberoftags+".png");
    
    TCanvas* canvasQCDNorm = new TCanvas("canvasQCDNorm", "canvasQCDNorm", 700, 500);
    gStyle->SetOptStat(0);

    double tempmax2 = 0.;
    for (int i = 0; i<4; i++){
      if (qcd_cont_array[i]->Integral() > 0.){
	qcd_cont_array[i]->Scale(1./qcd_cont_array[i]->Integral());
      }
      qcd_cont_array[i]->SetLineColor(colors[i]);
      qcd_cont_array[i]->SetLineWidth(5);
	if (qcd_cont_array[i]->GetMaximum() > tempmax2){
	  tempmax2 = qcd_cont_array[i]->GetMaximum();
	}
    }

    qcd_cont_array[0]->Draw();
    qcd_cont_array[0]->GetXaxis()->SetTitleSize(0.05);
    qcd_cont_array[0]->SetMaximum(1.2 * tempmax2);
    qcd_cont_array[0]->SetTitle("Contributions to qcd template");
    qcd_cont_array[1]->Draw("same");
    qcd_cont_array[2]->Draw("same");
    qcd_cont_array[3]->Draw("same");

    TLegend* leg4 = new TLegend(0.56, 0.5, 0.86, 0.82);
    leg4->SetBorderSize(0);
    leg4->SetTextFont(42);
    leg4->SetFillColor(0);
    leg4->AddEntry(qcd_cont_array[0], " Data sideband", "L");
    leg4->AddEntry(qcd_cont_array[1], " TTJets sb", "L");
    leg4->AddEntry(qcd_cont_array[2], " Single top sb", "L");
    leg4->AddEntry(qcd_cont_array[3], " W+Jets sb", "L");
    leg4->SetTextSize(0.04);
    leg4->Draw("same");

    TText* textPrelim4 = doPrelim(L/1000, 0.525, 0.915);
    textPrelim4->Draw();
    textPrelim4->SetTextFont(42);
    gPad->RedrawAxis();

    canvasQCDNorm->Update();
    canvasQCDNorm->SaveAs("QCDTemp_"+numberofbins+"b_"+numberoftags+".png");
  }

  // Normalize histograms to 1 (but first determine Nexp)
  ini_val[0] = his_com_array[0]->Integral();
  ini_val[1] = his_com_array[1]->Integral();
  ini_val[2] = Ntotal - ini_val[0] - ini_val[1];
  if (ini_val[2] < 0.) ini_val[2] = 0.;

  his_com_array[0]->Scale(1./his_com_array[0]->Integral());
  his_com_array[1]->Scale(1./his_com_array[1]->Integral());
  his_com_array[2]->Scale(1./his_com_array[2]->Integral());

  // write histograms to corresponding vectors
  for(int ibin=0; ibin<nbins_new; ibin++){

    double top = his_com_array[0]->GetBinContent(ibin+1);
    top_Vec.push_back(top);

    double wjets = his_com_array[1]->GetBinContent(ibin+1);
    wjets_Vec.push_back(wjets);
    
    double qcd = his_com_array[2]->GetBinContent(ibin+1);
    qcd_Vec.push_back(qcd);
     
  }

  return ini_val;
   
}

//-------------------------------------------------------------------------

// fcn passes back f = - 2*ln(L), the function to be minimized.
void fcn(int& npar, double* deriv, double& f, double par[], int flag){

  double lnL = 0.0;

  int nbins_new = nbins / binfac;

  for (int i=0; i<nbins_new; i++){

    //data_i is the observed number of events in each bin
    int data_i = data_Vec[i];

    //xi is the expected number of events in each bin
    double xi = par[0]*top_Vec[i] + par[1]*wjets_Vec[i] + par[2]*qcd_Vec[i];

    lnL += log(TMath::Poisson(data_i, xi));
    
  }

  f = -2.0 * lnL;

  //Single top constraint
  //double nstop_err = numEvent[1]*0.1;

  //f += (par[1]-numEvent[1])*(par[1]-numEvent[1])/nstop_err/nstop_err;

}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TText* doPrelim(float luminosity, float x, float y)
{
 std::ostringstream stream;
 
 stream <<"CMS Preliminary, L = " << luminosity << " fb^{-1}";
 
 TLatex* text = new TLatex(x, y, stream.str().c_str());

 text->SetNDC(true);
 text->SetTextFont(62);
 text->SetTextSize(0.04);
 return text;
}
