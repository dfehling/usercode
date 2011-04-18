import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useFlavorHistory',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Flavor History Mode")

options.register('sampleNameInput',
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('allSys',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all systematics (1) or just the central one (0)")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")


options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

inputDoMC=True

inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    '/store/user/makouski/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/shyft_414_v1/4102b2143a05266d07e3ed7d177f56c8/shyft_414patch1_mc_9_1_Z8F.root'
                                    )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    filelist.readlines()
                                    )
                                )

if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )

#_____________________________________PF__________________________________________________
process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),                                       
                                        jetPtMin = cms.double(30.0),##
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        jetAlgo = cms.string("pf"),
                                        simpleSFCalc = cms.bool(False),                                        
                                        reweightBTagEff = cms.bool(True),
                                        weightSFCalc = cms.bool(True),                                        
                                        useCustomPayload = cms.bool(False),
                                        bcEffScale = cms.double(1.00),
                                        lfEffScale = cms.double(1.00),
                                        jetSmear = cms.double(0.1),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )                                    
                                    )

#___________Special case of MET < 20 GeV_________________
process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MET <20'),
        metMin = cms.double(0.0),
        metMax = cms.double(20.0),
        )
    )

#___________no MET cut________________
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )

#______________To extract secvtx shapes and >=3 tag jets count _____________________

process.pfShyftAnaMC = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    )
    )

process.pfShyftAnaMCNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC no MET'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )

process.pfShyftAnaMCMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )

################################################
#_______________Systematics__________________
#################################################

#________________________btagging Systematics ____________________________

##HF

process.pfShyftAnaReweightedBTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 080'),
        bcEffScale = cms.double(0.80),        
        )
    )

process.pfShyftAnaReweightedBTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 090'),
        bcEffScale = cms.double(0.90),
        )
    )


process.pfShyftAnaReweightedBTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 110'),
        bcEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedBTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 120'),
        bcEffScale = cms.double(1.20),
        )
    )


##LF

process.pfShyftAnaReweightedLFTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 080'),
        lfEffScale = cms.double(0.80),
        )
    )

process.pfShyftAnaReweightedLFTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 090'),        
        lfEffScale = cms.double(0.90),
        )
    )

process.pfShyftAnaReweightedLFTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 110'),     
        lfEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedLFTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 120'),
        lfEffScale = cms.double(1.20)
        )
    )

#____________________JES up and down _______________________

process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(-1.0),
        jetUncertainty = cms.double(0.036),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.0),
        jetUncertainty = cms.double(0.036),
        identifier = cms.string('PFJES105')
        )
    )

#____________________JER _______________________
process.pfShyftAnaJER000 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.00),
        identifier = cms.string('PFJER000')
        )
    )

process.pfShyftAnaJER020 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.20),
        identifier = cms.string('PFJER020')
        )
    )

#____________________MET Resolution _______________________
process.pfShyftAnaMETRES090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 0.90 ),
        identifier = cms.string('PFMETRES090')
        )
    )

process.pfShyftAnaMETRES110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 1.10 ),
        identifier = cms.string('PFMETRES110')
        )
    )

process.pfShyftAnaEleEEPt125 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt125')
        )
    )

process.pfShyftAnaEleEEPt075 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(-1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt075')
        )
    )

process.s = cms.Sequence(
   process.pfShyftAna*                 
   process.pfShyftAnaNoMET*
   process.pfShyftAnaJES095*    
   process.pfShyftAnaJES105*
   process.pfShyftAnaMETRES090*
   process.pfShyftAnaMETRES110*
   process.pfShyftAnaJER000*
   process.pfShyftAnaJER020*
   process.pfShyftAnaEleEEPt125*
   process.pfShyftAnaEleEEPt075* 
   process.pfShyftAnaReweightedBTag080*
   process.pfShyftAnaReweightedBTag090*
   process.pfShyftAnaReweightedBTag110*
   process.pfShyftAnaReweightedBTag120*
   process.pfShyftAnaReweightedLFTag080*
   process.pfShyftAnaReweightedLFTag090*
   process.pfShyftAnaReweightedLFTag110*
   process.pfShyftAnaReweightedLFTag120*
   process.pfShyftAnaMC*
   process.pfShyftAnaMCNoMET*
   process.pfShyftAnaMETMax20*
   process.pfShyftAnaMCMETMax20
    )

process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaMC
    )

if options.allSys == 1 :
    process.p *= process.s

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
