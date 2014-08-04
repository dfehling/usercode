#!/usr/bin/env python

from run_iheartny import run_threads, Sample

import shlex



samples = [
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--makeResponse  --semilep=1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--makeResponse  --semilep=1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--makeResponse --semilep=1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           flags='--semilep=-1.0',
           pdfsys=True, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_max700_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--mttGenMax=700. --semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-700to1000_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaledown_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),            
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/TT_Mtt-1000toInf_CT10_scaleup_TuneZ2star_8TeV-powheg-tauola',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup',
           flags='--semilep=-1.0',
           pdfsys=False, noms=True, jersys=False, jecsys=False, btagsys=False, toptagsys=False, qcd=False, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/skinnari/TopXS_June2014/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           title='W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu',
           pu='wjets', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sts', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stt', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttw', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='stsb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    ),
    Sample(directory='/uscms_data/d3/maral87/ntuples_TopXS/CMSSW_5_3_14_patch1/src/Analysis/IHeartNY/test/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           title='Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu',
           pu='sttwb', pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True, newiso=True
    )
]


run_threads( samples )
# Now the threads are done, exit gracefully
print 'So long, and thanks for all the fish!'
