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
        jetEtaMax = cms.double(2.4),
        jetScale=cms.double(1.0),
        minJets = cms.int32(5)
        ) ,
    sampleName = cms.string("top"),
    heavyFlavour = cms.bool(False),
    doMC           = cms.bool(False),
    doBTagPerformance = cms.bool(True),
    payload = cms.string( "PayLoad.root" ),
    bPerformanceTag = cms.string( "MCSSVMb" ),
    cPerformanceTag = cms.string( "MCSSVMc" ),
    lPerformanceTag = cms.string( "MCSSVMl" ),
    btaggerString = cms.string('simpleSecondaryVertexHighEffBJetTags'),
    identifier = cms.string('Douglas Adams'),
    reweightPDF = cms.bool(False),
    pdfSrc = cms.InputTag('generator'),
    pdfToUse = cms.string('cteq6ll.LHpdf'),
    pdfVariation = cms.int32(1),
#    pdfUsed = cms.string('cteq61'),
#    pdfSetNames = cms.vstring( [
#        'cteq61',
#        'cteq6AB',
#        'MRST2007lomod'
#        , "cteq65"
#        , "MRST2006nnlo"
#        , "MRST2007lomod"
#        
#        ] ),
    doTagWeight = cms.bool(False),
    bcEffScale = cms.double(1.0),
    lfEffScale = cms.double(1.0),
    useDefaultDiscriminant = cms.bool(True),
    bDiscriminantCut = cms.double(1.74),
    cDiscriminantCut = cms.double(-1),
    lDiscriminantCut = cms.double(-1),
    useCustomPayload = cms.bool(False),
    jetAlgo = cms.string("calo"),
    customPayload = cms.string('ttbarEffSF.root')
    
#    btaggerString = cms.string('simpleSecondaryVertexBJetTags')
)

