import FWCore.ParameterSet.Config as cms


from PhysicsTools.SelectorUtils.wplusjetsAnalysis_cfi import wplusjetsAnalysis

shyftAnalysis = cms.PSet(
    wplusjetsAnalysis.clone(     
        muonSrc = cms.InputTag('selectedPatMuons'),
        electronSrc = cms.InputTag('selectedPatElectrons'),
        jetSrc = cms.InputTag('selectedPatJets'),
        metSrc = cms.InputTag('patMETs'),
        trigSrc = cms.InputTag('patTriggerEvent'),
        jetPtMin = cms.double(30.0),
        jetEtaMax = cms.double(2.4)
        ) ,
    sampleName = cms.string("top"),
    mode = cms.int32(0),
    heavyFlavour = cms.bool(False),
    doMC           = cms.bool(False),
    payload = cms.string( "PayLoad.root" ),
    bPerformanceTag = cms.string( "MCSSVMb" ),
    cPerformanceTag = cms.string( "MCSSVMc" ),
    lPerformanceTag = cms.string( "MCSSVMl" ),
    btaggerString = cms.string('simpleSecondaryVertexHighEffBJetTags')
)
