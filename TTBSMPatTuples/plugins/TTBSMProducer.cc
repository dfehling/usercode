// -*- C++ -*-
//
// Package:    TTBSMProducer
// Class:      TTBSMProducer
// 
/**\class TTBSMProducer TTBSMProducer.cc Analysis/TTBSMProducer/src/TTBSMProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Mon Jan 17 21:44:07 CST 2011
// $Id: TTBSMProducer.cc,v 1.10 2011/12/01 15:54:57 guofan Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerPath.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/SubjetHelper.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"
#include "Analysis/BoostedTopAnalysis/interface/CATopTagFunctor.h"
#include "Analysis/BoostedTopAnalysis/interface/BoostedTopWTagFunctor.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"


namespace LHAPDF {
      void initPDFSet(int nset, const std::string& filename, int member=0);
      int numberPDF(int nset);
      void usePDFMember(int nset, int member);
      double xfx(int nset, double x, double Q, int fl);
      double getXmin(int nset, int member);
      double getXmax(int nset, int member);
      double getQ2min(int nset, int member);
      double getQ2max(int nset, int member);
      void extrapolate(bool extrapolate=true);
}

//
// class declaration
//

class TTBSMProducer : public edm::EDFilter {
   public:
      explicit TTBSMProducer(const edm::ParameterSet&);
      ~TTBSMProducer();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
  edm::InputTag             wTagSrc_; 
  edm::InputTag             topTagSrc_;
  edm::InputTag             trigSrc_;
  edm::InputTag   rhoSrc_;          /// mean pt per unit area
  edm::InputTag   pvSrc_;           /// primary vertex
  std::vector<std::string>  trigs_;
  std::string               topTagName_;
  CATopTagFunctor           topTagFunctor_;
  BoostedTopWTagFunctor     wTagFunctor_;
  bool                      readTrig_;
  double                    scale_;
  double                    smear_;
  double                    etaSmear_;


  std::vector<std::string>  jecPayloads_; /// files for JEC payloads
  std::string               pdfSet_; /// lhapdf string

  boost::shared_ptr<JetCorrectionUncertainty> jecUnc_;
  boost::shared_ptr<FactorizedJetCorrector> jec_;



};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
TTBSMProducer::TTBSMProducer(const edm::ParameterSet& iConfig) :
  wTagSrc_      (iConfig.getParameter<edm::InputTag>("wTagSrc") ),
  topTagSrc_    (iConfig.getParameter<edm::InputTag>("topTagSrc") ),
  trigSrc_      (iConfig.getParameter<edm::InputTag>("trigSrc") ),
  rhoSrc_       ( iConfig.getParameter<edm::InputTag>("rhoSrc")),
  pvSrc_        ( iConfig.getParameter<edm::InputTag>("pvSrc")),
  trigs_        (iConfig.getParameter<std::vector<std::string> > ("trigs") ),
  topTagName_   (iConfig.getParameter<edm::ParameterSet>("topTagParams").getParameter<std::string>("tagName") ),
  topTagFunctor_(iConfig.getParameter<edm::ParameterSet>("topTagParams")),
  wTagFunctor_  (iConfig.getParameter<edm::ParameterSet>("wTagParams")),
  readTrig_     (iConfig.getParameter<bool>("readTrig")),
  scale_        (iConfig.getParameter<double>( "jetScale" ) ),
  smear_        (iConfig.getParameter<double>( "jetPtSmear") ),
  etaSmear_     (iConfig.getParameter<double>( "jetEtaSmear") ),
  jecPayloads_  (iConfig.getParameter<std::vector<std::string> >  ("jecPayloads")),
  pdfSet_       (iConfig.getParameter<std::string> ("pdfSet") )
{

  // Get the factorized jet corrector. 
  // The payloads contain N elements, 
  // the Nth is the uncertainty, and the first N-1 elements are the
  // actual correction levels. 
  std::vector<JetCorrectorParameters> vPar;
  for ( std::vector<std::string>::const_iterator ipayload = jecPayloads_.begin(),
	  ipayloadEnd = jecPayloads_.end(); ipayload != ipayloadEnd - 1; ++ipayload ) {
    std::cout << "Adding payload " << *ipayload << std::endl;
    JetCorrectorParameters pars(*ipayload);
    vPar.push_back(pars);
  }

  jec_ = boost::shared_ptr<FactorizedJetCorrector> ( new FactorizedJetCorrector(vPar) );

  jecUnc_ = boost::shared_ptr<JetCorrectionUncertainty>( new JetCorrectionUncertainty(jecPayloads_.back()));


  //register your products
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4");  
  produces<std::vector<double> > ("topTagBDisc");
  produces<std::vector<int> >    ("topTagPartonFlavour");
  produces<std::vector<double> > ("wTagBDisc");
  produces<std::vector<int> >    ("wTagPartonFlavour");
  produces<std::vector<double> > ("wTagMu");
  produces<std::vector<int> >    ("wTagPass");
  produces<std::vector<double> > ("topTagMinMass");
  produces<std::vector<double> > ("topTagTopMass");
  produces<std::vector<double> > ("topTagNSubjets");
  produces<std::vector<int> >    ("topTagPass");
  produces<std::vector<int> >    ("prescales");
  produces<std::vector<int> >    ("trigIndex");
  produces<std::vector<int> >    ("myTrigIndex");
  produces<std::vector<std::string> > ("trigNames");
  produces<double> ("rho");
  produces<double> ("weight");
  produces<unsigned int>    ("npv");
  produces<int>    ("npvTrue");
  produces<double>   ("mttgen");

  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4Hemis0");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("wTagP4Hemis1");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4Hemis0");
  produces<std::vector<reco::Candidate::PolarLorentzVector> > ("topTagP4Hemis1");
  produces<std::vector<double> > ("wTagBDiscHemis0");
  produces<std::vector<int> >    ("wTagPartonFlavour0");
  produces<std::vector<double> > ("wTagMuHemis0");
  produces<std::vector<double> > ("topTagMinMassHemis0");
  produces<std::vector<int> >    ("topTagPartonFlavour0");
  produces<std::vector<double> > ("topTagTopMassHemis0");
  produces<std::vector<double> > ("topTagNSubjetsHemis0");
  produces<std::vector<int> >    ("topTagPassHemis0");
  produces<std::vector<double> > ("wTagBDiscHemis1");
  produces<std::vector<int> >    ("wTagPartonFlavour1");
  produces<std::vector<double> > ("wTagMuHemis1");
  produces<std::vector<double> > ("topTagMinMassHemis1");
  produces<std::vector<int> >    ("topTagPartonFlavour1");
  produces<std::vector<double> > ("topTagTopMassHemis1");
  produces<std::vector<double> > ("topTagNSubjetsHemis1");
  produces<std::vector<int> >    ("topTagPassHemis1");
  produces<int>                  ("jet3Hemis0");
  produces<int>                  ("jet3Hemis1");
  produces<std::vector<double> > ("pdfWeights");


  if ( pdfSet_ != "" )
    LHAPDF::initPDFSet(1, pdfSet_.c_str());
}


TTBSMProducer::~TTBSMProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
bool
TTBSMProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{


  
  edm::Handle< std::vector<reco::Vertex> > h_pv;
  iEvent.getByLabel( pvSrc_, h_pv );

  typedef std::vector<reco::Candidate::PolarLorentzVector> p4_vector;
  typedef reco::Candidate::PolarLorentzVector LorentzV;

  std::auto_ptr<p4_vector> wTagP4( new p4_vector() );
  std::auto_ptr<p4_vector> topTagP4( new p4_vector() );
  std::auto_ptr<std::vector<double> > wTagBDisc ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagBDisc ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMu ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    wTagPass ( new std::vector<int>() );
  std::auto_ptr<std::vector<double> > topTagMinMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMass ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjets ( new std::vector<double>() );
  std::auto_ptr<std::vector<int> >    topTagPass ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> >    prescales ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> >    trigIndex ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> >    myTrigIndex ( new std::vector<int>() );
  std::auto_ptr<std::vector<std::string> >    trigNames ( new std::vector<std::string>() );
  std::auto_ptr<double>               rho( new double(-1.0) );
  std::auto_ptr<double>               weight( new double(1.0) );
  std::auto_ptr<double>               mttgen( new double(1.0) );

  //The duplicate quantities by hemisphere
  std::auto_ptr<p4_vector> topTagP4Hemis0 ( new p4_vector() );
  std::auto_ptr<p4_vector> topTagP4Hemis1 ( new p4_vector() );
  std::auto_ptr<p4_vector> wTagP4Hemis0 ( new p4_vector() );
  std::auto_ptr<p4_vector> wTagP4Hemis1 ( new p4_vector() );
  std::auto_ptr<int> jet3Hemis0   ( new int(-1) );
  std::auto_ptr<int> jet3Hemis1   ( new int(-1) );
  std::auto_ptr<std::vector<double> > wTagBDiscHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagBDiscHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMuHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > wTagMuHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagMinMassHemis0 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagMinMassHemis1 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMassHemis0 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagTopMassHemis1 ( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjetsHemis0( new std::vector<double>() );
  std::auto_ptr<std::vector<double> > topTagNSubjetsHemis1( new std::vector<double>() );
  std::auto_ptr<std::vector<int> > topTagPassHemis0  ( new std::vector<int>() );
  std::auto_ptr<std::vector<int> > topTagPassHemis1  ( new std::vector<int>() );
  
  std::auto_ptr<unsigned int> npv( new unsigned int() );
  std::auto_ptr<int> npvTrue( new int() );
  std::auto_ptr<std::vector<double> > pdf_weights( new std::vector<double>() );

  // Number of reconstructed PV's
  *npv = h_pv->size();

  // Pileup reweighting in the MC
  *npvTrue = -1;
  if ( ! iEvent.isRealData() ) {
    edm::InputTag PileupSrc_ ("addPileupInfo");
    edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    iEvent.getByLabel(PileupSrc_, PupInfo);
    std::vector<PileupSummaryInfo>::const_iterator PVI;
    // (then, for example, you can do)
    for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
      int BX = PVI->getBunchCrossing();
      if(BX == 0) { 
	*npvTrue = PVI->getPU_NumInteractions();
	break;
      }
    }
  }

  edm::Handle<std::vector<reco::GenParticle> >   h_gen;
  iEvent.getByLabel( "prunedGenParticles", h_gen );
  if(h_gen.isValid())  {
    std::vector<const reco::GenParticle *>  genTop;
    for ( std::vector<reco::GenParticle>::const_iterator  igen = h_gen->begin(),
          genEnd = h_gen->end(); igen != genEnd; ++igen ) {
        if (fabs(igen->pdgId()) == 6)
          genTop.push_back( &(*igen) );
    }
    if (genTop.size() == 2) {
        *mttgen = (genTop[0]->p4() + genTop[1]->p4()).M();
    }
  }


  edm::Handle<std::vector<pat::Jet> > h_wTag;
  edm::Handle<std::vector<pat::Jet> > h_topTag;
  edm::Handle<pat::TriggerEvent>      h_trig;
  edm::Handle<double> h_rho;

  iEvent.getByLabel( rhoSrc_, h_rho );
  double rhoVal = *h_rho;


  iEvent.getByLabel( wTagSrc_, h_wTag );
  iEvent.getByLabel( topTagSrc_, h_topTag );

  pat::strbitset wTagRet = wTagFunctor_.getBitTemplate();
  pat::strbitset topTagRet = topTagFunctor_.getBitTemplate();
  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_wTag->begin(),
	  jetEnd = h_wTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {


    // -------
    // Jet energy corrections
    // -------
    reco::Candidate::LorentzVector uncorrJet = ijet->correctedP4(0);
    jec_->setJetEta( uncorrJet.eta() );
    jec_->setJetPt ( uncorrJet.pt() );
    jec_->setJetE  ( uncorrJet.energy() );
    jec_->setJetA  ( ijet->jetArea() );
    jec_->setRho   ( rhoVal );
    jec_->setNPV   ( h_pv->size() );
    double corr = jec_->getCorrection();


    // -------
    // Jet energy scale variation
    // -------
    if ( fabs(scale_) > 0.0001 ) {
      // Now get the uncertainties
      jecUnc_->setJetEta( uncorrJet.eta() );
      jecUnc_->setJetPt( uncorrJet.pt() * corr );
      double unc = fabs(jecUnc_->getUncertainty( bool(scale_ > 0) ));

      // Add the "flat" flavor dependent corrections in quadrature
      unc = sqrt( unc*unc + scale_*scale_);
      double sign = 1.0;
      if ( scale_ < 0.0 ) sign = -1.0;
	     
      // Scale up or down by jetScale_
      double ijetscale = (1 + sign * unc);
      corr *= ijetscale;
    }    

    // -------
    // Jet angular resolution smearing
    // -------
    double etaScale_ = 1.0;
    if( fabs(etaSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
      double recoeta = ijet->eta();
      double geneta = ijet->genJet()->eta();
      double deltaeta = (recoeta-geneta)*etaSmear_ ;
      etaScale_ = std::max((double)0.0,(recoeta+deltaeta)/recoeta);
    }


    double phiScale_ = 1.0;
    if( fabs(etaSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
      double recophi = ijet->phi();
      double genphi = ijet->genJet()->phi();
      double deltaphi = (recophi-genphi)*etaSmear_ ;
      phiScale_ = std::max((double)0.0,(recophi+deltaphi)/recophi);
    }


    // -------
    // Jet energy resolution smearing
    // -------
    double ptSmear_ = 1.0;
    if( fabs(smear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 )  {
      double recopt = ijet->pt();
      double genpt = ijet->genJet()->pt();
      double deltapt = (recopt-genpt)*smear_;
      ptSmear_ = std::max((double)0.0, (recopt+deltapt)/recopt);
    }

    reco::Candidate::PolarLorentzVector corrJet (uncorrJet.pt(), uncorrJet.eta(), uncorrJet.phi(), uncorrJet.mass());
    corrJet *=  (corr * ptSmear_);
    corrJet.SetEta( corrJet.eta() * etaScale_ );
    corrJet.SetPhi( corrJet.phi() * phiScale_ );

    wTagP4->push_back( corrJet );
    reco::Candidate::PolarLorentzVector corrDa0 = ijet->daughter(0)->polarP4() * (corr * ptSmear_);
    reco::Candidate::PolarLorentzVector corrDa1 = ijet->daughter(1)->polarP4() * (corr * ptSmear_);

    corrDa0.SetEta( corrDa0.eta() * etaScale_ );
    corrDa1.SetEta( corrDa1.eta() * etaScale_ );

    corrDa0.SetPhi( corrDa0.phi() * phiScale_ );
    corrDa1.SetPhi( corrDa1.phi() * phiScale_ );


    bool passedWTag = wTagFunctor_(*ijet, wTagRet);
    double y = -1.0, mu = -1.0, dR = -1.0;
    pat::subjetHelper( corrDa0, corrDa1, y, mu, dR, corrJet.mass() );
    wTagMu->push_back( mu );
    wTagPass->push_back( passedWTag );
    wTagBDisc->push_back( ijet->bDiscriminator("trackCountingHighEffBJetTags") );
  }

  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_topTag->begin(),
	  jetEnd = h_topTag->end(), ijet = jetBegin; ijet != jetEnd; ++ijet ) {

    // -------
    // Jet energy corrections
    // -------
    reco::Candidate::LorentzVector uncorrJet = ijet->correctedP4(0);
    jec_->setJetEta( uncorrJet.eta() );
    jec_->setJetPt ( uncorrJet.pt() );
    jec_->setJetE  ( uncorrJet.energy() );
    jec_->setJetA  ( ijet->jetArea() );
    jec_->setRho   ( rhoVal );
    jec_->setNPV   ( h_pv->size() );
    double corr = jec_->getCorrection();


    // -------
    // Jet energy scale variation
    // -------
    if ( fabs(scale_) > 0.0001 ) {
      // Now get the uncertainties
      jecUnc_->setJetEta( uncorrJet.eta() );
      jecUnc_->setJetPt( uncorrJet.pt() * corr );
      double unc = fabs(jecUnc_->getUncertainty( bool(scale_ > 0) ));

      // Add the "flat" flavor dependent corrections in quadrature
      unc = sqrt( unc*unc + scale_*scale_);
      double sign = 1.0;
      if ( scale_ < 0.0 ) sign = -1.0;
	     
      // Scale up or down by jetScale_
      double ijetscale = (1 + sign * unc);
      corr *= ijetscale;
    }    

    // -------
    // Jet angular resolution smearing
    // -------
    double etaScale_ = 1.0;
    if( fabs(etaSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
      double recoeta = ijet->eta();
      double geneta = ijet->genJet()->eta();
      double deltaeta = (recoeta-geneta)*etaSmear_ ;
      etaScale_ = std::max((double)0.0,(recoeta+deltaeta)/recoeta);
    }


    double phiScale_ = 1.0;
    if( fabs(etaSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
      double recophi = ijet->phi();
      double genphi = ijet->genJet()->phi();
      double deltaphi = (recophi-genphi)*etaSmear_ ;
      phiScale_ = std::max((double)0.0,(recophi+deltaphi)/recophi);
    }



    // -------
    // Jet energy resolution smearing
    // -------
    double ptSmear_ = 1.0;
    if( fabs(smear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 )  {
      double recopt = ijet->pt();
      double genpt = ijet->genJet()->pt();
      double deltapt = (recopt-genpt)*smear_;
      ptSmear_ = std::max((double)0.0, (recopt+deltapt)/recopt);
    }

    reco::Candidate::PolarLorentzVector corrJet (uncorrJet.pt(), uncorrJet.eta(), uncorrJet.phi(), uncorrJet.mass());
    corrJet *=  (corr * ptSmear_);
    corrJet.SetEta( corrJet.eta() * etaScale_ );
    corrJet.SetPhi( corrJet.phi() * phiScale_ );

    const reco::CATopJetTagInfo * catopTag = 
      dynamic_cast<reco::CATopJetTagInfo const *>(ijet->tagInfo(topTagName_));
    bool passedTopTag = topTagFunctor_( *ijet, topTagRet );

    topTagP4->push_back( corrJet );
    topTagPass->push_back( passedTopTag );
    topTagMinMass->push_back( catopTag->properties().minMass * (corr * ptSmear_) );
    topTagTopMass->push_back( catopTag->properties().topMass * (corr * ptSmear_) );
    topTagNSubjets->push_back( ijet->numberOfDaughters() );
    topTagBDisc->push_back( ijet->bDiscriminator("trackCountingHighEffBJetTags") );

  }

  // For real data, get trigger path
  if ( readTrig_ ) {
    iEvent.getByLabel( trigSrc_,h_trig );
    for ( std::vector<std::string>::const_iterator itrigBegin = trigs_.begin(),
	    itrigEnd = trigs_.end(), itrig = itrigBegin;
	  itrig != itrigEnd; ++itrig ) {
      if ( h_trig->wasRun() && h_trig->wasAccept() && h_trig->paths() > 0 ) {
	int indexPath = h_trig->indexPath( *itrig );
	if ( indexPath > 0 ) {
	  pat::TriggerPath const * path = h_trig->path( *itrig );
	  if ( path != 0 && path->wasRun() && path->wasAccept() ) {
	    trigIndex->push_back( path->index() );
	    myTrigIndex->push_back( static_cast<int>(itrig - itrigBegin) );
	    prescales->push_back( path->prescale() );
	    trigNames->push_back( path->name() );
	  }
	}
      }
    }
  }

  //Make hemisphere
  if( topTagP4->size() > 0 ) {
    LorentzV  leadJet = topTagP4->at(0);
    for( size_t i=0; i<topTagP4->size(); i++ ) {
      double dPhi = fabs( reco::deltaPhi<double>( leadJet.phi(), topTagP4->at(i).phi() ) );
      if( dPhi < TMath::Pi()/2 )  {
        topTagP4Hemis0->push_back( topTagP4->at(i) );
        topTagMinMassHemis0->push_back( topTagMinMass->at(i) );
        topTagTopMassHemis0->push_back( topTagTopMass->at(i) );
        topTagNSubjetsHemis0->push_back( topTagNSubjets->at(i) );
        topTagPassHemis0->push_back( topTagPass->at(i) );
      }
      else  {
        topTagP4Hemis1->push_back( topTagP4->at(i) );
        topTagMinMassHemis1->push_back( topTagMinMass->at(i) );
        topTagTopMassHemis1->push_back( topTagTopMass->at(i) );
        topTagNSubjetsHemis1->push_back( topTagNSubjets->at(i) );
        topTagPassHemis1->push_back( topTagPass->at(i) );
      }
    }
    for( size_t i=0; i<wTagP4->size(); i++ )  {
      double dPhi = fabs( reco::deltaPhi<double>( leadJet.phi(), wTagP4->at(i).phi() )  );
      if( dPhi < TMath::Pi()/2 )  {
        wTagP4Hemis0->push_back( wTagP4->at(i) );
        wTagBDiscHemis0->push_back( wTagBDisc->at(i) );
        wTagMuHemis0->push_back( wTagMu->at(i) );
      }
      else  {
        wTagP4Hemis1->push_back( wTagP4->at(i) );
        wTagBDiscHemis1->push_back( wTagBDisc->at(i) );
        wTagMuHemis1->push_back( wTagMu->at(i) );
      }
    }
  }

  if( wTagP4Hemis0->size() > 0 )  {
    LorentzV   leadJetHemis0 = wTagP4Hemis0->at(0) ;
    double minDr = 99999. ;
    for( size_t i=1 ; i<wTagP4Hemis0->size() ; i++ )  {
      double deltaR = reco::deltaR<double>( leadJetHemis0.eta(), leadJetHemis0.phi(),
                                            wTagP4Hemis0->at(i).eta(), wTagP4Hemis0->at(i).phi() );
      if( deltaR < minDr )  {
        *jet3Hemis0 = i;
        minDr = deltaR;
      }
    }
  }
  if( wTagP4Hemis1->size() > 0 )  {
    LorentzV   leadJetHemis1 = wTagP4Hemis1->at(0) ;
    double minDr = 99999. ;
    for( size_t i=1 ; i<wTagP4Hemis1->size() ; i++ )  {
      double deltaR = reco::deltaR<double>( leadJetHemis1.eta(), leadJetHemis1.phi(),
                                            wTagP4Hemis1->at(i).eta(), wTagP4Hemis1->at(i).phi() );
      if( deltaR < minDr )  {
        *jet3Hemis1 = i;
        minDr = deltaR;
      }
    }
  }


  *rho = rhoVal ;


  edm::Handle<GenEventInfoProduct>    genEvt;
  iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
  if( genEvt.isValid() )  {
    *weight = genEvt->weight() ;
  }

  if ( ! iEvent.isRealData() && pdfSet_ != "" ) {

    edm::Handle<GenEventInfoProduct> pdfstuff;
    if (iEvent.getByLabel("generator", pdfstuff)) {


      LHAPDF::usePDFMember(1,0);

      float q = pdfstuff->pdf()->scalePDF;
 
      int id1 = pdfstuff->pdf()->id.first;
      double x1 = pdfstuff->pdf()->x.first;
      // double pdf1 = pdfstuff->pdf()->xPDF.first;
      
      int id2 = pdfstuff->pdf()->id.second;
      double x2 = pdfstuff->pdf()->x.second;
      // double pdf2 = pdfstuff->pdf()->xPDF.second; 

      double xpdf1 = LHAPDF::xfx(1, x1, q, id1);
      double xpdf2 = LHAPDF::xfx(1, x2, q, id2);
      double w0 = xpdf1 * xpdf2;
      for(int i=1; i <=44; ++i){
	LHAPDF::usePDFMember(1,i);
	double xpdf1_new = LHAPDF::xfx(1, x1, q, id1);
	double xpdf2_new = LHAPDF::xfx(1, x2, q, id2);
	double weight = xpdf1_new * xpdf2_new / w0;
	pdf_weights->push_back(weight);
      }
    }
  }

  iEvent.put(wTagP4        ,"wTagP4");
  iEvent.put(topTagP4      ,"topTagP4");  
  iEvent.put(wTagBDisc     ,"wTagBDisc");
  iEvent.put(topTagBDisc   ,"topTagBDisc");
  iEvent.put(wTagMu        ,"wTagMu");
  iEvent.put(wTagPass      ,"wTagPass");
  iEvent.put(topTagMinMass ,"topTagMinMass");
  iEvent.put(topTagTopMass ,"topTagTopMass");
  iEvent.put(topTagNSubjets,"topTagNSubjets");
  iEvent.put(topTagPass    ,"topTagPass");    
  iEvent.put(prescales     ,"prescales");
  iEvent.put(trigIndex     ,"trigIndex");
  iEvent.put(myTrigIndex   ,"myTrigIndex");
  iEvent.put(trigNames     ,"trigNames");
  iEvent.put(wTagP4Hemis0        ,"wTagP4Hemis0");
  iEvent.put(topTagP4Hemis0      ,"topTagP4Hemis0");
  iEvent.put(wTagBDiscHemis0     ,"wTagBDiscHemis0");
  iEvent.put(wTagMuHemis0        ,"wTagMuHemis0");
  iEvent.put(topTagMinMassHemis0 ,"topTagMinMassHemis0");
  iEvent.put(topTagTopMassHemis0 ,"topTagTopMassHemis0");
  iEvent.put(topTagNSubjetsHemis0,"topTagNSubjetsHemis0");
  iEvent.put(topTagPassHemis0    ,"topTagPassHemis0");
  iEvent.put(jet3Hemis0,          "jet3Hemis0" );
  iEvent.put(wTagP4Hemis1        ,"wTagP4Hemis1");
  iEvent.put(topTagP4Hemis1      ,"topTagP4Hemis1");
  iEvent.put(wTagBDiscHemis1     ,"wTagBDiscHemis1");
  iEvent.put(wTagMuHemis1        ,"wTagMuHemis1");
  iEvent.put(topTagMinMassHemis1 ,"topTagMinMassHemis1");
  iEvent.put(topTagTopMassHemis1 ,"topTagTopMassHemis1");
  iEvent.put(topTagNSubjetsHemis1,"topTagNSubjetsHemis1");
  iEvent.put(topTagPassHemis1    ,"topTagPassHemis1");
  iEvent.put(jet3Hemis1,          "jet3Hemis1"  );
  iEvent.put( rho,                "rho" );
  iEvent.put( weight,             "weight");
  iEvent.put( npv,     "npv");
  iEvent.put( npvTrue, "npvTrue");
  iEvent.put( pdf_weights, "pdfWeights");
  iEvent.put( mttgen, "mttgen" );

  return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
TTBSMProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TTBSMProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TTBSMProducer);
