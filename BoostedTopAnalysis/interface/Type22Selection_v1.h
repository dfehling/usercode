#ifndef Analysis_BoostedTopAnalysis_interface_Type22Selection_v1_h
#define Analysis_BoostedTopAnalysis_interface_Type22Selection_v1_h

#include "PhysicsTools/SelectorUtils/interface/EventSelector.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"

using namespace std;

class Type22Selection_v1 : public EventSelector {
  public :
    Type22Selection_v1( edm::ParameterSet const & params );
    virtual ~Type22Selection_v1() { }
    virtual bool operator() ( edm::EventBase const & t, pat::strbitset & ret );

  private :
    edm::ParameterSet const &                    pfJetIdParams_;
    boost::shared_ptr<PFJetIDSelectionFunctor>   pfJetSel_;
    BoostedTopWTagFunctor                        wJetSelector_;
    double      jetPt0_, jetPt1_;
    double      jetEta_;
    double      bTagOP_;
    string      bTagAlgo_;
    edm::InputTag                               jetTag_;
    std::vector<edm::Ptr<pat::Jet> >            pfJets_ ;
    std::vector<edm::Ptr<pat::Jet> >            highPtJets_;
    std::vector<edm::Ptr<pat::Jet> >            wTags_;
    std::vector<edm::Ptr<pat::Jet> >            bTags_;

};

#endif
