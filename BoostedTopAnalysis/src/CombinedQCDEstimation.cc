#include "Analysis/BoostedTopAnalysis/interface/CombinedQCDEstimation.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "AnalysisDataFormats/TopObjects/interface/CATopJetTagInfo.h"

CombinedQCDEstimation::CombinedQCDEstimation( const edm::ParameterSet & iConfig,  TFileDirectory & iDir ) :
	theDir( iDir ),
	type22Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type22Selection") ),
	bTagOP_                 ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("bTagOP") ),
	bTagAlgo_               ( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<string>("bTagAlgo") ),
	jetPt0_					( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("jetPt0") ),
	jetPt1_					( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("jetPt1") ),
	jetEta_					( iConfig.getParameter<edm::ParameterSet>("Type22Selection").getParameter<double>("jetEta") ),
	wMassMin_               ( iConfig.getParameter<double>("wMassMin") ),
	wMassMax_               ( iConfig.getParameter<double>("wMassMax") ),
	topMassMin_             ( iConfig.getParameter<double>("topMassMin") ),
	topMassMax_             ( iConfig.getParameter<double>("topMassMax") ),
	mistagFileName_         ( iConfig.getParameter<string>("mistagFile") ),
	prob                    ( iConfig.getParameter<double>("Probability") ),
	runOnData_              ( iConfig.getParameter<bool>("runOnData") ),
	type11Selection_v1_     ( iConfig.getParameter<edm::ParameterSet>("Type11Selection") ),
	caTopJetPtMin_          ( iConfig.getParameter<edm::ParameterSet>("Type11Selection").getParameter<double>("caTopJetPtMin") ),
	caTopJetEtaCut_         ( iConfig.getParameter<edm::ParameterSet>("Type11Selection").getParameter<double>("caTopJetEtaCut") ),
	caTopJetMassMin_        ( iConfig.getParameter<double>("caTopJetMassMin") ),
	caTopJetMassMax_        ( iConfig.getParameter<double>("caTopJetMassMax") ),
	caTopMinMassMin_        ( iConfig.getParameter<double>("caTopMinMassMin") ),
	caTopMistagFileName_    ( iConfig.getParameter<string>("caTopMistagFileName") )
{
	std::cout << "Instantiated CombinedQCDEstimation" << std::endl;
	
	// Type11 histograms
	histograms1d["ttMassType11_measured"]    = theDir.make<TH1F>("ttMassType11_measured",   "measured t#bar{t} Inv Mass Type11",   200,  0,  2000 );
	histograms1d["ttMassType11_predicted"]   = theDir.make<TH1F>("ttMassType11_predicted",  "predictedt#bar{t} Inv Mass Type11",   200,  0,  2000 );
	histograms1d["ttMassType11_predicted_errorSquared"] = theDir.make<TH1F>("ttMassType11_predicted_errorSquared", "sum of squared errors t#bar{t} Inv Mass Type11",   200,  0,  2000 );
    
	// Type12 histograms	
	histograms1d["ttMassType12_measured"]     = theDir.make<TH1F>("ttMassType12_measured",   "measured t#bar{t} Inv Mass Type12",   200,  0,  2000 );
	histograms1d["ttMassType12_predicted"]    = theDir.make<TH1F>("ttMassType12_predicted",  "predicted t#bar{t} Inv Mass Type12",  200,  0,  2000 );
	histograms1d["ttMassType12_predicted_errorSquared"] = theDir.make<TH1F>("ttMassType12_predicted_errorSquared", "sum of squared errors t#bar{t} Inv Mass Type12",   200,  0,  2000 );

	// Type22 histograms
	histograms1d["ttMassType22_measured"]    = theDir.make<TH1F>("ttMassType22_measured",   "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
	histograms1d["ttMassType22_predicted"]   = theDir.make<TH1F>("ttMassType22_predicted",  "t#bar{t} Inv Mass Type22",   200,  0,  2000 );
	histograms1d["ttMassType22_predicted_errorSquared"] = theDir.make<TH1F>("ttMassType22_predicted_errorSquared", "sum of squared errors t#bar{t} Inv Mass Type22",   200,  0,  2000 );

	
	histograms1d["topMassPred"]     = theDir.make<TH1F>("topMassPred",    "Top Mass",									100,  0,  500 );
	
	// counting histograms
	histograms1d["Nevents_22_tighttight_tightloose"]  = theDir.make<TH1F>("Nevents_22_tighttight_tightloose",   "Nevents_22_tighttight_tightloose",   2,  0.5,  2.5 );
	histograms1d["Nevents_12_tight_loose"]  = theDir.make<TH1F>("Nevents_12_tight_loose",   "Nevents_12_tight_loose",   2,  0.5,  2.5 );
	histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]  = theDir.make<TH1F>("Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg",   "Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg",   6,  0.5,  6.5 );
	histograms1d["Nevents_Type22_Case123"]  = theDir.make<TH1F>("Nevents_Type22_Case123",   "Nevents_Type22_Case123",   3,  0.5,  3.5 );

	std::cout << "Instantiated histograms" << std::endl;

	// Input histograms
	mistagFile_   =  TFile::Open( mistagFileName_.c_str() );
	wMistag_      =  (TH1F*)mistagFile_       ->  Get("wMistag");
	caTopMistagFile_   =  TFile::Open( caTopMistagFileName_.c_str() );
	topMistag_      =  (TH1F*)caTopMistagFile_       ->  Get("MISTAG_RATE");
	std::cout << "Input histograms" << std::endl;

	//use the PredictedDistrubution class to get correct error

	//ttMassPredictedDistribution_type22  =  new PredictedDistribution( (TH1D*)wMistag_ , "//ttMassPredictedDistribution_type22", "type22 t#bar{t} Inv Mass",  200,  0,  2000 );
	std::cout<<"check1"<<std::endl;

	//ttMassPredictedDistribution_type11  =  new PredictedDistribution( (TH1D*)topMistag_ , "//ttMassPredictedDistribution_type11", "type11 t#bar{t} Inv Mass",  200,  0,  2000 );
	std::cout<<"check2"<<std::endl;

	//ttMassPredictedDistribution_type12  =  new PredictedDistribution( (TH1D*)wMistag_ , "//ttMassPredictedDistribution_type12", "type12 t#bar{t} Inv Mass",  200,  0,  2000 );

	std::cout << "PredictedDistrubution" << std::endl;

	
	edm::Service<edm::RandomNumberGenerator> rng;
	if ( ! rng.isAvailable()) {
		throw cms::Exception("Configuration")
		<< "Module requires the RandomNumberGeneratorService\n";
	}
	
	CLHEP::HepRandomEngine& engine = rng->getEngine();
	flatDistribution_ = new CLHEP::RandFlat(engine, 0., 1.);
}

