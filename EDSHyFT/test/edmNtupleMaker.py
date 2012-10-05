import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMNtuple")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
import sys
#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")
options.register ('runData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "if running over data (1) else (0)")
options.register('eleEt',
                  30.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")

options.register('runLoose',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run extra sequence(1) for loose selction  or ignore them (0)")
                 
options.parseArguments()

print options

if options.runData == 1:
    runData = True
else: runData  = False

runNoEleID = options.runLoose

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source    
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
   # '/store/user/b2g12006/bazterra/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_1001_1_eOl.root',
#   '/store/user/lpctlbsm/jpilot/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_53x_mc_105_1_sFj.root'
   '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_10_3_lNR.root'
  #  '/store/user/b2g12006/agarabed/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v1_TLBSM_52x_v5/2bcc6fdd1e664d93e9026c3764d0b403/ttbsm_52x_mc_486_1_xai.root'
  #'/store/user/b2g12006/peiffer/peiffer/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12-PU_S7_START52_V9-v2_TLBSM_52x_v5/2bcc6fdd1e664d93e9026c3764d0b403/ttbsm_52x_mc_9_1_ZnS.root'

 #'/store/results/B2G/SingleElectron/StoreResults-Run2012A-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/SingleElectron/USER/StoreResults-Run2012A-PromptReco-v1_TLBSM_52x_v5-37420123b49b4f52358fad22bcc775a4/0000/94340698-D6F7-E111-80B4-001A92971B30.root',    
    )
                            )                           

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

if runData:
    process.GlobalTag.globaltag = 'GR_P_V40_AN1::All'
else:
    process.GlobalTag.globaltag = 'START53_V7::All'
    #process.GlobalTag.globaltag = 'START53_V11::All'

process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

# apply the JEC on fly
payloads = [
    'Jec12_V2_L1FastJet_AK5PFchs.txt',
    'Jec12_V2_L2Relative_AK5PFchs.txt', 
    'Jec12_V2_L3Absolute_AK5PFchs.txt',
    'Jec12_V2_L2L3Residual_AK5PFchs.txt',
    'Jec12_V2_Uncertainty_AK5PFchs.txt',   
]

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis
#_______________________________BTagging SF and Pileup________________________________________

process.load("CondCore.DBCommon.CondDBCommon_cfi")

# Final 2011 b-tag performance measurements
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB062012")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB062012")

if not runData:
    process.pileupReweightingProducer = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(False),
                                         oneDReweighting = cms.untracked.bool(True),
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
                                                       )

    # creates value maps to jets as userInt index:
    #-1 -- ignore, 1 -- right out of the box, 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.    
    process.goodPatJetsPFlowSF = cms.EDProducer("BTaggingSFProducer",
        JetSource = cms.InputTag('goodPatJetsPFlow'),
        DiscriminatorTag = cms.string('combinedSecondaryVertexBJetTags'),
        DiscriminatorValue = cms.double(0.679),
        BTagger = cms.string('CSVM'),
        HeavySFUncInflateBy = cms.double(1.5),
        LightSFCorrFunction = cms.string('1.10422 + (-0.000523856*x) + (1.14251e-06*x*x)'),
        EffMapB = cms.string('Analysis/EDSHyFT/data/BprimeBprimeToTWTWinc_bTaggingEfficiencyMap_b.root'),
        EffMapC = cms.string('Analysis/EDSHyFT/data/BprimeBprimeToTWTWinc_bTaggingEfficiencyMap_c.root'),
        EffMapUDSG = cms.string('Analysis/EDSHyFT/data/BprimeBprimeToTWTWinc_bTaggingEfficiencyMap_udsg.root')
    )


    process.GenInfo = cms.EDProducer('BoostedParticles')
    
#_____________________________________PF__________________________________________________


from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput

process.pfTupleEle = cms.EDFilter('EDSHyFTSelector',
                                  shyftSelection = shyftSelectionInput.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( True ),
    muPlusJets = cms.bool( False ),
    eEt = cms.double(options.eleEt),
    jetPtMin = cms.double(30.0),
    minJets = cms.int32(1),
    useNoPFIso = cms.bool(True),
    useNoID  = cms.bool(True),
    useData = cms.bool(runData),
    identifier = cms.string('AK5 PF'),
    cutsToIgnore=cms.vstring(inputCutsToIgnore),
    jecPayloads = cms.vstring( payloads ),
    ),
                                  matchByHand = cms.bool(False),
                                  )


process.pfTupleC8APruned = process.pfTupleEle.clone()
process.pfTupleC8APruned.shyftSelection.jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF')
process.pfTupleC8APruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleC8APruned.matchByHand = cms.bool(True)


## configure output module
process.p0 = cms.Path( process.patTriggerDefaultSequence)
process.p1 = cms.Path( process.pfTupleEle)
process.p2 = cms.Path( process.pfTupleC8APruned)


process.p3 = cms.Path()

if not runData:
    process.p3 = cms.Path( process.pileupReweightingProducer * process.goodPatJetsPFlowSF * process.GenInfo)
    
process.out = cms.OutputModule("PoolOutputModule",
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring( 'p0', 'p1', 'p2', 'p3') ),
                               fileName =  cms.untracked.string('edmTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfTuple*_*_*',
                                                                      'keep *_patTriggerEvent_*_*',
                                                                      'keep *_patTrigger_*_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'drop *_pfTupleC8APruned_*_*',
                                                                      'keep *_pfTupleC8APruned_jets_*',
                                                                      'keep *_pfTupleC8APruned_MET_*',
                                                                      'keep *_caPrunedPFlow_SubJets_*'
                                                                      ),
                               )
if not runData:
    process.out.outputCommands += [
                               #'keep *_prunedGenParticles_*_*',
                               'keep *_GenInfo*_*_*',
                               'keep *_*_pileupWeights_*',
                               'keep PileupSummaryInfos_*_*_*',
                               ]

## output path
process.outpath = cms.EndPath(process.out)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
