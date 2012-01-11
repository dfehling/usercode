import ROOT
import copy
from math import *
from operator import itemgetter, attrgetter

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle
from Analysis.TTBSMTuplesAnalysis import *

class Type11Analyzer :
    """Run 1 + 1 Analysis"""
    def __init__(self, useMC, outfile, mistagFile, collectionLabelSuffix, useGenWeight, triggerFile, modMassFile, pdfWeight="nominal", triggerWeight = "noWeight"):
        self.outfile = outfile
        self.mistagFileStr = mistagFile
        self.triggerFileStr = triggerFile
        self.modMassFileStr = modMassFile
        self.useMC = useMC
        self.useGenWeight = useGenWeight
        self.pdfWeight = pdfWeight
        self.triggerWeight = triggerWeight
		
        label = 'ttbsmAna'+collectionLabelSuffix


        self.allTopTagHandle = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
        self.allTopTagLabel  = ( label,   "topTagP4")

        self.allTopTagTopMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagTopMassLabel   = ( label,   "topTagTopMass" )
        self.allTopTagMinMassHandle  = Handle( "std::vector<double>" )
        self.allTopTagMinMassLabel   = ( label,   "topTagMinMass" )
        self.allTopTagNSubjetsHandle    = Handle("std::vector<double>" )
        self.allTopTagNSubjetsLabel     = ( label,   "topTagNSubjets" )

        self.allTopTagPassHandle  = Handle( "std::vector<int>" )
        self.allTopTagPassLabel   = ( label,   "topTagPass" )

        self.weightsHandle = Handle( "double" )
        self.weightsLabel = ( label, "weight" )
        self.pdfHandle = Handle("std::vector<double>")
        self.pdfLabel = ( label, "pdfWeights")
        
        self.__book__()



    def __del__ (self):
        """(Internal) Destructor"""
        print 'Goodbye from Type11Analyzer. Before I go, I will delete some stuff'
        self.f.cd()
        self.mttPredDist.GetPredictedHist().Write()
        self.mttPredDist.GetObservedHist().Write()
        self.mttPredDist.GetTaggableHist().Write()
        
        self.mttPredDistMassCut.GetPredictedHist().Write()
        self.mttPredDistMassCut.GetObservedHist().Write()
        self.mttPredDistMassCut.GetTaggableHist().Write()

        self.mttPredDistModMassFlat.GetPredictedHist().Write()
        self.mttPredDistModMassFlat.GetObservedHist().Write()
        self.mttPredDistModMassFlat.GetTaggableHist().Write()

        self.mttPredDistMod3MassFlat.GetPredictedHist().Write()
        self.mttPredDistMod3MassFlat.GetObservedHist().Write()
        self.mttPredDistMod3MassFlat.GetTaggableHist().Write()

        self.mttPredDistMod3MassFlatSubtract.GetPredictedHist().Write()
        self.mttPredDistMod3MassFlatSubtract.GetObservedHist().Write()
        self.mttPredDistMod3MassFlatSubtract.GetTaggableHist().Write()

        self.mttPredDistModMassQCDdistSubtract.GetPredictedHist().Write()
        self.mttPredDistModMassQCDdistSubtract.GetObservedHist().Write()
        self.mttPredDistModMassQCDdistSubtract.GetTaggableHist().Write()

        
        for pair in sorted(self.runPairs, key=itemgetter(3)) :
            print '{0:12.2f} : Run {1:15.0f}, LumiBlock {2:15.0f}, Event {3:30.0f}'.format(
                pair[3], pair[0], pair[2], pair[1]
                )

        print '1'
        self.f.Write()
        self.f.Close()
        print '4'
        self.mistagFile.Close()
        self.triggerFile.Close()
        self.modMassFile.Close()
        print '5'

        print 'So long!'

    def __book__( self ) :
        """(Internal) Books histograms"""

        print 'Booking histograms'
        self.mistagFile = ROOT.TFile(self.mistagFileStr + ".root")
        self.mistagFile.cd()
        self.mistag = self.mistagFile.Get("TYPE11_MISTAG").Clone()
        self.mistag.SetName('mistag')
        self.mistagMassCut = self.mistagFile.Get("TYPE11_MISTAG_MASSCUT_LARGEBINS").Clone()
        self.mistagMassCut.SetName('mistagMassCut')
        if not self.useGenWeight:
            #self.mistagMassCutSubtract = self.mistagFile.Get("TYPE11_MISTAG_MASSCUT_SUBTRACT_TTBAR_LARGEBINS").Clone()
            self.mistagMassCutSubtract = self.mistagFile.Get("MISTAG_MU_REVERSE_SUB_TTBAR").Clone()
            self.mistagMassCutSubtract.SetName('mistagMassCutSubtract')
        if self.useGenWeight:
            self.mistagMassCutSubtract = self.mistagFile.Get("TYPE11_MISTAG_MASSCUT_LARGEBINS").Clone()
            self.mistagMassCutSubtract.SetName('mistagMassCutSubtract')
        print self.mistag.GetBinContent(3)
        ROOT.SetOwnership( self.mistag, False )
        ROOT.SetOwnership( self.mistagMassCut, False )
       
        self.triggerFile = ROOT.TFile(self.triggerFileStr + ".root")
        self.triggerFile.cd()
        self.triggerFile.ls()
        self.triggerHist = self.triggerFile.Get("TYPE11_TRIGGER_EFFIC").Clone()
        self.triggerHist.SetName('triggerHist')
        ROOT.SetOwnership( self.triggerHist, False )

        self.modMassFile = ROOT.TFile(self.modMassFileStr + ".root")
        self.modMassFile.cd()
        self.modMassFile.ls()
        #self.modMassHist = self.modMassFile.Get("jetMass").Clone()
        self.modMassHist = self.modMassFile.Get("jetMassOneTag_MassWindow").Clone()
        self.modMassHist.SetName('modMassHist')
        ROOT.SetOwnership( self.modMassHist, False )
        print "integral "+str(self.modMassHist.Integral())
       # print "integral "+str(self.jetMassOneTag_MassWindow.Integral())
       
        self.f = ROOT.TFile( self.outfile + ".root", "recreate" )
        self.f.cd()

        self.mttPredDist                 = ROOT.PredictedDistribution( self.mistagMassCutSubtract, "mttPredDist", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistMassCut          = ROOT.PredictedDistribution( self.mistagMassCut, "mttPredDistMassCut", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistModMassFlat      = ROOT.PredictedDistribution( self.mistagMassCut, "mttPredDistModMassFlat", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistMod3MassFlat     = ROOT.PredictedDistribution( self.mistagMassCut, "mttPredDistMod3MassFlat", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistMod3MassFlatSubtract     = ROOT.PredictedDistribution( self.mistagMassCutSubtract, "mttPredDistMod3MassFlatSubtract", "mTT Mass",       1000, 0,  5000 )
        self.mttPredDistModMassQCDdistSubtract     = ROOT.PredictedDistribution( self.mistagMassCutSubtract, "mttPredDistModMassQCDdistSubtract", "mTT Mass",       1000, 0,  5000 )


        ROOT.SetOwnership( self.mttPredDist, False )
        ROOT.SetOwnership( self.mttPredDistMassCut, False )
        ROOT.SetOwnership( self.mttPredDistModMassFlat, False )
        ROOT.SetOwnership( self.mttPredDistMod3MassFlat, False )
        ROOT.SetOwnership( self.mttPredDistMod3MassFlatSubtract, False )
        ROOT.SetOwnership( self.mttPredDistModMassQCDdistSubtract, False )

        self.jetEta               = ROOT.TH1D("jetEta",               "jetEta",            100, -4,    4)
        self.jetRap               = ROOT.TH1D("jetRap",               "jetRap",            100, -4,    4)
        self.jetMass              = ROOT.TH1D("jetMass",              "jetMass",        100,  0,  500 )
        self.jetMassOneTag        = ROOT.TH1D("jetMassOneTag",        "jetMassOneTag",        100,  0,  500 )
        self.jetPt                = ROOT.TH1D("jetPt",                "jetPt",          400,  0,  2000 )    
        self.jetPtOneTag          = ROOT.TH1D("jetPtOneTag",          "jetPtOneTag",    400,  0,  2000 )
        self.jetRapOneTag         = ROOT.TH1D("jetRapOneTag",         "jetRapOneTag",    100, -4, 4 )
        self.jetMinMass           = ROOT.TH1D("jetMinMass",           "jetMinMass",          400,  0,  200 )
        self.topTagMass           = ROOT.TH1D("topTagMass",           "Top Tag Mass",             100,  0,  500 )
        self.topTagMinMass        = ROOT.TH1D("topTagMinMass",               "Top Tag MinMass",             100,  0,  200 )
        self.topTagPt             = ROOT.TH1D("topTagPt",                    "Top Tag Pt",               400,  0,  2000 )
        self.mttCandMass          = ROOT.TH1D("mttCandMass",                     "mTT Cand Mass",                 1000, 0,  5000 )
        self.mttMass              = ROOT.TH1D("mttMass",                     "mTT Mass",                 1000, 0,  5000 )
        self.mttMassTriggerWeighted   = ROOT.TH1D("mttMassTriggerWeighted",                     "mTT Mass",                 1000, 0,  5000 )
        self.cutflow              = ROOT.TH1D("cutflow",                     "cutflow",                 7, 0,  7 ) 
        self.mtt_gen              = ROOT.TH1D("mtt_gen",              "mtt gen",                    1000,   0,    5000)
        self.mtt_gen_vs_reco      = ROOT.TH2D("mtt_gen_vs_reco",      "mtt gen vs reco",    1000, 0,  5000, 1000, 0,  5000)
        
        self.mttMass.Sumw2()
        self.runPairs = []
        self.mttMassTriggerWeighted.Sumw2()

    def analyze(self, event) :
        """Analyzes event"""
        
        event.getByLabel (self.allTopTagLabel, self.allTopTagHandle)
        topJets = self.allTopTagHandle.product()
         
        self.cutflow.Fill(0.5,1)    

        nTopCand = 0
        for i in range(0,len(topJets) ) :
          if( topJets[i].pt() > 350 ) :
            nTopCand = nTopCand + 1

        if nTopCand < 2 :
            return

        
        #pairMass = 0.0
        #ttMass = 0.0

        weight = 1.0
        if self.useGenWeight :
            event.getByLabel( self.weightsLabel, self.weightsHandle )
            weight = self.weightsHandle.product()[0]

        if self.triggerWeight != "noWeight" :
            jetTriggerWeight = 1.0
            if topJets[0].pt() < 800:
                bin0 = self.triggerHist.FindBin(topJets[0].pt()) 
                jetTriggerWeight = self.triggerHist.GetBinContent(bin0)
                deltaTriggerEff  = 0.5*(1.0-jetTriggerWeight)
                jetTriggerWeightUp  =   jetTriggerWeight + deltaTriggerEff
                jetTriggerWeightDown  = jetTriggerWeight - deltaTriggerEff
                jetTriggerWeightUp  = min(1.0,jetTriggerWeightUp)
                jetTriggerWeightDown  = max(0.0,jetTriggerWeightDown)
                if self.triggerWeight == "Nominal" :
                    weight = weight*jetTriggerWeight
                if self.triggerWeight == "Up" :
                    weight = weight*jetTriggerWeightUp
                if self.triggerWeight == "Down" :
                    weight = weight*jetTriggerWeightDown


        #print 'topJets[0].pt() ' + str(topJets[0].pt())    
        #print 'jetTriggerWeight ' + str(jetTriggerWeight)    

        event.getByLabel (self.allTopTagMinMassLabel, self.allTopTagMinMassHandle)
        topJetMinMass= self.allTopTagMinMassHandle.product()
        event.getByLabel (self.allTopTagNSubjetsLabel, self.allTopTagNSubjetsHandle)
        topJetNSubjets= self.allTopTagNSubjetsHandle.product()
        event.getByLabel (self.allTopTagTopMassLabel, self.allTopTagTopMassHandle)
        topJetMass= self.allTopTagTopMassHandle.product()
        event.getByLabel (self.allTopTagPassLabel, self.allTopTagPassHandle )
        topJetPass= self.allTopTagPassHandle.product()


        if self.pdfWeight != "nominal" :
            iweight = 0.0
            event.getByLabel( self.pdfLabel, self.pdfHandle )
            pdfs = self.pdfHandle.product()
            if self.pdfWeight == "up" :
                for pdf in pdfs[0::2] :
                    iweight = iweight + pdf
            else :
                for pdf in pdfs[1::2] :
                    iweight = iweight + pdf
            iweight = iweight / len(pdfs) * 2.0
            weight = iweight

        ttMass = 0.0
        deltaPhi = topJets[0].phi() - topJets[1].phi()
        if deltaPhi > ROOT.TMath.Pi():
            deltaPhi = deltaPhi - 2*ROOT.TMath.Pi()
        if deltaPhi < -ROOT.TMath.Pi():
            deltaPhi = deltaPhi + 2*ROOT.TMath.Pi()

        #ptCuts = topJets[0].pt() > 450 and topJets[1].pt() > 450
        ptCuts = topJets[0].pt() > 350 and topJets[1].pt() > 350
        etaCuts = abs(topJets[0].Rapidity()) < 2.4 and abs(topJets[1].Rapidity()) < 2.4
        deltaPhiCut = abs(deltaPhi)>2.1
        passType11KinCuts   = ptCuts and etaCuts and deltaPhiCut

        if ptCuts:
            self.cutflow.Fill(1.5,1)  
            if etaCuts:
                self.cutflow.Fill(2.5,1)  
                if deltaPhiCut:
                    self.cutflow.Fill(3.5,1) 
                    topMassCuts = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMass[1] > 140 and topJetMass[1] < 250   
                    if topMassCuts:
                        self.cutflow.Fill(4.5,1)
                        nSubjetsCuts = topJetNSubjets[0] > 2 and topJetNSubjets[1] > 2
                        if nSubjetsCuts:
                            self.cutflow.Fill(5.5,1)
                            minMassCuts = topJetMinMass[0] > 50 and topJetMinMass[1] > 50
                            if minMassCuts:
                                self.cutflow.Fill(6.5,1)
 

        if passType11KinCuts :

            topTag0        = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
            topTag1        = topJetMass[1] > 140 and topJetMass[1] < 250 and topJetMinMass[1] > 50 and topJetNSubjets[1] > 2
            passType11     = topTag0 and topTag1
            ttMass   = (topJets[0]+topJets[1]).mass()
            
            myrand = ROOT.gRandom.Uniform(140,250)
            jet0P4_massFlat = copy.copy(topJets[0])
            jet0P4_massFlat.SetM( myrand )
            ttMassJet0MassFlat = (topJets[1]+jet0P4_massFlat).mass()
            
            myrand2 = ROOT.gRandom.Uniform(140,250)
            jet1P4_massFlat = copy.copy(topJets[1])
            jet1P4_massFlat.SetM( myrand2 )
            ttMassJet1MassFlat = (topJets[0]+jet1P4_massFlat).mass()
           
            myrand_QCDdist_jet0 = self.modMassHist.GetRandom()
            jet0P4_modmassQCDdist = copy.copy(topJets[0])
            jet0P4_modmassQCDdist.SetM( myrand_QCDdist_jet0 )
            ttMassJet0modmassQCDdist = (topJets[1]+jet0P4_modmassQCDdist).mass()
            

            myrand_QCDdist_jet1 = self.modMassHist.GetRandom()
            jet1P4_modmassQCDdist = copy.copy(topJets[1])
            jet1P4_modmassQCDdist.SetM( myrand_QCDdist_jet1 )
            ttMassJet1modmassQCDdist = (topJets[0]+jet1P4_modmassQCDdist).mass()
		    
            #ibin0 = self.triggerHist.FindBin(topJets[0].pt())
		    #jetTriggerWeight = self.triggerHist.GetBinContent(bin0)

            ttMassMod3Jet0Flat = ttMass
            ttMassMod3Jet1Flat = ttMass
            if topJets[0].mass() < 140 or topJets[0].mass() > 250:
                ttMassMod3Jet0Flat = ttMassJet0MassFlat
            if topJets[1].mass() < 140 or topJets[1].mass() > 250:
                ttMassMod3Jet1Flat = ttMassJet1MassFlat
           
            ttMassModJet0QCDdist = ttMass
            ttMassModJet1QCDdist = ttMass
            if topJets[0].mass() < 140 or topJets[0].mass() > 250:
                ttMassModJet0QCDdist = ttMassJet0modmassQCDdist
            if topJets[1].mass() < 140 or topJets[1].mass() > 250:
                ttMassModJet1QCDdist = ttMassJet1modmassQCDdist




            self.jetMass.Fill( topJets[0].mass(), weight )
            self.jetMass.Fill( topJets[1].mass(), weight )
            self.jetPt.Fill( topJets[0].pt(), weight )
            self.jetPt.Fill( topJets[1].pt(), weight )
            self.jetEta.Fill( topJets[0].eta(), weight )
            self.jetEta.Fill( topJets[1].eta(), weight )
            self.jetRap.Fill( topJets[0].Rapidity(), weight )
            self.jetRap.Fill( topJets[1].Rapidity(), weight )
            self.jetMinMass.Fill( topJetMinMass[0], weight )
            self.jetMinMass.Fill( topJetMinMass[1], weight )
            self.mttCandMass.Fill( ttMass, weight )
            

            if passType11  :
                self.topTagMass.Fill( topJets[0].mass(), weight )
                self.topTagMass.Fill( topJets[1].mass(), weight )
                self.topTagPt.Fill( topJets[0].pt(), weight )
                self.topTagPt.Fill( topJets[1].pt(), weight )
                self.topTagMinMass.Fill( topJetMinMass[0], weight )
                self.topTagMinMass.Fill( topJetMinMass[1], weight )
                self.mttMass.Fill( ttMass, weight )
                h_mtt = Handle("double")
                event.getByLabel( ("ttbsmAna", "mttgen"), h_mtt)
                if h_mtt.isValid():
                    mtt = h_mtt.product()
                    self.mtt_gen.Fill(mtt[0])
                    self.mtt_gen_vs_reco.Fill(mtt[0], ttMass)

                if not self.useMC :
                    self.runPairs.append( [event.object().id().run(),
                                           event.object().id().event(),
                                           event.object().id().luminosityBlock() ,
                                           ttMass] )
                self.mttMassTriggerWeighted.Fill( ttMass, weight )   

            #background estiation
            x = ROOT.gRandom.Uniform()        
            if x < 0.5 :
                if topTag0 :
                    self.jetPtOneTag.Fill( topJets[1].pt(), weight )
                    self.jetRapOneTag.Fill( topJets[1].Rapidity(), weight )
                    self.jetMassOneTag.Fill( topJets[1].mass(), weight )
                    self.mttPredDist.             Accumulate( ttMass,             topJets[1].pt(), topTag1, weight )
                    self.mttPredDistMassCut.      Accumulate( ttMass,             topJets[1].pt(), topTag1, weight )
                    self.mttPredDistModMassFlat.  Accumulate( ttMassJet1MassFlat, topJets[1].pt(), topTag1, weight )
                    self.mttPredDistMod3MassFlat. Accumulate( ttMassMod3Jet1Flat, topJets[1].pt(), topTag1, weight )
                    self.mttPredDistMod3MassFlatSubtract. Accumulate( ttMassMod3Jet1Flat, topJets[1].pt(), topTag1, weight )
                    self.mttPredDistModMassQCDdistSubtract. Accumulate( ttMassModJet1QCDdist, topJets[1].pt(), topTag1, weight )
            if x >= 0.5 :
                if topTag1 :
                    self.jetPtOneTag.Fill( topJets[0].pt(), weight )
                    self.jetRapOneTag.Fill( topJets[0].Rapidity(), weight )
                    self.jetMassOneTag.Fill( topJets[0].mass(), weight )
                    self.mttPredDist.             Accumulate( ttMass,             topJets[0].pt(), topTag0, weight )
                    self.mttPredDistMassCut.      Accumulate( ttMass,             topJets[0].pt(), topTag0, weight )
                    self.mttPredDistModMassFlat.  Accumulate( ttMassJet0MassFlat, topJets[0].pt(), topTag0, weight )
                    self.mttPredDistMod3MassFlat. Accumulate( ttMassMod3Jet0Flat, topJets[0].pt(), topTag0, weight )
                    self.mttPredDistMod3MassFlatSubtract. Accumulate( ttMassMod3Jet0Flat, topJets[0].pt(), topTag0, weight )
                    self.mttPredDistModMassQCDdistSubtract. Accumulate( ttMassModJet0QCDdist, topJets[0].pt(), topTag0, weight )



