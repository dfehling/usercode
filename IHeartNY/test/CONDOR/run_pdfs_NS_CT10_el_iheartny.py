#!/usr/bin/env python

from run_iheartny_unfold import run_threads, Sample

import shlex



samples = [
    
    #------------------------------    
    # Nominal samples, CT10
    #------------------------------
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_el',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_el',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_el',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_nom',
           flags='--semilep=-1.0 --pdfSys=0.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    
    #------------------------------    
    # PDF Up samples, CT10
    #------------------------------
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_el',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfup',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_el',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_el',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfup',
           flags='--semilep=-1.0 --pdfSys=1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

    #------------------------------    
    # PDF Down samples, CT10
    #------------------------------
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_inclusive_el',
           title='TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfdown',
           flags='--mttGenMax=700. --semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_700to1000_el',
           title='TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),
    Sample(directory='/eos/uscms/store/user/skinnari/Unfold_24feb2015/TT_1000toInf_el',
           title='TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_el_CT10_pdfdown',
           flags='--semilep=-1.0 --pdfSys=-1.0 --pdfSet=0.0 --lepType=ele',
           pdfsys=False, noms=True, jersys=True, jecsys=True, btagsys=True, toptagsys=True, qcd=True
    ),

]


run_threads( samples )
# Now the threads are done, exit gracefully
#print 'So long, and thanks for all the fish!'
