from pvcompare import check_inputs
import pvcompare.main as main
import pvcompare.constants as constants
import os
import pandas as pd
import shutil
import glob
import matplotlib.pyplot as plt
import logging
import numpy as np
import seaborn as sns

sns.set()


def create_loop_output_structure(outputs_directory, scenario_name, variable_name):
    """
    Defines the path of the loop_output_directory.

    Parameters
    ----------
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY.
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    variable_name: str
        name of the variable that is atapted in each loop.

    Returns
    -------
    str
        path of the loop_output_directory.
    """

    # defines scenario folder and loop_output_directory
    scenario_folder = os.path.join(outputs_directory, scenario_name)
    # creates scenario folder if it doesn't exist yet
    if not os.path.isdir(scenario_folder):
        # create scenario folder
        os.mkdir(scenario_folder)

    #  defines loop output directory in scenario_folder
    loop_output_directory = os.path.join(
        scenario_folder, "loop_outputs_" + str(variable_name)
    )

    # checks if loop_output_directory already exists, otherwise create it
    if os.path.isdir(loop_output_directory):
        raise NameError(
            f"The loop output directory {loop_output_directory} "
            f"already exists. Please "
            f"delete the existing folder or rename {scenario_name}."
        )
    else:
        os.mkdir(loop_output_directory)

    # create two folder in loop_output_directories for "scalars" and "timeseries"
    os.mkdir(os.path.join(loop_output_directory, "scalars"))
    os.mkdir(os.path.join(loop_output_directory, "timeseries"))

    return loop_output_directory


def loop_pvcompare(
    scenario_name,
    latitude,
    longitude,
    years,
    storeys,
    country,
    loop_type,
    loop_dict=None,
    pv_setup=None,
    user_inputs_mvs_directory=None,
    outputs_directory=None,
    user_inputs_pvcompare_directory=None,
):
    """
    Starts multiple *pvcompare* simulations with a range of values for a
    specific loop type.

    The loop type corresponds to a variable or a set of
    variables that is/are changed in each loop.The
    results, stored in two excel sheets, are copied into `loop_output_directory`.

    Parameters
    ----------
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    latitude: float
        latitude of the location
    longitude: foat
        longitude of the location
    years: list
        year(s) of simulation
    storeys: int
        number of storeys
    country: str
        country of location
    loop_type: str
        possible values: 'location', 'year', 'storeys', 'technology', 'hp_temp'.
        Defines the variable or variables that are changed with each loop.
    loop_dict: dict
        For location, the form of the dict should be: {"step1": ["country", "lat", "lon"], "step2": ["country", "lat", "lon"], etc}.
        For technology, the form of the dict should be: {"step1": "si", "step2": "cpv", "step3": "psi"}
        For year/storeys/hp_temp, the form of the dict should be: {"start": "1", "stop": "10", "step": "2"}
    pv_setup: dict or None
        If `pv_setup` is None, it is loaded from the `input_directory/pv_setup.cvs`.
        Default: None.
    user_inputs_mvs_directory: str or None
        Default: `user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY`
    outputs_directory: str or None
        Path to output directory.
        Default: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`
    user_inputs_pvcompare_directory: str or None
        If None, `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used
        as user_input_directory. Default: None.

    Returns
    -------
        None
    """
    # checks of outputs_directory and user_inputs_mvs_directory is None
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )

    loop_output_directory = create_loop_output_structure(
        outputs_directory=outputs_directory,
        scenario_name=scenario_name,
        variable_name=loop_type,
    )

    for year in years:
        if loop_type is "location":
            for key in loop_dict:
                country = loop_dict[key][0]
                latitude = loop_dict[key][1]
                longitude = loop_dict[key][2]

                single_loop_pvcompare(
                    scenario_name=scenario_name,
                    storeys=storeys,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    year=year,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    outputs_directory=outputs_directory,
                    plot=False,
                    pv_setup=pv_setup,
                    loop_output_directory=loop_output_directory,
                    step=str(latitude) + "_" + str(longitude),
                    loop_type=loop_type,
                )

        elif loop_type is "year":

            year = loop_dict["start"]
            while year <= loop_dict["stop"]:

                single_loop_pvcompare(
                    scenario_name=scenario_name,
                    storeys=storeys,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    year=year,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    outputs_directory=outputs_directory,
                    plot=False,
                    pv_setup=pv_setup,
                    loop_output_directory=loop_output_directory,
                    step=year,
                    loop_type=loop_type,
                )
                year = year + loop_dict["step"]

        elif loop_type is "storeys":

            number_of_storeys = loop_dict["start"]
            while number_of_storeys <= loop_dict["stop"]:

                single_loop_pvcompare(
                    scenario_name=scenario_name,
                    storeys=number_of_storeys,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    year=year,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    outputs_directory=outputs_directory,
                    plot=False,
                    pv_setup=pv_setup,
                    loop_output_directory=loop_output_directory,
                    step=number_of_storeys,
                    loop_type=loop_type,
                )

                number_of_storeys = number_of_storeys + loop_dict["step"]

        elif loop_type is "technology":

            for key in loop_dict:
                technology = loop_dict[key]

                data_path = os.path.join(
                    user_inputs_pvcompare_directory, "pv_setup.csv"
                )
                # load input parameters from pv_setup.csv
                pv_setup = pd.read_csv(data_path)
                for i, row in pv_setup.iterrows():
                    pv_setup.at[i, "technology"] = technology
                pv_setup.to_csv(data_path, index=False)

                single_loop_pvcompare(
                    scenario_name=scenario_name,
                    storeys=storeys,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    year=year,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    outputs_directory=outputs_directory,
                    plot=False,
                    pv_setup=None,
                    loop_output_directory=loop_output_directory,
                    step=technology,
                    loop_type=loop_type,
                )

        elif loop_type is "hp_temp":
            temp_high = loop_dict["start"]

            data_path = os.path.join(
                user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
            )
            while temp_high <= loop_dict["stop"]:
                # load input parameters from pv_setup.csv
                hp_file = pd.read_csv(data_path, index_col=0)
                hp_file.at["heat_pump", "temp_high"] = temp_high
                hp_file.to_csv(data_path)

                single_loop_pvcompare(
                    scenario_name=scenario_name,
                    storeys=storeys,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    year=year,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    outputs_directory=outputs_directory,
                    plot=False,
                    pv_setup=pv_setup,
                    loop_output_directory=loop_output_directory,
                    step=temp_high,
                    loop_type=loop_type,
                )
                temp_high = temp_high + loop_dict["step"]

    logging.info("starting postprocessing KPI")
    postprocessing_kpi(scenario_name=scenario_name, outputs_directory=outputs_directory)


