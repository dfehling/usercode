#####################################################################
#
# A python script to produce MET plots for the boosted top QCD estimation
# Plots are produced for each step of the selection function
# 
#####################################################################

#! /usr/bin/env python
import os
import glob

#Helper function to find electron relative isolation
def getAeff(eleEta) :
    aEff = 0.0
    if abs(eleEta) < 1.0:
        aEff = 0.21
    if (abs(eleEta) > 1.0 and abs(eleEta) < 1.479):
        aEff = 0.21
    if (abs(eleEta) > 1.479 and abs(eleEta) < 2.0):
        aEff = 0.11
    if (abs(eleEta) > 2.0 and abs(eleEta) < 2.2):
        aEff = 0.14
    if (abs(eleEta) > 2.2 and abs(eleEta) < 2.3):
        aEff = 0.18
    if (abs(eleEta) > 2.3 and abs(eleEta) < 2.4):
        aEff = 0.19
    if abs(eleEta) > 2.4:
        aEff = 0.26
    return float(aEff) 

from optparse import OptionParser

parser = OptionParser()

#Describe all command line options

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')


parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='TTSemilepAnalyzer_antibtag_w_mucut',
                  dest='outname',
                  help='output name')

parser.add_option('--pileup', metavar='F', type='string', action='store',
                  default='none',
                  dest='pileup',
                  help='ttbar or wjets')

parser.add_option('--isNew', metavar='F', action='store_true',
                  default=False,
                  dest='isNew',
                  help='running on new ntuples')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='B discriminator cut')

parser.add_option('--htCut', metavar='F', type='float', action='store',
                  default=150.,
                  dest='htCut',
                  help='HT cut')

parser.add_option('--thisQCD', metavar='F', type='string', action='store',
                  default='none',
                  dest='thisQCD',
                  help='old, loose, or btag')

(options, args) = parser.parse_args()

argv = []

eventsbegin = [1,10000001,20000001,30000001,40000001,50000001]
eventsend = [10000000,20000000,30000000,40000000,50000000,60000000]

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

import sys
from DataFormats.FWLite import Events, Handle

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname + ".root", "recreate")
name = options.outname

print "Creating histograms"

PileFile = ROOT.TFile("../Pileup_plots.root")
if options.pileup == 'wjets':
	PilePlot = PileFile.Get("pweightwjets")
if options.pileup == 'ttbar':
	PilePlot = PileFile.Get("pweightttbar")
f.cd()

histMET = ROOT.TH1F("histMET", "MET", 40, 0., 400.)
histMETbtag = ROOT.TH1F("histMETbtag", "MET", 40, 0., 400.)
histMETnjet = ROOT.TH1F("histMETnjet", "MET", 40, 0., 400.)
histMETtoppt = ROOT.TH1F("histMETtoppt", "MET", 40, 0., 400.)
histMETnsj = ROOT.TH1F("histMETnsj", "MET", 40, 0., 400.)
histMETminm = ROOT.TH1F("histMETminm", "MET", 40, 0., 400.)
histMETmass = ROOT.TH1F("histMETmass", "MET", 40, 0., 400.)
histMETtop = ROOT.TH1F("histMETtop", "MET", 40, 0., 400.)
histMETvsBtag = ROOT.TH2F("histMETvsBtag", "MET vs. nBtags", 40, 0., 400., 3, -0.5, 2.5)
histMETvsNjets = ROOT.TH2F("histMETvsNjets", "MET vs. nJets", 40, 0., 400., 10, -0.5, 9.5)
histMETvsTopPt = ROOT.TH2F("histMETvsTopPt", "MET vs. Top Jet Pt", 40, 0., 400., 50, 200., 1200.)
histMETvsNsj = ROOT.TH2F("histMETvsNsj", "MET vs. # Subjets", 40, 0., 400., 5, -0.5, 4.5)
histMETvsMinM = ROOT.TH2F("histMETvsMinM", "MET vs. Min Mass", 40, 0., 400., 35, 0., 140.)
histMETvsTopM = ROOT.TH2F("histMETvsTopM", "MET vs. Top Jet Mass", 40, 0., 400., 40, 0., 400.)

events = Events (files)

puHandle    	= 	Handle("int")
puLabel     	= 	( "pileup", "npvRealTrue" )

