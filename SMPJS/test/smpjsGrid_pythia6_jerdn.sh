# !/bin/sh

python smpjsGrid.py "$1" "5" "--files=/eos/uscms/store/user/smpjs/srappocc/QCD_Flat15to3000_pythia6_z2_ttbsm_v10beta_tuples_withgen_withnpv/res/\*.root" "--useMC " "--jerSmearVal=0.0"
