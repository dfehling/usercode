#ifndef EDMultijetAnalysis_h
#define EDMultijetAnalysis_h

#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "Analysis/JetAnalysis/interface/JetStudies2011.h"

typedef edm::AnalyzerWrapper<JetStudies2011>   EDJetStudies2011;


DEFINE_FWK_MODULE(EDJetStudies2011);



#endif