tightJetPtHandle         = Handle( "std::vector<float>" )
tightJetPtLabel    = ( "pfShyftTupleJets",   "pt" )
tightJetEtaHandle         = Handle( "std::vector<float>" )
tightJetEtaLabel    = ( "pfShyftTupleJets",   "eta" )
tightJetPhiHandle         = Handle( "std::vector<float>" )
tightJetPhiLabel    = ( "pfShyftTupleJets",   "phi" )
tightJetMassHandle         = Handle( "std::vector<float>" )
tightJetMassLabel    = ( "pfShyftTupleJets",   "mass" )
tightJetCSVHandle         = Handle( "std::vector<float>" )
tightJetCSVLabel    = ( "pfShyftTupleJets",   "csv" )

looseJetPtHandle         = Handle( "std::vector<float>" )
looseJetPtLabel    = ( "pfShyftTupleJetsLoose",   "pt" )
looseJetEtaHandle         = Handle( "std::vector<float>" )
looseJetEtaLabel    = ( "pfShyftTupleJetsLoose",   "eta" )
looseJetPhiHandle         = Handle( "std::vector<float>" )
looseJetPhiLabel    = ( "pfShyftTupleJetsLoose",   "phi" )
looseJetMassHandle         = Handle( "std::vector<float>" )
looseJetMassLabel    = ( "pfShyftTupleJetsLoose",   "mass" )
looseJetCSVHandle         = Handle( "std::vector<float>" )
looseJetCSVLabel    = ( "pfShyftTupleJetsLoose",   "csv" )

if options.isNew :
    tightJetPtHandle         = Handle( "std::vector<float>" )
    tightJetPtLabel    = ( "pfShyftTupleJetsAK5",   "pt" )
    tightJetEtaHandle         = Handle( "std::vector<float>" )
    tightJetEtaLabel    = ( "pfShyftTupleJetsAK5",   "eta" )
    tightJetPhiHandle         = Handle( "std::vector<float>" )
    tightJetPhiLabel    = ( "pfShyftTupleJetsAK5",   "phi" )
    tightJetMassHandle         = Handle( "std::vector<float>" )
    tightJetMassLabel    = ( "pfShyftTupleJetsAK5",   "mass" )
    tightJetCSVHandle         = Handle( "std::vector<float>" )
    tightJetCSVLabel    = ( "pfShyftTupleJetsAK5",   "csv" )

    looseJetPtHandle         = Handle( "std::vector<float>" )
    looseJetPtLabel    = ( "pfShyftTupleJetsLooseAK5",   "pt" )
    looseJetEtaHandle         = Handle( "std::vector<float>" )
    looseJetEtaLabel    = ( "pfShyftTupleJetsLooseAK5",   "eta" )
    looseJetPhiHandle         = Handle( "std::vector<float>" )
    looseJetPhiLabel    = ( "pfShyftTupleJetsLooseAK5",   "phi" )
    looseJetMassHandle         = Handle( "std::vector<float>" )
    looseJetMassLabel    = ( "pfShyftTupleJetsLooseAK5",   "mass" )
    looseJetCSVHandle         = Handle( "std::vector<float>" )
    looseJetCSVLabel    = ( "pfShyftTupleJetsLooseAK5",   "csv" )

topTagPtHandle         = Handle( "std::vector<float>" )
topTagPtLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "pt" )
topTagEtaHandle         = Handle( "std::vector<float>" )
topTagEtaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "eta" )
topTagPhiHandle         = Handle( "std::vector<float>" )
topTagPhiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "phi" )
topTagMassHandle         = Handle( "std::vector<float>" )
topTagMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "mass" )
topTagMinMassHandle         = Handle( "std::vector<float>" )
topTagMinMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "minMass" )
topTagNSubjetsHandle         = Handle( "std::vector<float>" )
topTagNSubjetsLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "nSubjets" )

tightMuonPtHandle         = Handle( "std::vector<float>" )
tightMuonPtLabel    = ( "pfShyftTupleMuons",   "pt" )
tightMuonEtaHandle         = Handle( "std::vector<float>" )
tightMuonEtaLabel    = ( "pfShyftTupleMuons",   "eta" )
tightMuonPhiHandle         = Handle( "std::vector<float>" )
tightMuonPhiLabel    = ( "pfShyftTupleMuons",   "phi" )
tightMuonPfisoHandle         = Handle( "std::vector<float>" )
tightMuonPfisoLabel    = ( "pfShyftTupleMuons",   "pfisoPU" )

