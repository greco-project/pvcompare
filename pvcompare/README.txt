Instructions for running run_sector_coupling_scenarios.py

Note: For the examinations in the working paper with the titel "The influence of innovative photovoltaictechnologies on urban energy systems - An energy system analysis with concentrator PV,perovskite-silicon PV and PV-powered heat pumps incomparison with state-of-the-art technologies"
simulations have been run, which have a Li-ion battery connected to the electricity bus as a storage component.
In the studies of the master thesis entitled "Modellierung und Analyse von sektorgekoppelten Energiesystemen mit photovoltaisch betriebenen Wärmepumpen und thermischen Energiespeichern",
Li-ion batteries are not considered in the simulations, since the analyses there focus on the influence of the
thermal components on corresponding KPIs.

1. Please make sure to add input data first by obtaining it from:

		~/[...]/pvcompare/pvcompare/data/user_inputs_collection/run_sector_coupling_scenarios/

	Choose whether you want to simulate

		A. with (directory: with_battery) or
		B. without (directory: without_battery)

	battery and copy the repective data to

	a. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs/ in case of simulating RefE scenarios
	b. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs_sector_coupling/ in case of simulating sector coupling scenarios A, B, C and D
	c. ~/[...]/pvcompare/pvcompare/data/user_inputs/mvs_inputs_sector_coupling_gas/ in case of simulating RefG scenarios

2. Please set facades to True if you want to simulate facades

3. Please set install_max_cap_pv to True if you want to simulate the maximum installable capacity

4. Please uncomment the scenarios you want to simulate
	e.g.:
		    # scenarios.run_scenario_RefE1()
		->  scenarios.run_scenario_RefE1()

5. Run the script



----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with "~/[...]/" as the path to your locally cloned repositories
