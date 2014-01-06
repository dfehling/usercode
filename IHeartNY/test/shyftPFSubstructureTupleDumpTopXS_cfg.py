import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")
#!!!Change below 0 to 1
options.register('muOrEle',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use muons (0) or electrons (1)")


options.register('useData',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Use data (1) or MC (0)")



options.parseArguments()

#print options

import sys
#!!!Change PoolSource 'dcap...' to '/store/results/B2G/SingleElectron/StoreResults-Run2012D-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/SingleElectron/USER/StoreResults-Run2012D-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/0000/0219E2CF-3DE8-E211-B880-003048FFD754.root'

if options.useData == 0 : 
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    '/store/results/B2G/TT_CT10_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3_bugfix_v1-99bd99199697666ff01397dad5652e9e/TT_CT10_TuneZ2star_8TeV-powheg-tauola/USER/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v3_bugfix_v1-99bd99199697666ff01397dad5652e9e/0000/002079E2-81CD-E211-B071-002590593878.root'
                                    )
        )
else : 
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    '/store/results/B2G/SingleMu/StoreResults-Run2012A-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/SingleMu/USER/StoreResults-Run2012A-22Jan2013-v1_TLBSM_53x_v3-db7dd8e58134469d4e102fe8d5e205b6/0000/00752EA1-DEBB-E211-8988-002590593878.root'
                                    )
        )


payloadsData = [
            'FT_53_V21_AN6_L1FastJet_AK5PFchs.txt',
            'FT_53_V21_AN6_L2Relative_AK5PFchs.txt',
            'FT_53_V21_AN6_L3Absolute_AK5PFchs.txt',
            'FT_53_V21_AN6_L2L3Residual_AK5PFchs.txt',
            'FT_53_V21_AN6_Uncertainty_AK5PFchs.txt'
                ]

payloadsMC = [
    'START53_V27_L1FastJet_AK5PFchs.txt',
    'START53_V27_L2Relative_AK5PFchs.txt',
    'START53_V27_L3Absolute_AK5PFchs.txt',
    'START53_V27_Uncertainty_AK5PFchs.txt'
]

if options.useData :
    payloads = payloadsData
else :
    payloads = payloadsMC


## process.source = cms.Source("PoolSource",
##                             fileNames = cms.untracked.vstring(
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_10_1_5eL.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_11_1_y36.root',
## 'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/vasquez/TTJets_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_12_1_RFD.root'

## )
## )



from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.ignoreTrigger :
    process.hltSelection = cms.Sequence()
else :
    process.hltSelectionMu = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = ['HLT_Mu40_eta2p1_v*'
                                                                                                       ])
    process.hltSelectionEle = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths =  ['HLT_Ele30_CaloIdVT_TrkIdT_PFNoPUJet100_PFNoPUJet25_v*'
                                                                                                          ])

    process.hltSelectionMu.throw = False
    process.hltSelectionEle.throw = False

    if options.muOrEle :
        process.hltSelection = cms.Sequence( ~process.hltSelectionMu * process.hltSelectionEle )
    else :
        process.hltSelection = cms.Sequence( process.hltSelectionMu )


## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.SHyFT.shyftPFSelection_cfi import shyftPFSelection as shyftPFSelectionInput

process.pileup = cms.EDFilter('PileUpProducer',
                                pvSrc = cms.InputTag('goodOfflinePrimaryVertices')

)
#!!!Change below doElectrons .. False to True
process.pfShyftProducerAK5 = cms.EDFilter('EDSHyFTPFSelector',
                                    shyftPFSelection = shyftPFSelectionInput.clone(
                                           jetSrc = cms.InputTag('goodPatJetsPFlow'),
    					   rhoSrc = cms.InputTag('kt6PFJets', 'rho'),
					   doElectrons = cms.bool(False),
                                           jecPayloads = cms.vstring( payloads )
                                        )
                                    )
#!!!Change below doElectrons from False to True
process.pfShyftProducerAK5Loose = cms.EDFilter('EDSHyFTPFSelector',
                                            shyftPFSelection = shyftPFSelectionInput.clone(
                                                jetSrc = cms.InputTag('goodPatJetsPFlow'),
                                                muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                                electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose'),
						doElectrons = cms.bool(False),
    					   	rhoSrc = cms.InputTag('kt6PFJets', 'rho'),
                                                jecPayloads = cms.vstring( payloads ),
                                                removeLooseLep = cms.bool(True)
                                                )
                                            )