void CombinedQCDEstimation::analyze( const edm::EventBase & iEvent )
{
	double evtWeight = 1.0;
	
	edm::Handle<GenEventInfoProduct>    genEvt;
	iEvent.getByLabel( edm::InputTag("generator"),  genEvt );
	if( genEvt.isValid() )  {
		//evtWeight = genEvt->weight() ;
	}
	
	bool verbose_ = false;
	int run = iEvent.id().run();
	int event = iEvent.id().event();
	int lumi = iEvent.id().luminosityBlock(); 
	if (verbose_)cout<<"\nAnalyze event "<<iEvent.id()<<endl;

	pat::strbitset   retType11 = type11Selection_v1_.getBitTemplate();
	bool passType11 = type11Selection_v1_( iEvent, retType11 );
	std::vector<edm::Ptr<pat::Jet> >  const &  caTopJets_ = type11Selection_v1_.caTopJets();
	std::vector<edm::Ptr<pat::Jet> >  const &  ca8Jets_ = type11Selection_v1_.ca8Jets();
	
	pat::strbitset   retType22 = type22Selection_v1_.getBitTemplate();
	bool passType22 = type22Selection_v1_( iEvent, retType22 );
	std::vector<edm::Ptr<pat::Jet> >  const &  pfJets_ = type22Selection_v1_.pfJets();
	
	wJetSelector_  = &(type22Selection_v1_.wJetSelector() );

	if (verbose_)cout<<"Selector results: passType11 = "<<passType11<<"  passType22 = "<<passType22<<endl;
	if (verbose_&&passType11) cout<<"  ca8Jets_.size() = "<<ca8Jets_.size()<<endl;
	if (verbose_&&passType11) cout<<"  caTopJets_.size() = "<<caTopJets_.size()<<endl;
	if (verbose_&&passType22) cout<<"  pfJets_.size() = "<<pfJets_.size()<<endl;
	
	if (verbose_&&passType11)
	{
		cout<<"Print ca8Jets info"<<endl;
		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=ca8Jets_.begin(), jetEnd=ca8Jets_.end(), ica8=jetBegin ;
			ica8!=jetEnd; ica8++ ) 
		{
			pat::Jet const & ca8Jet = **ica8;
			
			cout<<"  eta "<<ca8Jet.eta()<<" phi "<<ca8Jet.phi()<<" pt "<<ca8Jet.pt()<<" mass "<<ca8Jet.mass()<<endl;
		}
		cout<<"Print caTopJet info"<<endl;
		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=caTopJets_.begin(), jetEnd=caTopJets_.end(), icatop=jetBegin ;
			icatop!=jetEnd; icatop++ ) 
		{
			pat::Jet const & caTopJet = **icatop;
			
			cout<<"  eta "<<caTopJet.eta()<<" phi "<<caTopJet.phi()<<" pt "<<caTopJet.pt()<<" mass "<<caTopJet.mass()<<endl;
		}
	}
	if (verbose_&&passType22)
	{
		cout<<"Print prunedJet info"<<endl;
		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
			ijet!=jetEnd; ijet++ ) 
		{
			pat::Jet const & jet = **ijet;
			bool  wtagged = false;
			bool  btagged = false;
			bool  cajet_btagged = false;
			pat::strbitset iret = wJetSelector_->getBitTemplate();
			wtagged = wJetSelector_->operator()( jet, iret );
			bool passWMass = (jet.mass() > wMassMin_ ) && (jet.mass() < wMassMax_ );
			btagged = (jet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );
			cout<<"  eta "<<jet.eta()<<" phi "<<jet.phi()<<" pt "<<jet.pt()<<" mass "<<jet.mass()<<" wtagged? "<<wtagged<<" btagged? "<<btagged<<" energy "<<jet.energy()<<" px "<<jet.px()<<" py "<<jet.py()<<" jet.pz() "<<jet.pz()<<endl;			
		}
		cout<<"Print prunedJet pairwise masses"<<endl;

		int count1=0;
		
		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
			ijet!=jetEnd; ijet++ ) 
		{
			int count2=0;

			pat::Jet const & jet = **ijet;
			for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin2=pfJets_.begin(), jetEnd2=pfJets_.end(), ijet2=jetBegin2 ;
				ijet2!=jetEnd2; ijet2++ ) 
			{
				if (count1==count2) continue;
				pat::Jet const & jet2 = **ijet2;
				
				reco::Candidate::LorentzVector p4_top = jet.p4() + jet2.p4() ;

				double px1 = jet.px();
				double py1 = jet.py();
				double pz1 = jet.pz();
				double e1 = jet.energy();
		
				double px2 = jet2.px();
				double py2 = jet2.py();
				double pz2 = jet2.pz();
				double e2 = jet2.energy();
				 
				double mymass = sqrt( (e1+e2)*(e1+e2) - (px1+px2)*(px1+px2) - (py1+py2)*(py1+py2) - (pz1+pz2)*(pz1+pz2) );
				
				cout<<" m("<<count1<<","<<count2<<") = "<< p4_top.mass()<<"  mass calculation2 = "<<mymass<<"  jet.pt() "<<jet.pt()<<"  jet2.pt() "<<jet2.pt()<<endl;
				
					
				count2++;
			}
			count1++;	
		}
			
	
	}
	
	// Define two hemispheres in deltaphi. hemisphere0 is centered on the leading unpruned CA8 jet. hemisphere1 is opposite. Group caTop and pruned jets into these hemispheres.
	if (verbose_) cout<<"Group jets into hemispheres"<<endl;
	if( passType11 && passType22 && ca8Jets_.size()>=2 )  
	{			
		//Put jets in the proper hemisphere
		pat::Jet const & leadJet = *ca8Jets_.at(0);
		std::vector<edm::Ptr<pat::Jet> >  hemisphere0_ca8, hemisphere1_ca8;
		std::vector<edm::Ptr<pat::Jet> >  hemisphere0, hemisphere1;
		std::vector<edm::Ptr<pat::Jet> >  hemisphere0_catop, hemisphere1_catop;
		std::vector<edm::Ptr<pat::Jet> >  wTags0,   wTags1;
		std::vector<edm::Ptr<pat::Jet> >  bTags0,   bTags1;
		std::vector<edm::Ptr<pat::Jet> >  noTags0,  noTags1;
		pat::Jet const * aJet0=NULL;
		pat::Jet const * aJet1=NULL;
		
		for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=ca8Jets_.begin(), jetEnd=ca8Jets_.end(), ica8=jetBegin ;
			ica8!=jetEnd; ica8++ ) 
		{
			pat::Jet const & ca8Jet = **ica8;
			if (verbose_) cout<<" ca8Jet eta "<<ca8Jet.eta()<<" phi "<<ca8Jet.phi()<<" pt "<<ca8Jet.pt()<<" mass "<<ca8Jet.mass()<<endl;
			
			//Group the ca8 jets into hemispheres
			double deltaPhi_leadJet_ca8Jet = fabs( reco::deltaPhi<double>( leadJet.phi(), ca8Jet.phi() ) );
			if( deltaPhi_leadJet_ca8Jet < TMath::Pi()/2 ) 
			{
				hemisphere0_ca8.push_back( *ica8 );	
				if (verbose_) cout<<"   -> hemisphere0_ca8. deltaPhi = "<< deltaPhi_leadJet_ca8Jet <<endl;
				
				// Match caTop to ca8 jets and group into hemispheres
				for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=caTopJets_.begin(), jetEnd=caTopJets_.end(), icatop=jetBegin ;
					icatop!=jetEnd; icatop++ ) 
				{
					pat::Jet const & caTopJet = **icatop;
					double deltaR_ca8Jet_caTopJet = deltaR( ca8Jet.eta(), ca8Jet.phi(), caTopJet.eta(), caTopJet.phi() );
					
					//match caTop jet to ca8 jet
					if( deltaR_ca8Jet_caTopJet < 0.1 ) 
					{
						if (verbose_) cout<<"   -> found matching caTopJet eta "<<caTopJet.eta()<<" phi "<<caTopJet.phi()<<" pt "<<caTopJet.pt()<<" mass "<<caTopJet.mass()<<" deltaR "<<deltaR_ca8Jet_caTopJet<<endl;
						hemisphere0_catop.push_back( *icatop );	
						if (verbose_) cout<<"     -> hemisphere0_catop. "<<endl;
					}
					
				}
				// Match pruned jets to ca8 jets and group into hemispheres
				for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
					ijet!=jetEnd; ijet++ ) 
				{
					pat::Jet const & prunedJet = **ijet;				
					bool  wtagged = false;
					bool  btagged = false;
					pat::strbitset iret = wJetSelector_->getBitTemplate();
					wtagged = wJetSelector_->operator()( prunedJet, iret );
					bool passWMass = (prunedJet.mass() > wMassMin_ ) && (prunedJet.mass() < wMassMax_ );
					btagged = (prunedJet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );
					
					double deltaR_ca8Jet_prunedJet = deltaR( ca8Jet.eta(), ca8Jet.phi(), prunedJet.eta(), prunedJet.phi() );
					
					//match pruned jet to catop jet
					if( deltaR_ca8Jet_prunedJet < 0.1 ) 
					{	
						if (verbose_) cout<<"   -> found matching prunedJet eta "<<prunedJet.eta()<<" phi "<<prunedJet.phi()<<" pt "<<prunedJet.pt()<<" mass "<<prunedJet.mass()<<" deltaR "<<deltaR_ca8Jet_prunedJet<<endl;
						
						hemisphere0.push_back( *ijet );
						
						if( wtagged && passWMass ) 
							wTags0.push_back( *ijet );
						else if ( btagged )
							bTags0.push_back( *ijet );
						else
							noTags0.push_back( *ijet );												
					}
				}
			}
			else
			{
				hemisphere1_ca8.push_back( *ica8 );	
				if (verbose_) cout<<"   -> hemisphere1_ca8. deltaPhi = "<< deltaPhi_leadJet_ca8Jet<<endl;
				
				// Match caTop to ca8 jets and group into hemispheres
				for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=caTopJets_.begin(), jetEnd=caTopJets_.end(), icatop=jetBegin ;
					icatop!=jetEnd; icatop++ ) 
				{
					pat::Jet const & caTopJet = **icatop;
					double deltaR_ca8Jet_caTopJet = deltaR( ca8Jet.eta(), ca8Jet.phi(), caTopJet.eta(), caTopJet.phi() );
					
					//match caTop jet to ca8 jet
					if( deltaR_ca8Jet_caTopJet < 0.1 ) 
					{
						if (verbose_) cout<<"   -> found matching caTopJet eta "<<caTopJet.eta()<<" phi "<<caTopJet.phi()<<" pt "<<caTopJet.pt()<<" mass "<<caTopJet.mass()<<" deltaR "<<deltaR_ca8Jet_caTopJet<<endl;
						hemisphere1_catop.push_back( *icatop );	
						if (verbose_) cout<<"     -> hemisphere1_catop. "<<endl;
					}
					
				}
				// Match pruned jets to ca8 jets and group into hemispheres
				for( vector<edm::Ptr<pat::Jet> >::const_iterator jetBegin=pfJets_.begin(), jetEnd=pfJets_.end(), ijet=jetBegin ;
					ijet!=jetEnd; ijet++ ) 
				{
					pat::Jet const & prunedJet = **ijet;				
					bool  wtagged = false;
					bool  btagged = false;
					pat::strbitset iret = wJetSelector_->getBitTemplate();
					wtagged = wJetSelector_->operator()( prunedJet, iret );
					bool passWMass = (prunedJet.mass() > wMassMin_ ) && (prunedJet.mass() < wMassMax_ );
					btagged = (prunedJet.bDiscriminator( bTagAlgo_ ) > bTagOP_ );
					
					double deltaR_ca8Jet_prunedJet = deltaR( ca8Jet.eta(), ca8Jet.phi(), prunedJet.eta(), prunedJet.phi() );
					
					//match pruned jet to catop jet
					if( deltaR_ca8Jet_prunedJet < 0.1 ) 
					{	
						if (verbose_) cout<<"   -> found matching prunedJet eta "<<prunedJet.eta()<<" phi "<<prunedJet.phi()<<" pt "<<prunedJet.pt()<<" mass "<<prunedJet.mass()<<" deltaR "<<deltaR_ca8Jet_prunedJet<<endl;
						
						hemisphere1.push_back( *ijet );
						
						if( wtagged && passWMass ) 
							wTags1.push_back( *ijet );
						else if ( btagged )
							bTags1.push_back( *ijet );
						else
							noTags1.push_back( *ijet );												
					}
				}
			}
		}	
		if (verbose_) cout<<"  hemisphere0_ca8.size() "<<hemisphere0_ca8.size()<<endl;
		if (verbose_) cout<<"  hemisphere1_ca8.size() "<<hemisphere1_ca8.size()<<endl;
		if (verbose_) cout<<"  hemisphere0_catop.size() "<<hemisphere0_catop.size()<<endl;
		if (verbose_) cout<<"  hemisphere1_catop.size() "<<hemisphere1_catop.size()<<endl;
		if (verbose_) cout<<"  hemisphere0.size() "<<hemisphere0.size()<<endl;
		if (verbose_) cout<<"  hemisphere1.size() "<<hemisphere1.size()<<endl;
		
		if( wTags0.size() >= 1 )  {
			if (verbose_) cout<<"Find untagged jet clostest to Wjet0"<<endl;
			double minDr = 999999. ;
			for(size_t i=0; i<noTags0.size(); i++ ) {
				double dR = reco::deltaR<double>( wTags0.at(0)->eta(), wTags0.at(0)->phi(),
												 noTags0.at(i)->eta(), noTags0.at(i)->phi() );
				if( dR < minDr )  {
					aJet0 = &(*noTags0.at(i));
					minDr = dR;
				}
			}
			if (verbose_ && noTags0.size()>0 ) cout<<"  wJet0 eta "<<wTags0.at(0)->eta()<<" wJet0 phi "<<wTags0.at(0)->phi()<<" closest jet eta "<<aJet0->eta()<<" phi "<<aJet0->phi()<<endl;
		}
		
		if( wTags1.size() >= 1 )  {
			if (verbose_) cout<<"Find untagged jet clostest to Wjet1"<<endl;
			double minDr = 999999. ;
			for( size_t i=0; i<noTags1.size(); i++ )  {
				double dR = reco::deltaR<double>( wTags1.at(0)->eta(), wTags1.at(0)->phi(),
												 noTags1.at(i)->eta(), noTags1.at(i)->phi() );
				if( dR < minDr )  {
					aJet1 = &(*noTags1.at(i));
					minDr = dR;
				}
			}
			if (verbose_ && noTags1.size()>0 ) cout<<"  wJet1 eta "<<wTags1.at(0)->eta()<<" wJet1 phi "<<wTags1.at(0)->phi()<<" closest jet eta "<<aJet1->eta()<<" phi "<<aJet1->phi()<<endl;
		}
		
		// Preselection
		bool preselected_event=false;
		if ( hemisphere0_ca8.size()>0 && hemisphere1_ca8.size()>0 )
		{
			pat::Jet const & ca8_0 = *hemisphere0_ca8.at(0);
			pat::Jet const & ca8_1 = *hemisphere1_ca8.at(0);
			if ( ca8_0.pt() > jetPt0_ && ca8_1.pt() > jetPt0_ && fabs(ca8_0.eta()) < caTopJetEtaCut_ && fabs(ca8_1.eta()) < caTopJetEtaCut_ )
			{
				preselected_event = true;
				if (verbose_) cout<<"Event passes preselection (pt>"<<caTopJetPtMin_<<" && |eta|<"<<caTopJetEtaCut_<<").  pt0 "<<ca8_0.pt()<<" pt1 "<<ca8_1.pt()<<" eta0 "<<ca8_0.eta()<<" eta1 "<<ca8_1.eta()<<endl;

			}
			else 
			{
				if (verbose_) cout<<"Event fails preselection! (pt<"<<caTopJetPtMin_<<" || |eta|>"<<caTopJetEtaCut_<<").  pt0 "<<ca8_0.pt()<<" pt1 "<<ca8_1.pt()<<" eta0 "<<ca8_0.eta()<<" eta1 "<<ca8_1.eta()<<endl;
			}
		}
		
		if (preselected_event)
		{
			// Setup Type 1
			if (verbose_) cout<<"Setup Type 1"<<endl;
			bool hasTaggedTopJet0=false;
			bool hasTaggedTopJet1=false;
			reco::Candidate::LorentzVector p4_catop_jet0;
			reco::Candidate::LorentzVector p4_catop_jet1;
			double j0_minmass=-99;
			double j1_minmass=-99;
			double j0_nsubjets=-99;
			double j1_nsubjets=-99;
			
			if ( hemisphere0_catop.size()>0 && hemisphere1_catop.size()>0 )
			{			
				
				pat::Jet const & catop0 = *hemisphere0_catop.at(0);
				pat::Jet const & catop1 = *hemisphere1_catop.at(0);
				
				p4_catop_jet0 = catop0.p4();
				p4_catop_jet1 = catop1.p4();
				
				double delta_phi_catop = fabs( reco::deltaPhi<double>( catop0.phi(), catop1.phi() ) );
				if (verbose_) cout<<"  catop0  pt "<<catop0.pt()<<" eta "<<catop0.eta()<<" phi "<<catop0.phi()<<endl;
				if (verbose_) cout<<"  catop1  pt "<<catop1.pt()<<" eta "<<catop1.eta()<<" phi "<<catop1.phi()<<endl;
				if (verbose_) cout<<"  delta_phi_catop "<<delta_phi_catop<<endl;
				if (verbose_) cout<<"  delta_phi_catop "<<delta_phi_catop<<endl;
				if (delta_phi_catop >2.1)
				{
					if (verbose_) cout<<"  passes delta_phi_catop"<<endl;
					if (verbose_) cout<<"  caTopJetPtMin_ "<<caTopJetPtMin_<<"  caTopJetEtaCut_ "<<caTopJetEtaCut_<<endl;
					if ( catop0.pt() > caTopJetPtMin_ && catop1.pt() > caTopJetPtMin_ && fabs(catop0.eta()) < caTopJetEtaCut_ && fabs(catop1.eta()) < caTopJetEtaCut_ )
					{
						if (verbose_) cout<<"  catop0 and catop1 pass eta and pt cuts"<<endl;
						preselected_event=true;
						std::vector<const reco::Candidate *>  catop0_subjets = catop0.getJetConstituentsQuick();
						
						if ( catop0_subjets.size() >=3)
						{	
							int subjetLoopCount=0;
							math::XYZTLorentzVector pairwiseMass01;
							math::XYZTLorentzVector pairwiseMass02;
							math::XYZTLorentzVector pairwiseMass12;
							
							for (std::vector<const reco::Candidate *>::iterator subjetIt = catop0_subjets.begin(); subjetIt != catop0_subjets.end(); subjetIt++)
							{					
								reco::Candidate const * subjetCand =  (*subjetIt);
								reco::PFJet const * pfSubjet = dynamic_cast<reco::PFJet const *>(subjetCand);  
								
								if (subjetLoopCount==0 || subjetLoopCount==1) pairwiseMass01 += pfSubjet->p4();
								if (subjetLoopCount==0 || subjetLoopCount==2) pairwiseMass02 += pfSubjet->p4();
								if (subjetLoopCount==1 || subjetLoopCount==2) pairwiseMass12 += pfSubjet->p4();
								subjetLoopCount++;
							}
							
							double min2 = std::min(pairwiseMass01.mass(), pairwiseMass02.mass() );
							j0_minmass = std::min(min2, pairwiseMass12.mass() );
							j0_nsubjets = subjetLoopCount;
						}//end if jet0 nsubjets>=3
						
						std::vector<const reco::Candidate *>  catop1_subjets = catop1.getJetConstituentsQuick();
						
						if ( catop1_subjets.size() >=3)
						{	
							int subjetLoopCount=0;
							math::XYZTLorentzVector pairwiseMass01;
							math::XYZTLorentzVector pairwiseMass02;
							math::XYZTLorentzVector pairwiseMass12;
							
							for (std::vector<const reco::Candidate *>::iterator subjetIt = catop1_subjets.begin(); subjetIt != catop1_subjets.end(); subjetIt++)
							{					
								reco::Candidate const * subjetCand =  (*subjetIt);
								reco::PFJet const * pfSubjet = dynamic_cast<reco::PFJet const *>(subjetCand);  
								
								if (subjetLoopCount==0 || subjetLoopCount==1) pairwiseMass01 += pfSubjet->p4();
								if (subjetLoopCount==0 || subjetLoopCount==2) pairwiseMass02 += pfSubjet->p4();
								if (subjetLoopCount==1 || subjetLoopCount==2) pairwiseMass12 += pfSubjet->p4();
								subjetLoopCount++;
							}
							
							double min2 = std::min(pairwiseMass01.mass(), pairwiseMass02.mass() );
							j1_minmass = std::min(min2, pairwiseMass12.mass() );
							j1_nsubjets = subjetLoopCount;
							
						}//end if jet1 nsubjets>=3
						
						if (verbose_) cout<<"    catop0.mass() "<<catop0.mass()<<"  j0_minmass "<<j0_minmass<<"  j0_nsubjets "<<j0_nsubjets<<endl;
						if (verbose_) cout<<"    catop1.mass() "<<catop1.mass()<<"  j1_minmass "<<j1_minmass<<"  j1_nsubjets "<<j0_nsubjets<<endl;
						
						if ( catop0.mass() > caTopJetMassMin_ && catop0.mass() < caTopJetMassMax_ && j0_minmass > caTopMinMassMin_ && j0_nsubjets>2){hasTaggedTopJet0=true;}
						if ( catop1.mass() > caTopJetMassMin_ && catop1.mass() < caTopJetMassMax_ && j1_minmass > caTopMinMassMin_ && j1_nsubjets>2){hasTaggedTopJet1=true;}					
						
						if (verbose_ && hasTaggedTopJet0 ) cout<<" hasTaggedTopJet0"<<endl;
						if (verbose_ && hasTaggedTopJet1 ) cout<<" hasTaggedTopJet1"<<endl;
						if (verbose_ && hasTaggedTopJet0 && hasTaggedTopJet1 ) cout<<" jet0 and jet1 are tagged"<<endl;
						
					}//end if passes pt and eta cuts
				}//end if passes deltaphi
			}//end if both hemispheres have catop jets
			
			
			if (verbose_) cout<<"Check if each hemisphere has non-leading b-jet"<<endl;
			bool hasNonLeadingBjet0 = false;
			bool hasNonLeadingBjet1 = false;
			
			for(size_t i=0; i<hemisphere0_ca8.size(); i++ ) {
				pat::Jet const & ca8 = *hemisphere0_ca8.at(i);
				if (verbose_) cout<<"  hemi0 ca8  jet "<<i<<"  eta "<<ca8.eta()<<" phi "<<ca8.phi()<<" pt "<<ca8.pt()<<" bDiscrim "<<ca8.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;
				
				if ( ca8.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
				{
					if (verbose_) cout<<"   -> b-tagged"<<endl;
					if (i>0) { hasNonLeadingBjet0 = true; if (verbose_) cout<<"    -> non-leading b-tag"<<endl;}
				}
			}
			for(size_t i=0; i<hemisphere1_ca8.size(); i++ ) {
				pat::Jet const & ca8 = *hemisphere1_ca8.at(i);
				if (verbose_) cout<<"  hemi1 ca8 jet "<<i<<"  eta "<<ca8.eta()<<" phi "<<ca8.phi()<<" pt "<<ca8.pt()<<" bDiscrim "<<ca8.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;
				
				if ( ca8.bDiscriminator( bTagAlgo_ ) > bTagOP_ )
				{
					if (verbose_) cout<<"   -> b-tagged"<<endl;
					if (i>0) { hasNonLeadingBjet1 = true; if (verbose_) cout<<"    -> non-leading b-tag"<<endl;}
				}
			}
			
			
			/*
			for(size_t i=0; i<hemisphere0.size(); i++ ) {
				pat::Jet const & prunedjet = *hemisphere0.at(i);
				if (verbose_) cout<<" hemi0 prunedjet  jet "<<i<<"  eta "<<prunedjet.eta()<<" phi "<<prunedjet.phi()<<" pt "<<prunedjet.pt()<<" bDiscrim "<<prunedjet.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;
				
			}
			for(size_t i=0; i<hemisphere1.size(); i++ ) {
				pat::Jet const & prunedjet = *hemisphere1.at(i);
				if (verbose_) cout<<" hemi1 prunedjet jet "<<i<<"  eta "<<prunedjet.eta()<<" phi "<<prunedjet.phi()<<" pt "<<prunedjet.pt()<<" bDiscrim "<<prunedjet.bDiscriminator( bTagAlgo_ )<<" op "<< bTagOP_ <<endl;
				
			}
			*/
			// Setup Type 2		
			if (verbose_) cout<<"Setup Type 2"<<endl;
			bool hasLooseTop0 = false, hasTightTop0 = false;
			bool hasLooseTop1 = false, hasTightTop1 = false;
			bool hasTwoWTags = (wTags0.size() >=1 ) && (wTags1.size() >=1 );
			bool hasBTag0 = (bTags0.size() >=1 );
			bool hasBTag1 = (bTags1.size() >= 1 );
			bool hasWTag0 = (wTags0.size() >= 1 );
			bool hasWTag1 = (wTags1.size() >= 1 );
			bool hasOneWTag = (hasWTag0 && !hasWTag1 ) || (hasWTag1 && !hasWTag0) ;
			bool hasWTag = hasWTag0 || hasWTag1;
			bool hasBTag = hasBTag0 || hasBTag1;
			
			reco::Candidate::LorentzVector p4_top0;
			reco::Candidate::LorentzVector p4_top1;
			
			
			if( hasBTag0 && hasWTag0 )  {
				p4_top0 = wTags0.at(0)->p4() + bTags0.at(0)->p4() ;
				if (verbose_) cout<<"  hemi 0 has W and b tag.   mass(W,b) = "<<p4_top0.mass()<<endl;
				
				if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )
					hasTightTop0 = true;
			} else if( aJet0 && hasWTag0 ) {
				p4_top0 = wTags0.at(0)->p4() + aJet0->p4() ;
				if (verbose_) cout<<"  hemi 0 has W tag and a non-b jet.   mass(W,jet) = "<<p4_top0.mass()<<endl;
				if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )
					hasLooseTop0 = true;
			}
			if( hasBTag1 && hasWTag1 )  {
				p4_top1 = wTags1.at(0)->p4() + bTags1.at(0)->p4();
				if (verbose_) cout<<"  hemi 1 has W and b tag.   mass(W,b) = "<<p4_top1.mass()<<endl;
				if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )
					hasTightTop1 = true;
			} else if ( aJet1 && hasWTag1 ) {
				p4_top1 = wTags1.at(0)->p4() + aJet1->p4();
				if (verbose_) cout<<"  hemi 1 has W tag and a non-b jet.   mass(W,jet) = "<<p4_top1.mass()<<endl;
				if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )
					hasLooseTop1 = true;
			}
						
			if (verbose_) 
			{			
				cout<<"Setup Summary "<<endl;
				cout<<"           hasWTag0 "<<hasWTag0<<endl;
				cout<<"           hasBTag0 "<<hasBTag0<<endl;
				cout<<"       hasTightTop0 "<<hasTightTop0<<endl;
				cout<<"       hasLooseTop0 "<<hasLooseTop0<<endl;	
				cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
				cout<<" hasNonLeadingBjet0 "<<hasNonLeadingBjet0<<endl;
				cout<<"           hasWTag1 "<<hasWTag1<<endl;
				cout<<"           hasBTag1 "<<hasBTag1<<endl;
				cout<<"       hasTightTop1 "<<hasTightTop1<<endl;
				cout<<"       hasLooseTop1 "<<hasLooseTop1<<endl;	
				cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
				cout<<" hasNonLeadingBjet1 "<<hasNonLeadingBjet1<<endl;
			}	
			
			
			
			
			///////////////////////////////////////////////////////////////////////////////////////////////
			// Measure pass events
			if (verbose_) cout<<"Measure pass events"<<endl;

			bool type11_passevent=false;
			bool type12_passevent=false;
			bool type22_passevent=false;
			
			// Use unpruned, regular CA8 jets for Njets, pT, and eta cuts. 
			
			// Type 1+1 signal
			if ( preselected_event && hasTaggedTopJet0 && hasTaggedTopJet1 )
			{
				type11_passevent = true;
				histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(1,evtWeight);
				
				double ttMass = (p4_catop_jet0+p4_catop_jet1).mass();
				histograms1d["ttMassType11_measured"] ->Fill (ttMass, evtWeight);
				
				if(runOnData_||verbose_) 
				{
					cout<<" Yipee!, Type1+Type1, Event id, "<<iEvent.id()<<endl;
					cout<<" summary:"<<endl;
					cout<<"  j0_pt "<<p4_catop_jet0.pt()<<endl;
					cout<<"  j1_pt "<<p4_catop_jet1.pt()<<endl;
					cout<<"  j0_mass "<<p4_catop_jet0.mass()<<endl;
					cout<<"  j1_mass "<<p4_catop_jet1.mass()<<endl;
					cout<<"  j0_nsubjets "<<j0_nsubjets<<endl;
					cout<<"  j1_nsubjets "<<j1_nsubjets<<endl;
					cout<<"  j0_minmass "<<j0_minmass<<endl;
					cout<<"  j1_minmass "<<j1_minmass<<endl;
				}
				//This is our signal, return
				return;
			}
			
			// Type 1+2 signal
			if ( preselected_event && !type11_passevent )
			{
				//some test histograms
				if ( (hasTaggedTopJet0 && hasTightTop1) || (hasTaggedTopJet1 && hasTightTop0) ) histograms1d["Nevents_12_tight_loose"] ->Fill (1, evtWeight);
				if ( (hasTaggedTopJet0 && hasLooseTop1) || (hasTaggedTopJet1 && hasLooseTop0) ) histograms1d["Nevents_12_tight_loose"] ->Fill (2, evtWeight);
				
				//fill pass histograms
				//if ( (hasTaggedTopJet0 && ( hasTightTop1 || hasLooseTop1)) || (hasTaggedTopJet1 && ( hasTightTop0 || hasLooseTop0)) )
				
				if ( hasOneWTag )
				{
					if ( (hasTaggedTopJet0 && hasTightTop1) || (hasTaggedTopJet1 && hasTightTop0) )
					{
						type12_passevent = true;
						histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(2,evtWeight);
						
						double ttMass =0;
						if (hasTaggedTopJet0) ttMass = (p4_catop_jet0+p4_top1).mass() ; 
						if (hasTaggedTopJet1) ttMass = (p4_catop_jet1+p4_top0).mass() ; 
						histograms1d["ttMassType12_measured"] ->Fill (ttMass, evtWeight);
						
						if(runOnData_||verbose_) 
						{
							cout<<" WoopWoop!, Type1+Type2, Event id, "<<iEvent.id()<<endl;
							cout<<" summary:"<<endl;
							cout<<"  catop j0_mass "<<p4_catop_jet0.mass()<<endl;
							cout<<"  catop j1_mass "<<p4_catop_jet1.mass()<<endl;
							cout<<"  catop j0_nsubjets "<<j0_nsubjets<<endl;
							cout<<"  catop j1_nsubjets "<<j1_nsubjets<<endl;
							cout<<"  catop j0_minmass "<<j0_minmass<<endl;
							cout<<"  catop j1_minmass "<<j1_minmass<<endl;
							
							cout<<"  p4_catop_jet0.mass() "<<p4_catop_jet0.mass()<<endl;
							cout<<"  p4_catop_jet1.mass() "<<p4_catop_jet1.mass()<<endl;
							cout<<"  p4_top0.mass() "<<p4_top0.mass()<<endl;
							cout<<"  p4_top1.mass() "<<p4_top1.mass()<<endl;
							cout<<"  ttMass "<<ttMass<<endl;
						}
						//This is our signal, return
						return;
					}
				}
			}
			
			// Type 22	
			if ( preselected_event && !type11_passevent && !type12_passevent )
			{
				//some test histograms
				if(hasTightTop0 && hasTightTop1) histograms1d["Nevents_22_tighttight_tightloose"] ->Fill (0.5, 1);
				if((hasTightTop0 && hasLooseTop1) || (hasLooseTop0 && hasTightTop1))  histograms1d["Nevents_22_tighttight_tightloose"] ->Fill (1.5, 1);
				
				//fill pass histogram
				if( (hasTightTop0 && hasTightTop1) || (hasTightTop0 && hasLooseTop1) || (hasLooseTop0 && hasTightTop1) )  
				{
					type22_passevent=true;
					histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(3,evtWeight);
					
					double ttMass = (p4_top0+p4_top1).mass() ;
					histograms1d["ttMassType22_measured"]      ->  Fill( ttMass, evtWeight );
					
					if(runOnData_||verbose_) 
					{
						cout<<" Woohoo, Type2+Type2, Event id, "<<iEvent.id()<<endl;
						cout<<"  p4_top0.mass() "<<p4_top0.mass()<<endl;
						cout<<"  p4_top1.mass() "<<p4_top1.mass()<<endl;
						cout<<"  ttMass "<<ttMass<<endl;
						cout<<"  hasTaggedTopJet0 "<<hasTaggedTopJet0<<" hasTaggedTopJet1 "<<hasTaggedTopJet1<<" hasTightTop0 "<< hasTightTop0 <<" hasTightTop1 "<<hasTightTop1<<" hasLooseTop0 "<<hasLooseTop0<<" hasLooseTop1 "<<hasLooseTop1<<endl;
						cout<<"  hasBTag0 "<<hasBTag0<<" hasBTag1 "<<hasBTag1<<" hasWTag0 "<<hasWTag0<<" hasWTag1 "<<hasWTag1<<endl; 
					}
					//This is our signal, return
					return;
				}
			}
			
			
			///////////////////////////////////////////////////////////////////////////////////////////////
			// Background estimation
			if (verbose_) cout<<"Background estimation"<<endl;

			bool type11_bkgd_prediction_event=false;
			bool type12_bkgd_prediction_event=false;
			
			// Type 1+1 Background estimation starts here
			if ( preselected_event && !type11_passevent && !type12_passevent && !type22_passevent )
			{
				if (!hasBTag0 && !hasBTag1 )
				{
					int bin0 = topMistag_->FindBin( p4_catop_jet0.pt() );
					int bin1 = topMistag_->FindBin( p4_catop_jet1.pt() );
					double mistagProb_jet0 = topMistag_->GetBinContent(bin0);
					double mistagProb_jet1 = topMistag_->GetBinContent(bin1);
					double mistagError_jet0 = topMistag_->GetBinError(bin0);
					double mistagError_jet1 = topMistag_->GetBinError(bin1);
					
					if ( (hasTaggedTopJet0 && !hasTaggedTopJet1 && !hasNonLeadingBjet1) || (hasTaggedTopJet1 && !hasTaggedTopJet0 && !hasNonLeadingBjet0)  ) 
					{		
						if (verbose_) cout<<" Type 11 background estimation event"<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
						if (verbose_) cout<<"   hasNonLeadingBjet0 "<<hasNonLeadingBjet0<<endl;
						if (verbose_) cout<<"   hasNonLeadingBjet1 "<<hasNonLeadingBjet1<<endl;
						
						type11_bkgd_prediction_event=true;
						histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(4,evtWeight);
						
						double ttMass = (p4_catop_jet0+p4_catop_jet1).mass();
						double weight = 0;
						double error_squared = 0;
						double pt=0;
						if (hasTaggedTopJet0)
						{	
							weight = mistagProb_jet1;
							error_squared = mistagError_jet1;
							pt = p4_catop_jet1.pt();
						}
						if (hasTaggedTopJet1)
						{	
							weight = mistagProb_jet0;
							error_squared = mistagError_jet0;
							pt = p4_catop_jet0.pt();
						}
						
						histograms1d["ttMassType11_predicted"] ->Fill (ttMass, weight);
						histograms1d["ttMassType11_predicted_errorSquared"] ->Fill (ttMass, error_squared);
						//ttMassPredictedDistribution_type11 -> Accumulate( ttMass, pt, 1,  evtWeight );
					}
				}
			}//end 11bkg
			
			// Type 1+2 Background estimation starts here
			//  Events with 1 top-tagged jet, 0 W-tagged jets, 1 b-tagged jet. 
			//  Jets in the hemisphere opposite the top jet which, when combined with the b-jet, have a pairwise mass in the top mass window, are used as probes to estimate the background
			if( preselected_event && !type11_passevent && !type12_passevent && !type22_passevent && !type11_bkgd_prediction_event )  
			{
				if( hasBTag && !hasWTag0 && !hasWTag1 ) 
				{
					if( hasTaggedTopJet0  && !hasWTag1 && hasBTag1 )  
					{ 
						if (verbose_) cout<<" Type 12 background estimation event"<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
						if (verbose_) cout<<"   hasWTag0 "<<hasWTag0<<endl;
						if (verbose_) cout<<"   hasWTag1 "<<hasWTag1<<endl;
						if (verbose_) cout<<"   hasBTag0 "<<hasBTag0<<endl;
						if (verbose_) cout<<"   hasBTag1 "<<hasBTag1<<endl;
						
						bool passTopMass1 = false;
						p4_top1.SetPxPyPzE(0,0,0,0);
						
						for( size_t i=0; i<noTags1.size(); i++ ) 
						{
							double pt = noTags1.at(i)->pt();
							int bin = wMistag_       ->  FindBin( pt );
							double weight = wMistag_ ->  GetBinContent( bin );  //dummy value, depend on pt
							double mistagError = wMistag_ ->GetBinError( bin );
							
							p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();
							if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  
							{
								histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(5,evtWeight);
								type12_bkgd_prediction_event=true;
								
								passTopMass1 = true;
								double ttMass = (p4_catop_jet0+p4_top1).mass() ;
								
								histograms1d["ttMassType12_predicted"]      ->  Fill( ttMass, weight*evtWeight );
								histograms1d["ttMassType12_predicted_errorSquared"] ->Fill (ttMass, mistagError*mistagError);
								//ttMassPredictedDistribution_type12 -> Accumulate( ttMass, pt, 1,  evtWeight );
							}
							
						}  // end i  
					} // jet0_toptagged 
					else if ( hasTaggedTopJet1 && !hasWTag0 && hasBTag0) 
					{
						if (verbose_) cout<<" Type 12 background estimation event"<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet0 "<<hasTaggedTopJet0<<endl;
						if (verbose_) cout<<"   hasTaggedTopJet1 "<<hasTaggedTopJet1<<endl;
						if (verbose_) cout<<"   hasWTag0 "<<hasWTag0<<endl;
						if (verbose_) cout<<"   hasWTag1 "<<hasWTag1<<endl;
						if (verbose_) cout<<"   hasBTag0 "<<hasBTag0<<endl;
						if (verbose_) cout<<"   hasBTag1 "<<hasBTag1<<endl;
						
						bool passTopMass0 = false;
						p4_top0.SetPxPyPzE(0,0,0,0);
						
						for( size_t i=0; i<noTags0.size(); i++ )  
						{
							double pt = noTags0.at(i)->pt();
							int   bin   =   wMistag_      ->  FindBin( pt );
							double weight = wMistag_      ->  GetBinContent( bin );  //dummy value, depend on pt
							double mistagError = wMistag_ ->GetBinError( bin );

							p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
							if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  
							{
								histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(5,evtWeight);
								type12_bkgd_prediction_event=true;
								
								passTopMass0 = true;
								double ttMass = (p4_top0+p4_catop_jet1).mass() ;
								histograms1d["ttMassType12_predicted"]      ->  Fill( ttMass, weight*evtWeight );
								histograms1d["ttMassType12_predicted_errorSquared"] ->Fill (ttMass, mistagError*mistagError);
								//ttMassPredictedDistribution_type12 -> Accumulate( ttMass, pt, 1,  evtWeight );
							}
						}  // end i
					} //has top jet
				} // end if has btag
			}//end if preselected
			

			// Type 2+2 Background estimation starts here
			if( preselected_event && !type11_passevent && !type12_passevent && !type22_passevent && !type11_bkgd_prediction_event && !type12_bkgd_prediction_event )  
			{
				if( hasOneWTag && hasBTag ) {
					if( hasWTag0 )  { 
						//cout<<"case 1"<<endl;
						bool passTopMass1 = false;
						p4_top1.SetPxPyPzE(0,0,0,0);
						if( hasTightTop0 )  { 
							//cout<<"case 10"<<endl;
							if (verbose_) cout<<"hasTightTop0. loop over hemi1 jets for background estimation"<<endl;
							
							for( size_t i=0; i<noTags1.size(); i++ )  {
								
								
								double pt = noTags1.at(i)->pt();
								int bin = wMistag_       ->  FindBin( pt );
								double weight = wMistag_ ->  GetBinContent( bin );  //dummy value, depend on pt
								double mistagError = wMistag_ ->GetBinError( bin );
								if (verbose_) cout<<" jet "<<i<<" pt "<<noTags1.at(i)->pt()<<"  weight "<<weight<<endl;

								if( hasBTag1 )  {
									cout<<"   -> hasBTag1"<<endl;
									p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();
									histograms1d["topMassPred"]     ->  Fill( p4_top1.mass(), weight*evtWeight );
									if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
										cout<<"   -> passes top mass cut "<<p4_top1.mass() <<endl;

										if (verbose_) cout<<" Type 22 background estimation event "<<endl;
										if (verbose_) cout<<"   hasTightTop0. hemi 1 has b-tag and p4_top1.mass() "<<p4_top1.mass()<<endl;

										passTopMass1 = true;
										histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
										histograms1d["Nevents_Type22_Case123"]->Fill(1,evtWeight);

										double ttMass = (p4_top0+p4_top1).mass() ;
										histograms1d["ttMassType22_predicted"]      ->  Fill( ttMass, weight*evtWeight );
										histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );
										
										//ttMassPredictedDistribution_type22      ->    Accumulate( ttMass, pt, 1,  evtWeight );
									}
								}
								else {  
									cout<<"   -> no hemi1 btag"<<endl;
									cout<<"      Loop over other jets and find the closest jet"<<endl;

									double minDr = 9999.0;
									pat::Jet const * nearestJet=NULL;
									for( size_t j=0; j<noTags1.size(); j++ )  {
										if( i==j )   continue;
										double dR = reco::deltaR<double>( noTags1.at(i)->eta(), noTags1.at(i)->phi(),
																		 noTags1.at(j)->eta(), noTags1.at(j)->phi() );
										if( dR < minDr )  {
											minDr = dR ;
											nearestJet = &(*noTags1.at(j));
										}
										cout<<"        Jet "<<j<<" dR "<<dR<<" minDr "<<minDr<<endl;

									} //end j
									if( nearestJet )  {
										//cout<<"case 11"<<endl;
										cout<<"          Found a nearestJet pt = "<<nearestJet->pt()<<" weight "<<weight<<endl;

										p4_top1 = noTags1.at(i)->p4() + nearestJet->p4();
										int  bin1  = wMistag_      ->  FindBin( nearestJet->pt() );
										double weight1 =  wMistag_ -> GetBinContent( bin1 );
										double mistagError1 = wMistag_ ->GetBinError( bin1 );

										weight *= (1-weight1);
										
										cout<<"            weight1 = "<<weight1<<" weight "<<weight<<endl;

										cout<<"            1-weight1 = "<<1-weight1<<" weight "<<weight<<endl;

										
										histograms1d["topMassPred"]   ->  Fill( p4_top1.mass(), weight*evtWeight );
										if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
											cout<<"               passes top mass cut "<<p4_top1.mass()<<endl;

											if (verbose_) cout<<" Type 22 background estimation event "<<endl;
											if (verbose_) cout<<"   hasTightTop0. hemi 1 has 0 b-tags and p4_top1.mass() "<<p4_top1.mass()<<endl;
											
											passTopMass1 = true;
											histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
											histograms1d["Nevents_Type22_Case123"]->Fill(2,evtWeight);

											double ttMass = (p4_top0+p4_top1).mass() ;
											histograms1d["ttMassType22_predicted"]    ->  Fill( ttMass, weight*evtWeight );
											histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );

											//ttMassPredictedDistribution_type22          ->      Accumulate( ttMass, pt, 1,  (1-weight1)*evtWeight );
										}
									}
								}  // end else
							}  // end i
						} //hasTightTop
						else if( hasLooseTop0 )  {
							//cout<<"case 12"<<endl;
							//cout<<bTags1.size()<<endl;
							for( size_t i=0; i<noTags1.size(); i++ )  {
								double pt = noTags1.at(i)->pt();
								int bin     = wMistag_      ->  FindBin( pt );
								double weight = wMistag_    ->  GetBinContent( bin ) ; //dummy value
								double mistagError = wMistag_ ->GetBinError( bin );

								p4_top1 = noTags1.at(i)->p4() + bTags1.at(0)->p4();

								histograms1d["topMassPred"]     ->   Fill( p4_top1.mass(), weight*evtWeight );
								if( p4_top1.mass() > topMassMin_ && p4_top1.mass() < topMassMax_ )  {
									
									if (verbose_) cout<<" Type 22 background estimation event "<<endl;
									if (verbose_) cout<<"   hasLooseTop0. hemi 1 has 0 b-tags and p4_top1.mass() "<<p4_top1.mass()<<endl;
									
									passTopMass1 = true;
									histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
									histograms1d["Nevents_Type22_Case123"]->Fill(3,evtWeight);

									double ttMass = (p4_top0+p4_top1).mass() ;
									histograms1d["ttMassType22_predicted"]      ->  Fill( ttMass, weight*evtWeight );
									histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );

									//ttMassPredictedDistribution_type22          ->      Accumulate( ttMass, pt, 1,  evtWeight );
								}
							}
						}        
					} // hasWTag0 
					else  {
						//cout<<"case 2"<<endl;
						bool passTopMass0 = false;
						p4_top0.SetPxPyPzE(0,0,0,0);
						if( hasTightTop1 )  {
							//cout<<"case 20"<<endl;
							for( size_t i=0; i<noTags0.size(); i++ )  {
								double pt = noTags0.at(i)->pt();
								int   bin   =   wMistag_      ->  FindBin( pt );
								double weight = wMistag_      ->  GetBinContent( bin );  //dummy value, depend on pt
								double mistagError = wMistag_ ->GetBinError( bin );

								if( hasBTag0 )  {
									p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
									histograms1d["topMassPred"]     ->  Fill( p4_top0.mass(), weight*evtWeight );
									if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
										
										if (verbose_) cout<<" Type 22 background estimation event "<<endl;
										if (verbose_) cout<<"   hasTightTop1. hemi 0 has b-tag and p4_top0.mass() "<<p4_top0.mass()<<endl;
										
										
										passTopMass0 = true;
										histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
										histograms1d["Nevents_Type22_Case123"]->Fill(1,evtWeight);

										double ttMass = (p4_top0+p4_top1).mass() ;
										histograms1d["ttMassType22_predicted"]      ->  Fill( ttMass, weight*evtWeight );
										histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );

										//ttMassPredictedDistribution_type22       ->      Accumulate( ttMass, pt, 1,  evtWeight );
									}
								}
								else {
									double minDr = 9999.0;
									pat::Jet const * nearestJet=NULL;
									for( size_t j=0; j<noTags0.size(); j++ )  {
										if( i==j )   continue;
										double dR = reco::deltaR<double>( noTags0.at(i)->eta(), noTags0.at(i)->phi(),
																		 noTags0.at(j)->eta(), noTags0.at(j)->phi() );
										if( dR < minDr )  {
											minDr = dR ;
											nearestJet = &(*noTags0.at(j));
										}
									} //end j
									if( nearestJet )  {
										//cout<<"case 22"<<endl;
										p4_top0 = noTags0.at(i)->p4() + nearestJet->p4();
										int   bin1  =  wMistag_       ->  FindBin( nearestJet->pt() );
										double weight1  = wMistag_    ->  GetBinContent( bin1 );
										double mistagError1 = wMistag_ ->GetBinError( bin1 );

										weight *= (1-weight1);
										histograms1d["topMassPred"]   ->  Fill( p4_top0.mass(), weight*evtWeight );
										if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
											
											if (verbose_) cout<<" Type 22 background estimation event "<<endl;
											if (verbose_) cout<<"   hasTightTop1. hemi 0 has 0 b-tags and p4_top0.mass() "<<p4_top0.mass()<<endl;
											
											passTopMass0 = true;
											histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
											histograms1d["Nevents_Type22_Case123"]->Fill(2,evtWeight);

											double ttMass = (p4_top0+p4_top1).mass() ;
											histograms1d["ttMassType22_predicted"]    ->  Fill( ttMass, weight*evtWeight );
											histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );

											//ttMassPredictedDistribution_type22      ->      Accumulate( ttMass, pt, 1,  (1-weight1)*evtWeight );
										}
									}
								}  // end else
							}  // end i
						} //hasTightTop
						else if( hasLooseTop1 )  {
							//cout<<"case 23"<<endl;
							for( size_t i=0; i<noTags0.size(); i++ )  {
								double pt = noTags0.at(i)->pt();
								int   bin =   wMistag_    ->  FindBin( pt );
								double weight = wMistag_  ->  GetBinContent( bin );  //dummy value
								double mistagError = wMistag_ ->GetBinError( bin );

								p4_top0 = noTags0.at(i)->p4() + bTags0.at(0)->p4();
								histograms1d["topMassPred"]     ->   Fill( p4_top0.mass(), weight*evtWeight );

								if( p4_top0.mass() > topMassMin_ && p4_top0.mass() < topMassMax_ )  {
									
									if (verbose_) cout<<" Type 22 background estimation event "<<endl;
									if (verbose_) cout<<"   hasLooseTop1. p4_top0.mass() "<<p4_top0.mass()<<endl;
									
									passTopMass0 = true;
									histograms1d["Nevents_11sig_12sig_22sig_11bkg_12bkg_22bkg"]->Fill(6,evtWeight);
									histograms1d["Nevents_Type22_Case123"]->Fill(3,evtWeight);

									double ttMass = (p4_top0+p4_top1).mass() ;
									histograms1d["ttMassType22_predicted"]      ->  Fill( ttMass, weight*evtWeight );
									histograms1d["ttMassType22_predicted_errorSquared"]      ->  Fill( ttMass, mistagError*mistagError );

									//ttMassPredictedDistribution_type22      ->      Accumulate( ttMass, pt, 1, evtWeight );
								}
							}
						}
					} // else 
				} // end type 2+2 background estimation
			}//end cascading cuts
		}//end if preselected
	}//end if passType11 && passType22
}//end analyze