def single_loop_pvcompare(
    scenario_name,
    storeys,
    country,
    latitude,
    longitude,
    year,
    user_inputs_pvcompare_directory,
    user_inputs_mvs_directory,
    outputs_directory,
    plot,
    pv_setup,
    loop_output_directory,
    loop_type,
    step,
):
    """

    Parameters
    ----------
    scenario_name: str
        name of the scenario.
    storeys: int
        number of storeys
    country: str
        country name
    latitude: float
        latitude of the location
    longitude: foat
        longitude of the location
    year: int
        year
    user_inputs_pvcompare_directory: str or None
        If None, `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used
        as user_input_directory. Default: None.
    user_inputs_mvs_directory: str or None
        Default: `user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY`
    outputs_directory: str or None
        Path to output directory.
        Default: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`
    plot: bool
        default: False
    loop_output_directory: str
        output directory defined in 'pvcompare.outputs.create_loop_output_structure()'.
    loop_type: str
        possible values: 'location', 'year', 'storeys', 'technology', 'hp_temp'.
        Defines the variable or variables that are changed with each loop.
    step: str or int
        Gradation of the loop variable.

    Returns
    -------
        None
    """

    main.apply_pvcompare(
        storeys=storeys,
        country=country,
        latitude=latitude,
        longitude=longitude,
        year=year,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        plot=plot,
        pv_setup=pv_setup,
    )

    # define mvs_output_directory for every looping step
    mvs_output_directory = os.path.join(
        outputs_directory,
        scenario_name,
        "mvs_outputs_loop_" + str(loop_type) + "_" + str(year) + "_" + str(step),
    )

    main.apply_mvs(
        scenario_name,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_output_directory=mvs_output_directory,
        outputs_directory=outputs_directory,
    )

    excel_file1 = "scalars.xlsx"
    new_excel_file1 = "scalars_" + str(year) + "_" + str(step) + ".xlsx"
    src_dir = os.path.join(mvs_output_directory, excel_file1)
    dst_dir = os.path.join(loop_output_directory, "scalars", new_excel_file1)
    shutil.copy(src_dir, dst_dir)

    excel_file2 = "timeseries_all_busses.xlsx"
    new_excel_file2 = (
        "timeseries_all_busses_" + "_" + str(year) + "_" + str(step) + ".xlsx"
    )
    src_dir = os.path.join(mvs_output_directory, excel_file2)
    dst_dir = os.path.join(loop_output_directory, "timeseries", new_excel_file2)
    shutil.copy(src_dir, dst_dir)