looseMuonPtHandle         = Handle( "std::vector<float>" )
looseMuonPtLabel    = ( "pfShyftTupleMuonsLoose",   "pt" )
looseMuonEtaHandle         = Handle( "std::vector<float>" )
looseMuonEtaLabel    = ( "pfShyftTupleMuonsLoose",   "eta" )
looseMuonPhiHandle         = Handle( "std::vector<float>" )
looseMuonPhiLabel    = ( "pfShyftTupleMuonsLoose",   "phi" )
looseMuonPfisoHandle         = Handle( "std::vector<float>" )
looseMuonPfisoLabel    = ( "pfShyftTupleMuonsLoose",   "pfisoPU" )

tightElePtHandle         = Handle( "std::vector<float>" )
tightElePtLabel    = ( "pfShyftTupleElectrons",   "pt" )
tightEleEtaHandle         = Handle( "std::vector<float>" )
tightEleEtaLabel    = ( "pfShyftTupleElectrons",   "eta" )
tightElePhiHandle         = Handle( "std::vector<float>" )
tightElePhiLabel    = ( "pfShyftTupleElectrons",   "phi" )
tightElePfisoCHHandle         = Handle( "std::vector<float>" )
tightElePfisoCHLabel    = ( "pfShyftTupleElectrons",   "pfisoCH" )
tightElePfisoNHHandle         = Handle( "std::vector<float>" )
tightElePfisoNHLabel    = ( "pfShyftTupleElectrons",   "pfisoNH" )
tightElePfisoPHHandle         = Handle( "std::vector<float>" )
tightElePfisoPHLabel    = ( "pfShyftTupleElectrons",   "pfisoPH" )

looseElePtHandle         = Handle( "std::vector<float>" )
looseElePtLabel    = ( "pfShyftTupleElectronsLoose",   "pt" )
looseEleEtaHandle         = Handle( "std::vector<float>" )
looseEleEtaLabel    = ( "pfShyftTupleElectronsLoose",   "eta" )
looseElePhiHandle         = Handle( "std::vector<float>" )
looseElePhiLabel    = ( "pfShyftTupleElectronsLoose",   "phi" )
looseElePfisoCHHandle         = Handle( "std::vector<float>" )
looseElePfisoCHLabel    = ( "pfShyftTupleElectronsLoose",   "pfisoCH" )
looseElePfisoNHHandle         = Handle( "std::vector<float>" )
looseElePfisoNHLabel    = ( "pfShyftTupleElectronsLoose",   "pfisoNH" )
looseElePfisoPHHandle         = Handle( "std::vector<float>" )
looseElePfisoPHLabel    = ( "pfShyftTupleElectronsLoose",   "pfisoPH" )

rhoHandle         = Handle( "double" )
rhoLabel    = ( "kt6PFJets",   "rho" )

tightMetHandle = Handle( "std::vector<float>" )
tightMetLabel = ("pfShyftTupleMET",   "pt" )
tightMetphiHandle = Handle( "std::vector<float>" )
tightMetphiLabel = ("pfShyftTupleMET",   "phi" )

looseMetHandle = Handle( "std::vector<float>" )
looseMetLabel = ("pfShyftTupleMETLoose",   "pt" )
looseMetphiHandle = Handle( "std::vector<float>" )
looseMetphiLabel = ("pfShyftTupleMETLoose",   "phi" )

mptv=0  #Counts number of times muonPtHandle.isValid() fails

# loop over events
count = 0
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0

