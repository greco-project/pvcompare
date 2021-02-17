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
                pv_setup.at[0, "technology"] = technology
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


def plot_all_flows(
    scenario_name=None,
    outputs_directory=None,
    timeseries_directory=None,
    timeseries_name="timeseries_all_busses.xlsx",
    month=None,
    calendar_week=None,
    weekday=None,
):

    """
    Plots all flows of the energy system for a given period of time.

    Parameters
    ----------
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str or None
        Path to the directory in which the plot should be saved.
        Default: None.
        If None: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`
    timeseries_directory: str or None
        Path to the timeseries directory.
        If None: `timeseries_directory = outputs_directory`.
        Default: None.
    timeseries_name: str or None
        Default: timeseries_all_busses.xlsx
    month: int
        Number of month that should be plotted.
        Only fill in a number here, if you want to plot over one month.
        If None: will plot over week, weekday or the whole year. Default: None
    calendar_week: int
        the week (number in calender weeks) that should be plotted.
        Only fill in a number here, if you want to plot over one a week or a weekday.
        if None: will plot over one month or the whole year. Default: None
    weekday: int
        The day of the caldendar_week (from 0-6 with 0 : Monday and 6: Sunday.
        If None: the next greater period is plotted. Default: None

    Returns
    -------
        None
        Saves figure into outputs_directory
    -------


    """
    # check if weekday is a valid day
    if weekday not in range(0, 6, 1):
        logging.error(
            "The weekday is not valid. Please choose a number "
            "between 0-6 with 0:Monaday and 6:Sunday."
        )

    # read timeseries
    # check if scenario is specified or the timeseries directory is given
    if timeseries_directory is None:
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
        scenario_folder = os.path.join(outputs_directory, scenario_name)
        if timeseries_directory == None:
            timeseries_directory = os.path.join(scenario_folder, "mvs_outputs")
        if not os.path.isdir(timeseries_directory):
            logging.warning(
                "The timeseries directory does not exist. Please check "
                "the scenario name or specify the timeseries directory."
            )
    df = pd.read_excel(
        os.path.join(timeseries_directory, timeseries_name),
        sheet_name="Electricity bus",
        index_col=0,
    )
    # Converting the index as date
    df.index = pd.to_datetime(df.index)

    # define period for the plot
    if month is None:
        if calendar_week is None:
            period = "year"
            pass
            if weekday is not None:
                logging.error(
                    "If you want to create a plot over one weekday, please "
                    "define a caldendar_week as well. Otherwise set"
                    " weekday to 'None'."
                )
        else:
            if weekday is not None:
                df = df[df.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
            else:
                df = df[df.index.week == calendar_week]
                period = "caldendar_week_" + str(calendar_week)
    else:
        if calendar_week is not None:
            if weekday is None:
                logging.warning(
                    "You inserted a month and a week. In this case the "
                    "plot will cover one caldendar_week. If you want to plot "
                    "over one month please set the calendar_week to 'None'"
                )
                df = df[df.index.week == calendar_week]
                period = "week_" + str(calendar_week)
            else:
                logging.warning(
                    "You inserted a month, a caldendar_week and a weekday. In this case the "
                    "plot will cover one weekday only. If you want to plot "
                    "over one month please set the caldendar_week and weekday to 'None'"
                )
                df = df[df.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
        else:
            df = df[df.index.month == month]
            period = "month_" + str(month)

    # plot
    plt.title("All Flows", color="black")
    df.plot().legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.xlabel("time")
    plt.ylabel("kW")

    # save plot into output directory
    plt.savefig(
        os.path.join(timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.png"),
        bbox_inches="tight",
    )


def plot_kpi_loop(
    variable_name, kpi, scenario_dict, outputs_directory=None,
):

    """
    Plots KPI's from the 'mvs_output/scalars_**.xlsx' files in `loop_outputs`
    for a loop over one variable.

    The plot is saved into the `loop_output_directory`.

    Parameters
    ----------
    variable_name: str
        Name of the variable that is changed each loop. Please do not enter
        white spaces within the string.
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Degree of NZE"
            "Costs total PV",
            "Installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy",
            "Total non-renewable energy use"
    scenario_dict: dictionary
        dictionary with the scenario names that should be compared as keys and
        a label for the scenario as value. e.g.: {"Scenario_A1" : "si", "Scenario_A2": "cpv"}
         Notice: all scenarios you want to compare, need to include the
         loop-outputs for the same variable / steps. The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY

    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------


    """
    output_dict = {}
    for scenario_name in scenario_dict.keys():
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
        output = pd.DataFrame()
        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):

            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            step = int(get_step.split(".")[0])
            year = int(split_path[::-1][1])
            # get all different pv assets
            csv_directory = os.path.join(
                scenario_folder,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(step),
                "inputs",
                "csv_elements",
            )
            energyProduction = pd.read_csv(
                os.path.join(csv_directory, "energyProduction.csv"), index_col=0
            )
            energyProduction = energyProduction.drop(["unit"], axis=1)
            pv_labels = energyProduction.columns
            # get total costs pv and installed capacity
            index = str(year) + "_" + str(step)
            output.loc[index, "step"] = int(step)
            output.loc[index, "year"] = int(year)
            for pv in pv_labels:
                output.loc[index, "Costs total PV"] = file_sheet1.at[pv, "costs_total"]
                output.loc[index, "Installed capacity PV"] = file_sheet2.at[
                    pv, "optimizedAddCap"
                ]
                output.loc[index, "Total renewable energy"] = file_sheet3.at[
                    "Total renewable energy use", 0
                ]
                output.loc[index, "Renewable factor"] = file_sheet3.at[
                    "Renewable factor", 0
                ]
                output.loc[index, "LCOE PV"] = file_sheet1.at[
                    pv, "levelized_cost_of_energy_of_asset"
                ]
                output.loc[index, "Self consumption"] = file_sheet3.at[
                    "Onsite energy fraction", 0
                ]
                output.loc[index, "Self sufficiency"] = file_sheet3.at[
                    "Onsite energy matching", 0
                ]
                output.loc[index, "Degree of autonomy"] = file_sheet3.at[
                    "Degree of autonomy", 0
                ]
                output.loc[index, "Total emissions"] = file_sheet3.at[
                    "Total emissions", 0
                ]
                output.loc[index, "Total non-renewable energy"] = file_sheet3.at[
                    "Total non-renewable energy use", 0
                ]
                output.loc[index, "Degree of NZE"] = file_sheet3.at["Degree of NZE", 0]

            output_dict_column = output.to_dict()
            output_dict[scenario_dict[scenario_name]] = output_dict_column

    # define y labels
    y_title = {
        "Costs total PV": "Costs total PV \n in EUR",
        "Installed capacity PV": "Installed capacity \nPV in kWp",
        "Total renewable energy": "Total renewable \nenergy in kWh",
        "Renewable factor": "Renewable factor \nin %",
        "LCOE PV": "LCOE PV \nin EUR/kWh",
        "Self consumption": "Self consumption \nin %",
        "Self sufficiency": "Self sufficiency \nin %",
        "Degree of autonomy": "Degree of \nautonomy in %",
        "Total emissions": "Total emissions \nin kgCO2eq/kWh",
        "Total non-renewable energy": "Total non-renewable \n energy in kWh",
        "Degree of NZE": "Degree of NZE \n in %",
    }

    output.sort_index(inplace=True)

    # plot
    hight = len(kpi) * 2
    fig = plt.figure(figsize=(7, hight))
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number
    for i in kpi:
        ax = fig.add_subplot(num)
        num = num + 1
        for key in output_dict.keys():
            df = pd.DataFrame()
            df = df.from_dict(output_dict[key])
            df.plot(
                x="step",
                y=i,
                style=".",
                ax=ax,
                label=key,
                legend=False,
                sharex=True,
                xticks=df.step,
            )
            ax.set_ylabel(y_title[i])
            ax.set_xlabel(variable_name)
            ax.get_yaxis().set_label_coords(-0.13, 0.5)
            ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.5)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        bbox_to_anchor=(0.96, 0.96),
        loc="upper right",
        borderaxespad=0.0,
    )

    plt.tight_layout()

    name = ""
    for scenario_name in scenario_dict.keys():
        name = name + "_" + str(scenario_name)

    fig.savefig(
        os.path.join(
            outputs_directory,
            "plot_scalars" + str(name) + "_" + str(variable_name) + ".png",
        )
    )