def loop_mvs(
    latitude,
    longitude,
    years,
    storeys,
    country,
    variable_name,
    variable_column,
    csv_file_variable,
    start,
    stop,
    step,
    scenario_name,
    user_inputs_mvs_directory=None,
    outputs_directory=None,
):
    """
    Starts multiple MVS simulations with a range of values for a specific parameter.

    This function applies :py:func:`~.main.apply_pvcompare`, one time. After that
     :py:func:`~.main.apply_mvs` is executed in a loop.
     Before each loop a specific variable value is changed. The
    results, stored in two excel sheets, are copied into `loop_output_directory`.

    Parameters
    ----------
    latitude: float
        latitude of the location
    longitude: foat
        longitude of the location
    years: list
        year(s) for simulation
    storeys:int
        number of storeys
    country: str
        country of location
    variable_name: str
        name of the variable that is atapted in each loop
    variable_column: str
        name of the  variable column in the csv file
    csv_file_variable: str
        name of the csv file the variable is saved in
    start: int
        first value of the variable
    stop: int
        last value of the variable. notice that stop > start
    step: int
        step of increase
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    user_inputs_mvs_directory: str or None
        Default: `user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY`
    outputs_directory: str or None
        Path to output directory.
        Default: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`

    Returns
    -------

    """

    if outputs_directory is None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
    loop_output_directory = create_loop_output_structure(
        outputs_directory, scenario_name, variable_name
    )
    # define filename of variable that should be looped over
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    csv_filename = os.path.join(
        user_inputs_mvs_directory, "csv_elements", csv_file_variable
    )

    # loop over years
    for year in years:
        # apply pvcompare
        main.apply_pvcompare(
            latitude=latitude,
            longitude=longitude,
            year=year,
            storeys=storeys,
            country=country,
            user_inputs_mvs_directory=user_inputs_mvs_directory,
        )

        # loop over the variable
        i = start
        while i <= stop:
            # change variable value and save this value to csv
            csv_file = pd.read_csv(csv_filename, index_col=0)
            csv_file.loc[[variable_name], [variable_column]] = i
            csv_file.to_csv(csv_filename)

            # define mvs_output_directory for every looping step
            mvs_output_directory = os.path.join(
                outputs_directory,
                scenario_name,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(i),
            )

            # apply mvs for every looping step
            main.apply_mvs(
                scenario_name=scenario_name,
                mvs_output_directory=mvs_output_directory,
                user_inputs_mvs_directory=user_inputs_mvs_directory,
                outputs_directory=outputs_directory,
            )

            # copy excel sheets to loop_output_directory
            number_digits = len(str(stop)) - len(str(i))

            if number_digits == 0:
                j = str(i)
            elif number_digits == 1:
                j = "0" + str(i)
            elif number_digits == 2:
                j = "00" + str(i)
            elif number_digits == 3:
                j = "000" + str(i)
            elif number_digits == 4:
                j = "0000" + str(i)

            excel_file1 = "scalars.xlsx"
            new_excel_file1 = "scalars_" + str(year) + "_" + str(j) + ".xlsx"
            src_dir = os.path.join(mvs_output_directory, excel_file1)
            dst_dir = os.path.join(loop_output_directory, "scalars", new_excel_file1)
            shutil.copy(src_dir, dst_dir)

            excel_file2 = "timeseries_all_busses.xlsx"
            new_excel_file2 = (
                "timeseries_all_busses_" + str(year) + "_" + str(j) + ".xlsx"
            )
            src_dir = os.path.join(mvs_output_directory, excel_file2)
            dst_dir = os.path.join(loop_output_directory, "timeseries", new_excel_file2)
            shutil.copy(src_dir, dst_dir)

            # add another step
            i = i + step
    logging.info("starting postprocessing KPI")
    postprocessing_kpi(scenario_name=scenario_name, outputs_directory=outputs_directory, variable_name=variable_name)