process.pfShyftProducerAK5Loose.shyftPFSelection.cutsToIgnore.append('== 1 Tight Lepton')
process.pfShyftProducerAK5Loose.shyftPFSelection.cutsToIgnore.append('0 other lepton')
process.pfShyftProducerAK5Loose.shyftPFSelection.cutsToIgnore.append('>=1 Jets')
process.pfShyftProducerAK5Loose.shyftPFSelection.muonIdPFTight.cutsToIgnore.append('maxPfRelIso')
process.pfShyftProducerAK5Loose.shyftPFSelection.electronIdPFTight.cutsToIgnore.append('PFIso')


## std sequence to produce the kinematic fit for semi-leptonic events
process.load('TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi')
#!!!Uncomment below line and comment out above
#process.load('TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Electrons_cfi')

process.kinFitTtSemiLepEvent.jets = cms.InputTag("pfShyftProducerAK5", "jets")
process.kinFitTtSemiLepEvent.mets = cms.InputTag("pfShyftProducerAK5", "MET")
process.kinFitTtSemiLepEvent.leps = cms.InputTag("pfShyftProducerAK5", "muons")
#!!!Uncomment below line and comment out above
#process.kinFitTtSemiLepEvent.leps = cms.InputTag("pfShyftProducerAK5", "electrons")

process.load("TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi")
#!!!Uncomment below line and comment out above
#process.load("TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Electrons_cfi")

process.pfShyftTupleJetsAK5 = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5", "jets"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("csv"),
            quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        )
    )

process.pfShyftTupleJetsLooseAK5 = process.pfShyftTupleJetsAK5.clone(
    src = cms.InputTag("pfShyftProducerAK5Loose", "jets"),
    )




process.pfShyftTupleJetsLooseCA8Pruned = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("goodPatJetsCA8PrunedPFPacked"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("nSubjets"),
            quantity = cms.untracked.string("numberOfDaughters()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Pt"),
            quantity = cms.untracked.string("daughter(0).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Eta"),
            quantity = cms.untracked.string("daughter(0).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Phi"),
            quantity = cms.untracked.string("daughter(0).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da0Mass"),
            quantity = cms.untracked.string("daughter(0).mass()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Pt"),
            quantity = cms.untracked.string("daughter(1).pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Eta"),
            quantity = cms.untracked.string("daughter(1).eta()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Phi"),
            quantity = cms.untracked.string("daughter(1).phi()")
            ),
        cms.PSet(
            tag = cms.untracked.string("da1Mass"),
            quantity = cms.untracked.string("daughter(1).mass()")
            )
        )
    )


process.pfShyftTupleJetsLooseTopTag = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("goodPatJetsCATopTagPFPacked"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("nSubjets"),
            quantity = cms.untracked.string("numberOfDaughters()")
            ),
        cms.PSet(
            tag = cms.untracked.string("minMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().minMass : 0.0")
            ),
        cms.PSet(
            tag = cms.untracked.string("topMass"),
            quantity = cms.untracked.string("? hasTagInfo('CATop') ? tagInfo('CATop').properties().topMass : 0.0")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0csv"),
	    quantity = cms.untracked.string("daughter(0).bDiscriminator('combinedSecondaryVertexBJetTags')")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3csv"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).bDiscriminator('combinedSecondaryVertexBJetTags') : -1")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0pt"),
	    quantity = cms.untracked.string("daughter(0).pt()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).pt() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).pt() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3pt"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).pt()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0eta"),
	    quantity = cms.untracked.string("daughter(0).eta()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).eta() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).eta() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3eta"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).eta()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0phi"),
	    quantity = cms.untracked.string("daughter(0).phi()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).phi() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).phi() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3phi"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).phi()  : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj0mass"),
	    quantity = cms.untracked.string("daughter(0).mass()")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj1mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 1 ? daughter(1).mass() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj2mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 2 ? daughter(2).mass() : -1000")
            ),
	cms.PSet(
	    tag = cms.untracked.string("topsj3mass"),
	    quantity = cms.untracked.string("? numberOfDaughters() > 3 ? daughter(3).mass()  : -1000")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        )
    )


process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5", "muons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "userIsolation('pat::PfNeutralHadronIso') + " +
                                            "userIsolation('pat::PfGammaIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
	cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::PfPUChargedHadronIso') )"
                                            )
            ),
        )
    )

