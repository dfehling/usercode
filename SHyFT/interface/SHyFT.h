#ifndef Analysis_SHyFT_interface_SHyFT_h
#define Analysis_SHyFT_interface_SHyFT_h

#include "PhysicsTools/SelectorUtils/interface/WPlusJetsEventSelector.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Record.h"
#include "DataFormats/FWLite/interface/EventSetup.h"
#include "DataFormats/FWLite/interface/ESHandle.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"
#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"


#include <iostream>
#include <iomanip>
#include <cmath>      //necessary for absolute function fabs()
#include <boost/shared_ptr.hpp>
#include <boost/lexical_cast.hpp>


//Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TSystem.h"

typedef std::vector<reco::ShallowClonePtrCandidate> ShallowCloneCollection;

class SHyFT {

  public:

  struct SHyFTSummary {
    SHyFTSummary( unsigned int irun=0,
		  unsigned int ilumiSec=0,
		  unsigned int ievent=0,
		  unsigned int inJets=0,
		  unsigned int inTags=0 ) :
    run(irun), lumiSec(ilumiSec), event(ievent), nJets(inJets), nTags(inTags)
    {
      if ( nJets < nTags ) {
	throw cms::Exception("InvalidCode") << " This says there are more tags than jets."
					    << " This is nonsense." <<std::endl;
      }
    }
    unsigned int run;
    unsigned int lumiSec;
    unsigned int event;
    unsigned int nJets;
    unsigned int nTags;

    friend std::ostream & operator<<(std::ostream & out, SHyFTSummary const & r ) {
      char buff[1000];
      sprintf(buff, "%12d , %12d, %20d, %5d, %5d", r.run, r.lumiSec, r.event, r.nJets, r.nTags );
      out << buff;
      return out;
    }

    bool operator<( SHyFTSummary const & r ) const {
      if ( run < r.run ) return true;
      else if ( run > r.run ) return false;
      else { // equal runs
	if ( lumiSec < r.lumiSec ) return true;
	else if ( lumiSec > r.lumiSec ) return false;
	else { // equal lumi sections
	  if ( event < r.event ) return true;
	  else if ( event > r.event ) return false;
	  else return false;
	}
      }
    }
  };

    SHyFT(const edm::ParameterSet& iConfig, TFileDirectory& iDir);
    virtual ~SHyFT() {     
    }
    virtual void analyze(const edm::EventBase& iEvent);
    virtual void beginJob() {}
    virtual void endJob();

  private:
    bool analyze_electrons(const std::vector<reco::ShallowClonePtrCandidate>& electrons);
    bool analyze_muons(const std::vector<reco::ShallowClonePtrCandidate>& muons);    
    bool analyze_met( const reco::ShallowClonePtrCandidate & met );
    void calcTagWeight (double & weight, const std::vector<reco::ShallowClonePtrCandidate>& jets);
    bool calcSampleName (const edm::EventBase& iEvent, std::string &sampleName);

    bool make_templates(const std::vector<reco::ShallowClonePtrCandidate>& jets,
			const reco::ShallowClonePtrCandidate & met,
			const std::vector<reco::ShallowClonePtrCandidate>& muons,
			const std::vector<reco::ShallowClonePtrCandidate>& electrons
			);

    WPlusJetsEventSelector wPlusJets;
    TFileDirectory& theDir;
    // 'registry' for the histograms                                                                                                                                                                    
    std::map<std::string, TH1F*> histograms;
    std::map<std::string, TH2F*> histograms2d;
    std::map<std::string, TH3F*> histograms3d;
    // the following parameters need to come from the config
    bool muPlusJets_;
    bool ePlusJets_;
    bool useHFcat_;
    int nJetsCut_ ;
    int mode;
    std::string sampleNameInput;
    // used to be a global, what a shit!
    int HFcat_;
    std::string secvtxname;
    bool doMC_;
    std::string plRootFile_;
    TFile f_;
    fwlite::EventSetup es_;
    fwlite::RecordID  recId_;
    double btagOP_;
    std::string bPerformanceTag_;
    std::string cPerformanceTag_;
    std::string lPerformanceTag_;
    std::string btaggerString_;
    std::string identifier_;

    int allNumTags_;
    int allNumJets_;
    std::vector<SHyFTSummary> summary_;

    double globalWeight_;  // For reweighting the entire event for, e.g., pdf reweighting
    bool reweightPDF_;
    edm::InputTag pdfInputTag_; 
    std::vector<std::string> pdfSetNames_;

    bool doTagWeight_;
    double bcEffScale_;
    double lfEffScale_;
};


#endif