def postprocessing_kpi(scenario_name, variable_name, outputs_directory=None):
    """
    Overwrites all output excel files "timeseries_all_flows.xlsx" and "scalars.xlsx"
    in loop output directory of a scenario with modified KPI's.

    1) Creates new sheet "Electricity bus1" with the column
    Electricity demand = Electricity demand + Heat pump.
    2) Creates new sheets in scalars.xlsx with KPI's adjusted to the new demand.

    :param scenario_name: str
        scenario name
    :param outputs_directory: str
        output directory
    :return:
    """
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
        scenario_folder = os.path.join(outputs_directory, scenario_name)
    else:
        scenario_folder = os.path.join(outputs_directory, scenario_name)
        if not os.path.isdir(scenario_folder):
            logging.warning(f"The scenario folder {scenario_name} does not exist.")
    # get all variable names in scenario folder
    # list_var_name = []
    # for fname in list(glob.glob(os.path.join(scenario_folder, "*"))):
    #     folder_name = fname.split("/")[::-1][0]
    #     if folder_name.startswith("loop"):
    #         split_path = folder_name.split("_")
    #         get_var_name = split_path[::-1][0]
    #         list_var_name.append(get_var_name)
    # # loop over all loop output folders with variable name
    loop_output_directory = os.path.join(
        scenario_folder, "loop_outputs_" + str(variable_name)
    )
    if not os.path.isdir(loop_output_directory):
        logging.warning(
            f"The loop output folder {loop_output_directory} does not exist. "
            f"Please check the variable_name"
        )
    # parse through scalars folder and read in all excel sheets
    for filepath_s in list(
        glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
    ):
        scalars = pd.read_excel(filepath_s, sheet_name=None)

        # get variable value from filepath
        split_path = filepath_s.split("_")
        get_year = split_path[::-1][1]
        get_step = split_path[::-1][0]
        ending = str(get_year) + "_" + str(get_step)

        # load timeseries_all_busses
        for filepath_t in list(
            glob.glob(os.path.join(loop_output_directory, "timeseries", "*.xlsx"))
        ):
            if filepath_t.endswith(ending) is True:
                timeseries = pd.read_excel(filepath_t, sheet_name="Electricity bus")
                if "Heat pump" in timeseries.columns:
                    electricity_demand = (
                        timeseries["Electricity demand"] + timeseries["Heat pump"]
                    )
                    timeseries["Electricity demand"] = electricity_demand
                    with pd.ExcelWriter(filepath_t, mode="a") as writer:
                        timeseries.to_excel(writer, sheet_name="Electricity bus")
                    logging.info(
                        f"The timeseries_all_flows file {filepath_t} has been overwritten with the new electricity demand."
                    )
                else:
                    electricity_demand = timeseries["Electricity demand"]
        # read sheets of scalars
        file_sheet1 = scalars["cost_matrix"]
        file_sheet2 = scalars["scalar_matrix"]
        file_sheet2.index = file_sheet2["label"]
        file_sheet3 = scalars["scalars"]
        file_sheet3.index = file_sheet3.iloc[:, 0]
        file_sheet4 = scalars["KPI individual sectors"]

        # recalculate KPI
        file_sheet2.at["Electricity demand", "total_flow"] = sum(
            electricity_demand
        ) * (-1)
        file_sheet3.at["Total_demandElectricity", 0] = sum(electricity_demand) * (
            -1
        )
        file_sheet3.at["Degree of NZE", 0] = (
            file_sheet3.at["Total internal renewable generation", 0]
            - file_sheet3.at["Total_excessElectricity", 0]
        ) / file_sheet3.at["Total_demandElectricity", 0]
        file_sheet3.at["Degree of autonomy", 0] = (
            file_sheet3.at["Total_demandElectricity", 0]
            - file_sheet3.at["Total_consumption_from_energy_providerElectricity", 0]
        ) / file_sheet3.at["Total_demandElectricity", 0]
        file_sheet3.at["Onsite energy fraction", 0] = (
            file_sheet3.at["Total_demandElectricity", 0]
            - file_sheet3.at["Total_feedinElectricity", 0]
        ) / file_sheet3.at["Total internal renewable generation", 0]

        # save excel sheets
        with pd.ExcelWriter(filepath_s, mode="a") as writer:
            file_sheet1.to_excel(writer, sheet_name="cost_matrix", index=None)
            file_sheet2.to_excel(writer, sheet_name="scalar_matrix", index=None)
            file_sheet3.to_excel(writer, sheet_name="scalars", index=None)
            file_sheet4.to_excel(
                writer, sheet_name="KPI individual sectors", index=None
            )
        logging.info(
            f"Scalars file sheet {filepath_s} has been overwritten with new KPI's"
        )

