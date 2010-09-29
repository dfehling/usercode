# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/SHyFT/CMSSW_3_8_3_SHyFT/src/Analysis/EDSHyFT/test'




crabFiles = [
    ## ['crab_InclusiveMu15_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_WJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_ZJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],
    ## ['crab_VqqJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET'],

    ## ['crab_InclusiveMu15_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_WJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_ZJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    ## ['crab_VqqJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT'],
    
    ['crab_InclusiveMu15_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v10_bdisc'],
    ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_WJets-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_ZJets-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v10_bdisc'],
    ['crab_VqqJets-madgraph_shyftana_38xOn35x_v10_bdisc_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v10_bdisc']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
