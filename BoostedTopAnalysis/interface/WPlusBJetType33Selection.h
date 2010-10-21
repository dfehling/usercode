#ifndef Analysis_BoostedTopAnalysis_interface_WPlusBJetType33Selection_h
#define Analysis_BoostedTopAnalysis_interface_WPlusBJetType33Selection_h

#include "PhysicsTools/SelectorUtils/interface/EventSelector.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/ShallowClonePtrCandidate.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "Analysis/BoostedTopAnalysis/interface/WPlusBJetEventSelector.h"
#include "Math/GenVector/PxPyPzM4D.h"

using namespace std;

class WPlusBJetType33Selection : public EventSelector {

  public :
    WPlusBJetType33Selection( edm::ParameterSet const & params );
    virtual ~WPlusBJetType33Selection() { } //twPlusBJetSelection_.print(cout); owPlusBJetSelection_.print(cout); }
    virtual bool operator() ( edm::EventBase const & t, pat::strbitset & ret );
    std::vector<edm::Ptr<pat::Jet> >    const & wJet0 () const {  return twPlusBJetSelection_.wJets(); }
    std::vector<edm::Ptr<pat::Jet> >    const & wJet1 () const {  return owPlusBJetSelection_.wJets(); }
    std::vector<edm::Ptr<pat::Jet> >    const & bJet0 () const {  return twPlusBJetSelection_.bJets(); }
    std::vector<edm::Ptr<pat::Jet> >    const & bJet1 () const {  return owPlusBJetSelection_.bJets(); }
    std::vector<edm::Ptr<pat::Jet> >  const &  minDrPair0 () const {  return twPlusBJetSelection_.minDrPair(); }
    std::vector<edm::Ptr<pat::Jet> >  const &  minDrPair1 () const {  return owPlusBJetSelection_.minDrPair(); }
    std::vector<edm::Ptr<pat::Jet> >  const &  pfJets() const { return pfJets_ ; }
    reco::Candidate::LorentzVector  const & p4_top0() const { return p4_top0_; }
    reco::Candidate::LorentzVector  const & p4_top1() const { return p4_top1_; }

  private :
    edm::InputTag               jetTag_;
    edm::InputTag               trigSrc_;
    std::string                 trig_;
    double    leadJetPtCut_;
    double    wMassMin_;
    double    wMassMax_;
    double    topMassMin_;
    double    topMassMax_;
    double    jetPt_;
    double    jetEta_;
    WPlusBJetEventSelector    twPlusBJetSelection_; //towards direction selector
    WPlusBJetEventSelector    owPlusBJetSelection_; //opposite direction selector
    std::vector<edm::Ptr<pat::Jet> >           pfJets_;
    reco::Candidate::LorentzVector p4_top0_;
    reco::Candidate::LorentzVector p4_top1_;

};


#endif