def plot_lifetime_specificosts_psi(scenario_dict, variable_name, outputs_directory, basis_value):
    """

    :param scenario_dict:
    :return:
    """
    LCOE = pd.DataFrame()
    INSTCAP = pd.DataFrame()
    TOTALCOSTS = pd.DataFrame()
    for scenario_name in scenario_dict.keys():
        sc_step = scenario_name.split("_")[::-1][0]
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )
        # parse through scalars folder and read in all excel sheets
        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):

            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            lt_step = int(get_step.split(".")[0])

            # load timeseries_all_busses
            for filepath_t in list(
                glob.glob(os.path.join(loop_output_directory, "timeseries", "*.xlsx"))
            ):
                if filepath_t.endswith(ending) is True:
                    timeseries = pd.read_excel(filepath_t, sheet_name="Electricity bus")
                    if "Heat pump" in timeseries.columns:
                        electricity_demand = (
                            timeseries["Electricity demand"] + timeseries["Heat pump"]
                        )
                        timeseries["Electricity demand"] = electricity_demand
                        with pd.ExcelWriter(filepath_t, mode="a") as writer:
                            timeseries.to_excel(writer, sheet_name="Electricity bus")
                        logging.info(
                            f"The timeseries_all_flows file {filepath_t} has been overwritten with the new electricity demand."
                        )
                    else:
                        electricity_demand = timeseries["Electricity demand"]
            # read sheets of scalars
            file_sheet1 = scalars["cost_matrix"]
            file_sheet2 = scalars["scalar_matrix"]
            file_sheet2.index = file_sheet2["label"]
            file_sheet3 = scalars["scalars"]
            file_sheet3.index = file_sheet3.iloc[:, 0]
            file_sheet4 = scalars["KPI individual sectors"]

            # get LCOE pv and installed capacity
            index = lt_step
            column = str(sc_step)
#            LCOE.loc[index, "step"] = int(step)
            INSTCAP.loc[index, column] = file_sheet2.at[
                "PV psi", "optimizedAddCap"]
            LCOE.loc[index, column] = file_sheet1.at[
                "PV psi", "levelized_cost_of_energy_of_asset"
            ]
            TOTALCOSTS.loc[index, column] = file_sheet1.at[
                "PV psi", "costs_total"
            ]


    LCOE.sort_index(ascending=False, inplace=True)
    INSTCAP.sort_index(ascending=False, inplace=True)
    TOTALCOSTS.sort_index(ascending=False, inplace=True)
    # select values close to basis value
    basis = pd.DataFrame()
    for column in LCOE.columns:
        value = LCOE[column].iloc[(LCOE[column]-basis_value).abs().argsort()[:1]]
        if value.index[0] is not None:
            basis.loc[column, "lifetime"] = int(value.index[0])

    # plot LCOE
    f, (ax1, ax3) = plt.subplots(1, 2, figsize=(20, 9))
    plt.tick_params(bottom='on')
    sns.set_style("whitegrid", {'axes.grid': False})
    ax1 = plt.subplot(121)
    ax1 = sns.heatmap(LCOE, cmap="YlGnBu",cbar_kws={'label': 'LCOE in EUR/kWh'})
    ax1.set_ylabel("lifetime in years")
    ax1.set_xlabel("specific_costs in EUR")
