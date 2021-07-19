# README

## Instructions for running scenarios with /pvcompare/run_sector_coupling_scenarios.py

Note: For the examinations in the working paper with the title "The influence of innovative photovoltaic technologies on urban energy systems - An energy system analysis with concentrator PV, perovskite-silicon PV and PV-powered heat pumps in comparison with state-of-the-art technologies",
simulations have been run, which have a Li-ion battery connected to the electricity bus as a storage component.

1. Copy the input data from

   ~/[...]/pvcompare/pvcompare/data/user_inputs_collection/run_sector_coupling_scenarios/with_battery

   to

   a. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs/ in case of simulating RefE scenarios
   b. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs_sector_coupling/ in case of simulating sector coupling scenarios A, B, C and D
   c. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs_sector_coupling_gas/ in case of simulating RefG scenarios

2. Please set `facades` to True if you want to simulate facades

3. Please set `install_max_cap_pv` to True if you want to simulate the maximum installable capacity

4. Please uncomment the scenarios you want to simulate
   For example:


    :::python


    # # scenarios.run_scenario_RefE1()

->

    :::python

    # scenarios.run_scenario_RefE1()

5. Run the script


---------------------------


with "~/[...]/" as the path to your locally cloned repositories