print "Start looping"
for event in events:
    weight = 1.0
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)

    tightElePts = []
    tightElePfisoCHs = []
    tightElePfisoNHs = []
    tightElePfisoPHs = []
    tightEleEtas = []
    tightElePhis = []
    looseElePts = []
    looseElePfisoCHs = []
    looseElePfisoNHs = []
    looseElePfisoPHs = []
    looseEleEtas = []
    looseElePhis = []
    looseMuonPts = []
    looseMuonEtas = []
    looseMuonPhis = []
    looseMuonPfisos = []
    tightMuonPts = []
    tightMuonEtas = []
    tightMuonPhis = []
    tightMuonPfisos = []
    looseJetPts = []
    looseJetEtas = []
    looseJetPhis = []
    looseJetMasses = []
    looseJetCSVs = []
    tightJetPts = []
    tightJetEtas = []
    tightJetPhis = []
    tightJetMasses = []
    tightJetCSVs = []

    # Get muons
    event.getByLabel (looseMuonPtLabel, looseMuonPtHandle)
    if looseMuonPtHandle.isValid():
        looseMuonPts = looseMuonPtHandle.product()
    event.getByLabel (looseMuonEtaLabel, looseMuonEtaHandle)
    if looseMuonEtaHandle.isValid():
        looseMuonEtas = looseMuonEtaHandle.product()
    event.getByLabel (looseMuonPhiLabel, looseMuonPhiHandle)
    if looseMuonPhiHandle.isValid():
        looseMuonPhis = looseMuonPhiHandle.product()
    event.getByLabel (looseMuonPfisoLabel, looseMuonPfisoHandle)
    if looseMuonPfisoHandle.isValid():
        looseMuonPfisos = looseMuonPfisoHandle.product()

    event.getByLabel (tightMuonPtLabel, tightMuonPtHandle)
    if tightMuonPtHandle.isValid():
        tightMuonPts = tightMuonPtHandle.product()
    event.getByLabel (tightMuonEtaLabel, tightMuonEtaHandle)
    if tightMuonEtaHandle.isValid():
        tightMuonEtas = tightMuonEtaHandle.product()
    event.getByLabel (tightMuonPhiLabel, tightMuonPhiHandle)
    if tightMuonPhiHandle.isValid():
        tightMuonPhis = tightMuonPhiHandle.product()
    event.getByLabel (tightMuonPfisoLabel, tightMuonPfisoHandle)
    if tightMuonPfisoHandle.isValid():
        tightMuonPfisos = tightMuonPfisoHandle.product()

    # Do muon cuts here
    nTightMuon = 0
    if len(tightMuonPts) > 0:
        for iTightMuon in range(0,len(tightMuonPts)):
            if (tightMuonPts[iTightMuon] > 45. and abs(tightMuonEtas[iTightMuon]) < 2.1 and tightMuonPfisos[iTightMuon] / tightMuonPts[iTightMuon] < 0.12):
                nTightMuon += 1

    nLooseMuon = 0
    nInvMuon = 0
    if len(looseMuonPts) > 0:
        for iLooseMuon in range(0,len(looseMuonPts)):
            if (looseMuonPts[iLooseMuon] > 45. and abs(looseMuonEtas[iLooseMuon]) < 2.1):
                nLooseMuon += 1
                if (looseMuonPfisos[iLooseMuon] / looseMuonPts[iLooseMuon] > 0.12):
                    nInvMuon += 1

    if options.thisQCD == "loose" and nLooseMuon != 1 and nTightMuon != 0:
        continue
    if options.thisQCD == "old" and nInvMuon != 1:
        continue
    if (options.thisQCD == "none" or options.thisQCD == "btag") and nTightMuon != 1 :
        continue

    count0 += 1

    rho = -9999.
    event.getByLabel (rhoLabel, rhoHandle)
    if rhoHandle.isValid():
        rho = rhoHandle.product()

    event.getByLabel (tightElePtLabel, tightElePtHandle)
    if tightElePtHandle.isValid():
        tightElePts = tightElePtHandle.product()
    event.getByLabel (tightElePfisoCHLabel, tightElePfisoCHHandle)
    if tightElePfisoCHHandle.isValid():
        tightElePfisoCHs = tightElePfisoCHHandle.product()
    event.getByLabel (tightElePfisoNHLabel, tightElePfisoNHHandle)
    if tightElePfisoNHHandle.isValid():
        tightElePfisoNHs = tightElePfisoNHHandle.product()
    event.getByLabel (tightElePfisoPHLabel, tightElePfisoPHHandle)
    if tightElePfisoPHHandle.isValid():
        tightElePfisoPHs = tightElePfisoPHHandle.product()
    event.getByLabel (tightEleEtaLabel, tightEleEtaHandle)
    if tightEleEtaHandle.isValid():
        tightEleEtas = tightEleEtaHandle.product()
    event.getByLabel (tightElePhiLabel, tightElePhiHandle)
    if tightElePhiHandle.isValid():
        tightElePhis = tightElePhiHandle.product()

    event.getByLabel (looseElePtLabel, looseElePtHandle)
    if looseElePtHandle.isValid():
        looseElePts = looseElePtHandle.product()
    event.getByLabel (looseElePfisoCHLabel, looseElePfisoCHHandle)
    if looseElePfisoCHHandle.isValid():
        looseElePfisoCHs = looseElePfisoCHHandle.product()
    event.getByLabel (looseElePfisoNHLabel, looseElePfisoNHHandle)
    if looseElePfisoNHHandle.isValid():
        looseElePfisoNHs = looseElePfisoNHHandle.product()
    event.getByLabel (looseElePfisoPHLabel, looseElePfisoPHHandle)
    if looseElePfisoPHHandle.isValid():
        looseElePfisoPHs = looseElePfisoPHHandle.product()
    event.getByLabel (looseEleEtaLabel, looseEleEtaHandle)
    if looseEleEtaHandle.isValid():
        looseEleEtas = looseEleEtaHandle.product()
    event.getByLabel (looseElePhiLabel, looseElePhiHandle)
    if looseElePhiHandle.isValid():
        looseElePhis = looseElePhiHandle.product()

    # Do electron cuts here
    nTightEle = 0
    if len(tightElePts) > 0:
        for itightElePt in range(0,len(tightElePts)):
            tightElePt = tightElePts[itightElePt]
            tightElePfiso = tightElePfisoCHs[itightElePt] + max(0.0, tightElePfisoNHs[itightElePt] + tightElePfisoPHs[itightElePt] - rho[0] * getAeff(tightEleEtas[itightElePt]))
            if tightElePfiso / tightElePt < 0. :
                continue
            if (tightElePt > 35.0 and abs(tightEleEtas[itightElePt]) < 2.5 and tightElePfiso / tightElePt < 0.1) :
                nTightEle += 1

    nLooseEle = 0
    if len(looseElePts) > 0 :
        for ilooseElePt in range(0,len(looseElePts)):
            looseElePt = looseElePts[ilooseElePt]
            looseElePfiso = looseElePfisoCHs[ilooseElePt] + max(0.0, looseElePfisoNHs[ilooseElePt] + looseElePfisoPHs[ilooseElePt] - rho[0] * getAeff(looseEleEtas[ilooseElePt]))
            if looseElePfiso / looseElePt < 0.:
                continue
            if (looseElePt > 35.0 and abs(looseEleEtas[ilooseElePt]) < 2.5 and looseElePfiso / looseElePt < 0.1) :
                nLooseEle += 1

    if (options.thisQCD == "none" or options.thisQCD == "btag") and nTightEle != 0:
        continue
    if (options.thisQCD == "old" or options.thisQCD == "loose") and nLooseEle != 0:
        continue

    count1 += 1

    # Get jets
    event.getByLabel (looseJetPtLabel, looseJetPtHandle)
    if looseJetPtHandle.isValid():
        looseJetPts = looseJetPtHandle.product()
    event.getByLabel (looseJetEtaLabel, looseJetEtaHandle)
    if looseJetEtaHandle.isValid():
        looseJetEtas = looseJetEtaHandle.product()
    event.getByLabel (looseJetPhiLabel, looseJetPhiHandle)
    if looseJetPhiHandle.isValid():
        looseJetPhis = looseJetPhiHandle.product()
    event.getByLabel (looseJetMassLabel, looseJetMassHandle)
    if looseJetMassHandle.isValid():
        looseJetMasses = looseJetMassHandle.product()
    event.getByLabel (looseJetCSVLabel, looseJetCSVHandle)
    if looseJetCSVHandle.isValid():
        looseJetCSVs = looseJetCSVHandle.product()

    event.getByLabel (tightJetPtLabel, tightJetPtHandle)
    if tightJetPtHandle.isValid():
        tightJetPts = tightJetPtHandle.product()
    event.getByLabel (tightJetEtaLabel, tightJetEtaHandle)
    if tightJetEtaHandle.isValid():
        tightJetEtas = tightJetEtaHandle.product()
    event.getByLabel (tightJetPhiLabel, tightJetPhiHandle)
    if tightJetPhiHandle.isValid():
        tightJetPhis = tightJetPhiHandle.product()
    event.getByLabel (tightJetMassLabel, tightJetMassHandle)
    if tightJetMassHandle.isValid():
        tightJetMasses = tightJetMassHandle.product()
    event.getByLabel (tightJetCSVLabel, tightJetCSVHandle)
    if tightJetCSVHandle.isValid():
        tightJetCSVs = tightJetCSVHandle.product()

    # Do jet / btag cuts here
    looseMuonP4 = ROOT.TLorentzVector()
    if (len(looseMuonPts) > 0 and len(looseMuonEtas) > 0 and len(looseMuonPhis) > 0):
        looseMuonP4.SetPtEtaPhiM( looseMuonPts[0], looseMuonEtas[0], looseMuonPhis[0], 0.0 )

    nLooseJets = 0
    nLooseBtag = 0
    if len(looseMuonPts) > 0 and len(looseMuonEtas) > 0 and len(looseMuonPhis) > 0 and len(looseJetPts) > 0:
        for ijet in range(0,len(looseJetPts)) :
            if (looseJetPts[ijet] > 30.0 and abs(looseJetEtas[ijet]) < 2.5):
                nLooseJets += 1
                jet = ROOT.TLorentzVector()
                jet.SetPtEtaPhiM( looseJetPts[ijet], looseJetEtas[ijet], looseJetPhis[ijet], looseJetMasses[ijet] )
                if jet.DeltaR( looseMuonP4 ) < ROOT.TMath.Pi() / 2.0 : 
                    if looseJetCSVs[ijet] > options.bDiscCut :
                        nLooseBtag += 1

    tightMuonP4 = ROOT.TLorentzVector()
    if len(tightMuonPts) > 0 and len(tightMuonEtas) > 0 and len(tightMuonPhis) > 0:
        tightMuonP4.SetPtEtaPhiM( tightMuonPts[0], tightMuonEtas[0], tightMuonPhis[0], 0.0 )

    nTightJets = 0
    nTightBtag = 0
    if len(tightMuonPts) > 0 and len(tightMuonEtas) > 0 and len(tightMuonPhis) > 0 and len(tightJetPts) > 0:
        for ijet in range(0,len(tightJetPts)) :
            if (tightJetPts[ijet] > 30.0 and abs(tightJetEtas[ijet]) < 2.5):
                nTightJets += 1
                jet = ROOT.TLorentzVector()
                jet.SetPtEtaPhiM( tightJetPts[ijet], tightJetEtas[ijet], tightJetPhis[ijet], tightJetMasses[ijet] )
                if jet.DeltaR( tightMuonP4 ) < ROOT.TMath.Pi() / 2.0 : 
                    if tightJetCSVs[ijet] > options.bDiscCut :
                        nTightBtag += 1

    if (options.thisQCD == "loose" or options.thisQCD == "old") and nLooseJets >= 2:
        count2 += 1
        if nLooseBtag >= 1:
            count3 += 1

    elif (options.thisQCD == "none" or options.thisQCD == "btag") and nTightJets >= 2:
        count2 += 1
        if options.thisQCD == "none" and nTightBtag >= 1:
            count3 += 1
        elif options.thisQCD == "btag" and nTightBtag == 0:
            count3 += 1

    # Get MET
    looseMet = -1.
    event.getByLabel (looseMetLabel, looseMetHandle)
    if looseMetHandle.isValid():
        looseMets = looseMetHandle.product()
        looseMet = looseMets[0]

    tightMet = -1.
    event.getByLabel (tightMetLabel, tightMetHandle)
    if tightMetHandle.isValid():
        tightMets = tightMetHandle.product()
        tightMet = tightMets[0]

    # Do HT / MET cuts here
    htLoose = -1.
    if len(looseMuonPts) > 0 and len(looseMuonEtas) > 0 and len(looseMuonPhis) > 0:
        htLoose = looseMet + looseMuonP4.Perp()
    htTight = -1.
    if len(tightMuonPts) > 0 and len(tightMuonEtas) > 0 and len(tightMuonPhis) > 0:
        htTight = tightMet + tightMuonP4.Perp()

    if (options.thisQCD == "loose" or options.thisQCD == "old") and htLoose < options.htCut:
        continue
    elif (options.thisQCD == "none" or options.thisQCD == "btag") and htTight < options.htCut:
        continue

    if (options.thisQCD == "loose" or options.thisQCD == "old") and nLooseJets >= 2 and nLooseBtag >= 1:
        count4 += 1
    elif options.thisQCD == "none" and nTightJets >= 2 and nTightBtag >= 1:
        count4 += 1
    elif options.thisQCD == "btag" and nTightJets >= 2 and nTightBtag == 0:
        count4 += 1

    if (options.thisQCD == "loose" or options.thisQCD == "old") and looseMet < 20.:
        continue
    if (options.thisQCD == "none" or options.thisQCD == "btag") and tightMet < 20.:
        continue

    if (options.thisQCD == "loose" or options.thisQCD == "old") and nLooseJets >= 2 and nLooseBtag >= 1:
        count5 += 1
    elif options.thisQCD == "none" and nTightJets >= 2 and nTightBtag >= 1:
        count5 += 1
    elif options.thisQCD == "btag" and nTightJets >= 2 and nTightBtag == 0:
        count5 += 1
        
    # Get the top jet
    event.getByLabel (topTagPtLabel, topTagPtHandle)
    if topTagPtHandle.isValid():
        topTagPt = topTagPtHandle.product()
    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    if topTagEtaHandle.isValid():
        topTagEta = topTagEtaHandle.product()
    event.getByLabel (topTagPhiLabel, topTagPhiHandle)
    if topTagPhiHandle.isValid():
        topTagPhi = topTagPhiHandle.product()
    event.getByLabel (topTagMassLabel, topTagMassHandle)
    if topTagMassHandle.isValid():
        topTagMass = topTagMassHandle.product()
    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    if topTagMinMassHandle.isValid():
        topTagMinMass = topTagMinMassHandle.product()
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    if topTagNSubjetsHandle.isValid():
        topTagNSub = topTagNSubjetsHandle.product()

    topjet = ROOT.TLorentzVector()
    if len(topTagPt) > 0 and len(topTagEta) > 0 and len(topTagPhi) > 0 and len(topTagMass) > 0:
        topjet.SetPtEtaPhiM( topTagPt[0], topTagEta[0], topTagPhi[0], topTagMass[0] )

    # Get pileup
    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp 		= 	puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)

    # Fill plots here
    if len(topTagPt) > 0 and len(topTagEta) > 0 and len(topTagPhi) > 0 and len(topTagMass) > 0:
        if (options.thisQCD == "loose" or options.thisQCD == "old"):
            # Full sel
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMET.Fill(looseMet, weight)

            # no btag cut
            if ( nLooseJets >= 2 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETbtag.Fill(looseMet, weight)
                histMETvsBtag.Fill(looseMet, nLooseBtag, weight)

            # no njets cut
            if ( nLooseBtag >= 1 and
                 topjet.DeltaR(looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnjet.Fill(looseMet, weight)
                histMETvsNjets.Fill(looseMet, nLooseJets, weight)

            # no top pt cut
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250.) :
                histMETtoppt.Fill(looseMet, weight)

            # no nsj cut
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnsj.Fill(looseMet, weight)

            # no min mass cut
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETminm.Fill(looseMet, weight)

            # no top mass cut
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagPt[0] > 400.) :
                histMETmass.Fill(looseMet, weight)

            # no top cuts
            if ( nLooseJets >= 2 and 
                 nLooseBtag >= 1 and
                 topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0):
                histMETtop.Fill(looseMet, weight)
                histMETvsTopPt.Fill(looseMet, topTagPt[0], weight)
                histMETvsNsj.Fill(looseMet, topTagNSub[0], weight)
                histMETvsMinM.Fill(looseMet, topTagMinMass[0], weight)
                histMETvsTopM.Fill(looseMet, topTagMass[0], weight)

        # Plots for 0 tag sample
        if options.thisQCD == "btag":
            # Full sel
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMET.Fill(tightMet, weight)

            # no btag cut
            if ( nTightJets >= 2 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETbtag.Fill(tightMet, weight)
                histMETvsBtag.Fill(tightMet, nTightBtag, weight)

            # no njets cut
            if ( nTightBtag == 0 and
                 topjet.DeltaR(tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnjet.Fill(tightMet, weight)
                histMETvsNjets.Fill(tightMet, nTightJets, weight)

            # no top pt cut
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250.) :
                histMETtoppt.Fill(tightMet, weight)

            # no nsj cut
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnsj.Fill(tightMet, weight)

            # no min mass cut
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETminm.Fill(tightMet, weight)

            # no top mass cut
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagPt[0] > 400.) :
                histMETmass.Fill(tightMet, weight)

            # no top cuts
            if ( nTightJets >= 2 and 
                 nTightBtag == 0 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0):
                histMETtop.Fill(tightMet, weight)
                histMETvsTopPt.Fill(tightMet, topTagPt[0], weight)
                histMETvsNsj.Fill(tightMet, topTagNSub[0], weight)
                histMETvsMinM.Fill(tightMet, topTagMinMass[0], weight)
                histMETvsTopM.Fill(tightMet, topTagMass[0], weight)

        if options.thisQCD == "none" :
            # Full sel
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMET.Fill(tightMet, weight)

            # no btag cut
            if ( nTightJets >= 2 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETbtag.Fill(tightMet, weight)
                histMETvsBtag.Fill(tightMet, nTightBtag, weight)

            # no njets cut
            if ( nTightBtag >= 1 and
                 topjet.DeltaR(tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnjet.Fill(tightMet, weight)
                histMETvsNjets.Fill(tightMet, nTightJets, weight)

            # no top pt cut
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250.) :
                histMETtoppt.Fill(tightMet, weight)

            # no nsj cut
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagMinMass[0] >= 50. and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETnsj.Fill(tightMet, weight)

            # no min mass cut
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMass[0] > 140. and topTagMass[0] < 250. and
                 topTagPt[0] > 400.) :
                histMETminm.Fill(tightMet, weight)

            # no top mass cut
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and
                 topTagNSub[0] >= 3 and
                 topTagMinMass[0] >= 50. and
                 topTagPt[0] > 400.) :
                histMETmass.Fill(tightMet, weight)

            # no top cuts
            if ( nTightJets >= 2 and 
                 nTightBtag >= 1 and
                 topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0):
                histMETtop.Fill(tightMet, weight)
                histMETvsTopPt.Fill(tightMet, topTagPt[0], weight)
                histMETvsNsj.Fill(tightMet, topTagNSub[0], weight)
                histMETvsMinM.Fill(tightMet, topTagMinMass[0], weight)
                histMETvsTopM.Fill(tightMet, topTagMass[0], weight)

    # cutflow counts
    if (options.thisQCD == "loose" or options.thisQCD == "old") and nLooseJets >= 2 and nLooseBtag >= 1 and len(topTagPt) > 0:
        if topjet.DeltaR( looseMuonP4) > ROOT.TMath.Pi() / 2.0 and topTagNSub[0] >= 3 :
            count6 += 1
            if topTagMinMass[0] >= 50. :
                count7 += 1
                if topTagMass[0] > 140. and topTagMass[0] < 250. :
                    count8 += 1
                    if topTagPt[0] > 400. :
                        count9 += 1

    elif options.thisQCD == "none" and nTightJets >= 2 and nTightBtag >= 1 and len(topTagPt) > 0 :
        if topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and topTagNSub[0] >= 3 :
            count6 += 1
            if topTagMinMass[0] >= 50. :
                count7 += 1
                if topTagMass[0] > 140. and topTagMass[0] < 250. :
                    count8 += 1
                    if topTagPt[0] > 400. :
                        count9 += 1

    elif options.thisQCD == "btag" and nTightJets >= 2 and nTightBtag == 0 and len(topTagPt) > 0 :
        if topjet.DeltaR( tightMuonP4) > ROOT.TMath.Pi() / 2.0 and topTagNSub[0] >= 3 :
            count6 += 1
            if topTagMinMass[0] >= 50. :
                count7 += 1
                if topTagMass[0] > 140. and topTagMass[0] < 250. :
                    count8 += 1
                    if topTagPt[0] > 400. :
                        count9 += 1

# Print out cutflow results
print  '*** Cutflow table ***'
print  'Using QCD option ' + options.thisQCD
print  'Total Events: ' + str(count)
print  'isvalid() cuts: ' + str(mptv)
print  'Exactly one muon: ' + str(count0)
print  'Exactly zero electrons: ' + str(count1)
print  'At least 2 jets: ' + str(count2)
if options.thisQCD == "btag":
    print  'Exactly 0 btags: ' + str(count3)
else :
    print  'At least 1 btag: ' + str(count3)
print  'HT > ' + str(options.htCut) + ' GeV: ' + str(count4)
print  'MET > 20 GeV: ' + str(count5)
print  'At least three subjets: ' + str(count6)
print  'Min mass > 50 GeV: ' + str(count7)
print  '140 GeV < Top jet mass < 250 GeV: ' + str(count8) 
print  'Top jet pt > 400 GeV: ' + str(count9)


f.cd()
f.Write()
f.Close()
