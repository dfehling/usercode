#!/usr/bin/env python

import subprocess

class SystVar :
    def __init__(self,name,val,extraFlags=None) :
        self.name = name
        self.val = val
        self.extraFlags = extraFlags

class Sample :
    def __init__(self, directory, title, jersys=True, jecsys=True, pdfsys=True, extraFlags='' ) :
        self.directory=directory
        self.title=title
        self.extraFlags=extraFlags
        self.systs = []
        noms = [
            SystVar(name='', val=extraFlags)
            ]
        jersysts = [
            SystVar(name='_jerup', val='--jerSys=0.2',extraFlags=extraFlags),
            SystVar(name='_jerdn', val='--jerSys=0.0',extraFlags=extraFlags)
            ]
        jecsysts = [
            SystVar(name='_jecup', val='--jecSys=1.0',extraFlags=extraFlags),
            SystVar(name='_jecdn', val='--jecSys=-1.0', extraFlags=extraFlags)
            ]
        pdfsysts = [
            SystVar(name='_pdfup', val='--pdfSys=1.0',extraFlags=extraFlags),
            SystVar(name='_pdfdn', val='--pdfSys=-1.0',extraFlags=extraFlags)
            ]
        if jersys == True :
            self.systs = self.systs + jersysts
        if jecsys == True :
            self.systs = self.systs + jecsysts
        if pdfsys == True :
            self.systs = self.systs + pdfsysts

        
def run_iheartny( sample ) :

    for isyst in sample.systs : 
        s = ['python', 'iheartny_topxs_fwlite.py','--files=' + sample.directory + '/res/*.root', '--outname=' + sample.title + isyst.name, isyst.val, isyst.extraFlags ]
        print 'Executing '
        print s
        subprocess.call ( s )