process.pfShyftTupleMuonsLoose = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5Loose", "muons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "userIsolation('pat::PfNeutralHadronIso') + " +
                                            "userIsolation('pat::PfGammaIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPU"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso') + " +
                                            "max(0.0,  userIsolation('pat::PfNeutralHadronIso') + userIsolation('pat::PfGammaIso') - 0.5 * userIsolation('pat::PfPUChargedHadronIso') )"
                                            )
            ),
        )
    )

process.pfShyftTupleMET = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5", "MET"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            )
        )
    )

process.pfShyftTupleMETLoose = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5Loose", "MET"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            )
        )
    )


process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5", "electrons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("ptECAL"),
            quantity = cms.untracked.string("ecalDrivenMomentum().pt()")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )
    )

process.pfShyftTupleElectronsLoose = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("pfShyftProducerAK5Loose", "electrons"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoCH"),
            quantity = cms.untracked.string("userIsolation('pat::PfChargedHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoNH"),
            quantity = cms.untracked.string("userIsolation('pat::PfNeutralHadronIso')"
                                            )
            ),
        cms.PSet(
            tag = cms.untracked.string("pfisoPH"),
            quantity = cms.untracked.string("userIsolation('pat::PfGammaIso')"
                                            )
            ),
        )
    )

process.nsub = cms.EDProducer("NjettinessAdder",
                              #src=cms.InputTag("goodPatJetsCA8PrunedPFPacked"),
                              src=cms.InputTag("goodPatJetsCA8PF"),
                              cone=cms.double(0.8)
                              )

 #################### keep generator-level products #####################


process.topQuarks = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("prunedGenParticles"),
    cut = cms.string("status == 3 && abs(pdgId) == 6")
)

process.pfShyftTupleTopQuarks = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("topQuarks"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            )
        )
    )

process.pfShyftTupleGenParticles = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("prunedGenParticles"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("status"),
            quantity = cms.untracked.string("status")
            ),
        cms.PSet(
            tag = cms.untracked.string("pdgId"),
            quantity = cms.untracked.string("pdgId")
            )
        )
    )

process.pfShyftTupleCA8GenJets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("ca8GenJetsNoNu"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            )
        )
    )


process.pfShyftTupleAK5GenJets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("ak5GenJetsNoNu"),
    lazyParser = cms.untracked.bool(True),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            )
        )
    )


process.p1 = cms.Path(
    process.hltSelection*
    process.pileup*
    process.pfShyftProducerAK5Loose *
    process.pfShyftTupleJetsLooseAK5*
    process.pfShyftTupleJetsLooseTopTag*
    process.pfShyftTupleJetsLooseCA8Pruned*
    process.nsub*
    process.pfShyftTupleMuonsLoose*
    process.pfShyftTupleElectronsLoose*
    process.pfShyftTupleMETLoose*
    process.pfShyftTupleMETLoose*
    process.topQuarks*
    process.pfShyftTupleTopQuarks*
    process.pfShyftTupleGenParticles*
    process.pfShyftTupleCA8GenJets*
    process.pfShyftTupleAK5GenJets
    )

process.p2 = cms.Path(
    process.hltSelection*
    process.pfShyftProducerAK5*
    process.pfShyftTupleJetsAK5*
    process.pfShyftTupleMuons*
    process.pfShyftTupleElectrons*
    process.pfShyftTupleMET*
    process.topQuarks*
    process.pfShyftTupleTopQuarks*
    process.pfShyftTupleGenParticles*
    process.pfShyftTupleCA8GenJets*
    process.pfShyftTupleAK5GenJets
    )

if options.useData == 1 :
    process.p1.remove( process.topQuarks )
    process.p1.remove( process.pfShyftTupleTopQuarks )
    process.p1.remove( process.pfShyftTupleGenParticles )
    process.p1.remove( process.pfShyftTupleCA8GenJets )
    process.p1.remove( process.pfShyftTupleAK5GenJets )
    process.p2.remove( process.topQuarks )
    process.p2.remove( process.pfShyftTupleTopQuarks )
    process.p2.remove( process.pfShyftTupleGenParticles )
    process.p2.remove( process.pfShyftTupleCA8GenJets )
    process.p2.remove( process.pfShyftTupleAK5GenJets )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000




process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyft_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p1', 'p2') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      #'keep *_pfShyftProducerAK5_*_*',
                                                                      'keep double_*_rho_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_nsub*_*_*',
                                                                      'keep *_generator_*_*',
                                                                      'keep *_pileup*_*_*'
                                                                      #'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      )
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
