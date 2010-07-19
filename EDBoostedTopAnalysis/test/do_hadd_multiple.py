#!/bin/python

import subprocess
import sys

dirs = [
    'QCDDiJet_Pt0to15_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt1000to1400_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt120to170_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt1400to1800_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt15to20_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt170to230_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt1800to2200_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt20to30_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt2200to2600_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt230to300_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt2600to3000_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt3000to3500_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt300to380_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt30to50_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt380to470_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt470to600_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt50to80_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt600to800_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt800to1000_reweighted_pt_gt25_templates',
    'QCDDiJet_Pt80to120_reweighted_pt_gt25_templates'
    ]

for idir in dirs :
        s = "hadd " + idir + '.root ' + idir + '/res/*.root'
	print s
	subprocess.call( [s, ""], shell=True )
                