#    sns.lineplot(basis.columns, basis[0], ax = ax1)
    ax2=ax1.twinx()
    ax2.plot(basis.index, basis["lifetime"],color='darkorange', label = "SI")
#    line = ax1.lines[0] # get the line
#    line.set_xdata(line.get_xdata() + 0.5)
#    ax1.axis('tight')
#    ax1.set_xticks()
    ax2.set_ylim(5, 25.5)
    ax2.axis('off')



    ax3 =plt.subplot(122)
    ax3 = sns.heatmap(TOTALCOSTS, cmap="YlGnBu", cbar_kws={'label': 'Total costs PV in EUR'})
    ax3.set_ylabel("lifetime in years")
    ax3.set_xlabel("specific costs in EUR")

    plt.tight_layout()

    f.savefig(
        os.path.join(
            outputs_directory,
            "plot_PV_COSTS_LCOE_PSI_Spain_2015.png",
        )
    )



if __name__ == "__main__":
    latitude = 52.5243700
    longitude = 13.4105300
    years = [2011, 2015]  # a year between 2011-2013!!!
    storeys = 5
    country = "Germany"
    scenario_name = "Scenario_A2"

    loop_type = "storeys"

    if loop_type == "storeys":
        loop_dict = {"start": 3, "stop": 5, "step": 1}
    elif loop_type == "technology":
        loop_dict = {"step1": "cpv", "step2": "si", "step3": "psi"}
    elif loop_type == "hp_temp":
        loop_dict = {"start": 15, "stop": 25, "step": 5}
    elif loop_type == "year":
        loop_dict = {"start": 2010, "stop": 2017, "step": 1}

    # loop_pvcompare(
    #     scenario_name=scenario_name,
    #     latitude=latitude,
    #     longitude=longitude,
    #     years=years,
    #     storeys=storeys,
    #     country=country,
    #     loop_type=loop_type,
    #     loop_dict=loop_dict,
    #     user_inputs_mvs_directory=None,
    #     outputs_directory=None,
    #     user_inputs_pvcompare_directory=None,
    # )
    #
    # loop_mvs(
    #     latitude=latitude,
    #     longitude=longitude,
    #     years=years,
    #     storeys=storeys,
    #     country=country,
    #     variable_name="specific_costs",
    #     variable_column="PV si",
    #     csv_file_variable="energyProduction.csv",
    #     start=500,
    #     stop=600,
    #     step=100,
    #     outputs_directory=None,
    #     user_inputs_mvs_directory=None,
    #     scenario_name=scenario_name,
    # )

    # plot_all_flows(
    #     scenario_name=scenario_name,
    #     month=None,
    #     calendar_week=None,
    #     weekday=5,
    #     timeseries_directory=os.path.join(
    #         constants.DEFAULT_OUTPUTS_DIRECTORY,
    #         scenario_name,
    #         "mvs_outputs_loop_hp_temp_15",
    #     ),
    # )

    # scenario_dict = {"Scenario_A3": "psi", "Scenario_A5": "cpv", "Scenario_A7": "Basis"} # Basis scenarios need to be called "Basis"
    # plot_kpi_loop(
    #     scenario_dict=scenario_dict,
    #     variable_name="specific_costs", #specific_costs
    #     kpi=[
    #         "Installed capacity PV",
    #         "LCOE PV",
    #         "Total costs PV",
    #         "Total annual production",
    #         "Degree of NZE",
    #     ],
    # )
    #
    # compare_weather_years(
    #     latitude=latitude,
    #     longitude=longitude,
    #     country=country,
    #     static_inputs_directory=None,
    # )

#    postprocessing_kpi(scenario_name="Scenario_A6", variable_name="specific_costs", outputs_directory=None)

    scenario_dict = {"Scenario_C_500": "500", "Scenario_C_600": "600", "Scenario_C_700": "700", "Scenario_C_800": "800", "Scenario_C_900": "900", "Scenario_C_1000": "1000", "Scenario_C_1100": "1100"}
    plot_lifetime_specificosts_psi(scenario_dict, variable_name="lifetime",
                                   basis_value= 0.083,# basis_value Germany, 2016, SI = 0.124, basis_value_spain_2015 =  0,083
                                   outputs_directory=None)
