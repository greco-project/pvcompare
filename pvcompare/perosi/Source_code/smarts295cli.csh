#!/bin/csh 
# The hypothetical files smarts_01.inp.txt, smarts_02.inp.txt, 
#                        smarts_03.inp.txt, smarts_04.inp.txt, 
#                        smarts_june.inp.txt, smarts_july.inp.txt, 
#	                 smarts_20050910.inp.txt
# are assumed to reside in the root directory of SMARTS.
# Change according to your needs.
# Compile the code for true batch mode. See QuickStart_linux295.doc
#
# Use "source smarts295cli.csh" to run this file
# or 
# chmod u+x smarts295cli.csh
# and then
# ./smarts95cli.csh
#
foreach i (01 02 03 04 june july 20050914)
cp -f smarts_$i.inp.txt smarts295.inp.txt
./smarts295
mv smarts295.out.txt smarts_$i.out.txt
mv smarts295.scn.txt smarts_$i.scn.txt
mv smarts295.ext.txt smarts_$i.ext.txt
end
