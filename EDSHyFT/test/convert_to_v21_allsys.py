#! /bin/python

from string import *

crabFileStrs = [
    ['crab_InclusiveMu15_shyftana_38xOn35x_v13_anashyft.cfg',                 'InclusiveMu15_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',   'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',   'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',  'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',            'TTbarJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_VqqJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',              'VqqJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_WJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',                'WJets-madgraph_shyftana_38xOn35x_v21_allsys'],
    ['crab_ZJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',                'ZJets-madgraph_shyftana_38xOn35x_v21_allsys']

    ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on file ' + crabFileStr[0] + ' ---------------------------'
    f = open(crabFileStr[0], 'r')
    instring = f.read()
#    print instring
    a =  instring.replace( 'shyftana_38xOn35x_v13', 'shyftana_38xOn35x_v21_allsys')
    aa= a.replace( 'number_of_jobs = 1', 'number_of_jobs = 10')    
    b = aa.replace( 'shyftEDAnalyzer', 'shyftEDAnalyzer_allsys' )
    d = b.replace( 'doMC=1 ', '')
    e = d.replace( 'return_data = 1', 'return_data = 1\nadditional_input_files = ttbarEffSF_unity.root')
#    print e
    outname = crabFileStr[0].replace( '38xOn35x_v13', '38xOn35x_v21_allsys')
    fout = open( outname, 'w')
    fout.write( e )
#    print '   ------ New ------'    