def compare_weather_years(
    latitude,
    longitude,
    country,
    static_inputs_directory=None,
    outputs_directory=None,
    user_inputs_mvs_directory=None,
):
    """
    Barplot that shows yearly aggregated weather parameters: ghi, dni, dhi and
    temperature.


    Parameters
    ----------
    latitude: float
        latitude of the location
    longitude: float
        longitude of the location
    country: str
        country of simulation
    static_inputs_directory: str
        if None: 'constants.DEFAULT_STATIC_INPUTS_DIRECTORY'
    outputs_directory: str
        if None: 'constants.DEFAULT_OUTPUTS_DIRECTORY
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    Returns
    -------
        None
        The plot is saved into the `output_directory`.
    -------

    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    timeseries_directory = os.path.join(user_inputs_mvs_directory, "time_series")
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY

    ghi = pd.DataFrame()
    temp = pd.DataFrame()
    dni = pd.DataFrame()
    dhi = pd.DataFrame()
    electricity_demand = pd.DataFrame()
    heat_demand = pd.DataFrame()

    for file in os.listdir(static_inputs_directory):
        if file.startswith("weatherdata_" + str(latitude) + "_" + str(longitude)):
            year = file.split(".")[2].split("_")[1]
            weatherdata = pd.read_csv(
                os.path.join(static_inputs_directory, file), header=0
            )
            ghi[year] = weatherdata["ghi"]
            temp[year] = weatherdata["temp_air"]
            dni[year] = weatherdata["dni"]
            dhi[year] = weatherdata["dhi"]

    for file in os.listdir(timeseries_directory):
        if file.startswith("electricity_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                electricity_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                electricity_demand[year] = electricity_load["kWh"]
        elif file.startswith("heat_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                heat_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                heat_demand[year] = heat_load["kWh"]

    ghi = ghi.reindex(sorted(ghi.columns), axis=1)
    temp = temp.reindex(sorted(temp.columns), axis=1)
    dni = dni.reindex(sorted(dni.columns), axis=1)
    dhi = dhi.reindex(sorted(dhi.columns), axis=1)
    electricity_demand = electricity_demand.reindex(
        sorted(electricity_demand.columns), axis=1
    )
    heat_demand = heat_demand.reindex(sorted(electricity_demand.columns), axis=1)

    ghi_sum = ghi.sum(axis=0)
    temp_sum = temp.sum(axis=0)
    dni_sum = dni.sum(axis=0)
    dhi_sum = dhi.sum(axis=0)
    el_sum = electricity_demand.sum(axis=0)
    he_sum = heat_demand.sum(axis=0)

    # data to plot
    n_groups = len(ghi.columns)

    # create plot
    fig = plt.figure(figsize=(11, 7))  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes
    bar_width = 0.15
    opacity = 0.8

    ax2 = ax.twinx()

    ghi_sum.plot(
        kind="bar",
        color="tab:orange",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="ghi",
        position=3,
    )
    dni_sum.plot(
        kind="bar",
        color="gold",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dni",
        position=2,
    )
    dhi_sum.plot(
        kind="bar",
        color="tab:green",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dhi",
        position=1,
    )
    el_sum.plot(
        kind="bar",
        color="tab:blue",
        ax=ax2,
        alpha=opacity,
        width=bar_width,
        label="electricity load",
        position=0,
    )
    #    he_sum.plot(kind='bar', color = "purple", ax=ax2, alpha = opacity,width=bar_width, label="heat load", position = 0)

    plt.xlabel("year")
    ax.set_ylabel("Irradiance in kW/year")
    ax2.set_ylabel("Demand in kWh/year")
    #    plt.title("yearly energy yield")
    #    plt.xticks(index + bar_width, (ghi.columns))
    ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.1)
    # Put a legend to the right of the current axis
    ax.legend(loc="lower right", bbox_to_anchor=(-0.05, 0))
    ax2.legend(loc="lower left", bbox_to_anchor=(1.05, 0))
    #    plt.tight_layout()

    # save plot into output directory
    plt.savefig(
        os.path.join(
            outputs_directory, f"plot_compare_weatherdata_{latitude}_{longitude}.png"
        ),
        bbox_inches="tight",
    )


def postprocessing_kpi(scenario_name, outputs_directory=None):
    """
    Overwrites all output excel sheets "timeseries_all_flows.xlsx" and "scalars.xlsx"
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
    list_var_name = []
    for fname in list(glob.glob(os.path.join(scenario_folder, "*"))):
        folder_name = fname.split("/")[::-1][0]
        if folder_name.startswith("loop"):
            split_path = folder_name.split("_")
            get_var_name = split_path[::-1][0]
            list_var_name.append(get_var_name)
    # loop over all loop output folders with variable name
    for variable_name in list_var_name:
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
            ) / file_sheet3.at["Total_demandElectricity", 0]

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


if __name__ == "__main__":
    latitude = 52.5243700
    longitude = 13.4105300
    years = [2011]  # a year between 2011-2013!!!
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

    # scenario_dict = {"Scenario_A2": "psi", "Scenario_A9": "psi_HP"}
    # plot_kpi_loop(
    #     scenario_dict=scenario_dict,
    #     variable_name="lifetime",
    #     kpi=[
    #         "Installed capacity PV",
    #         "Total emissions",
    #         "Degree of autonomy",
    #     ],
    # )
    #
    # compare_weather_years(
    #     latitude=latitude,
    #     longitude=longitude,
    #     country=country,
    #     static_inputs_directory=None,
    # )

postprocessing_kpi(scenario_name="Scenario_A9", outputs_directory=None)
