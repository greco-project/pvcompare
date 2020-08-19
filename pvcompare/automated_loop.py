from pvcompare import check_inputs
import main
import constants
import os
import pandas as pd
import glob
import shutil
import matplotlib.pyplot as plt

def loop(latitude,
        longitude,
        year,
        population,
        country,
        variable_name,
        variable_column,
        csv_file_variable,
        start,
        stop,
        step,
        input_directory=None,
        mvs_input_directory=None,
        loop_output_directory=None,
        mvs_output_directory=None):

    """

    Parameters
    ----------
    latitude
    longitude
    year
    population
    country
    variable
    csv_file_variable
    start,
    stop,
    step

    Returns
    -------

    """


    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    if mvs_output_directory == None:
        mvs_output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY
    if loop_output_directory == None:
        loop_output_directory = constants.DEFAULT_LOOP_OUTPUT_DIRECTORY

    if os.path.isdir(loop_output_directory):
        shutil.rmtree(loop_output_directory)
        os.mkdir(loop_output_directory)
    else:
        try:
            os.mkdir(loop_output_directory)
        except OSError:
            print("Creation of the directory %s failed" % loop_output_directory)

        # create output folder in loop_output_directories for "sequences" and "timeseries"

    os.mkdir(os.path.join(loop_output_directory, "scalars"))
    os.mkdir(os.path.join(loop_output_directory, "timeseries"))

    csv_filename = os.path.join(mvs_input_directory, "csv_elements", csv_file_variable)
    csv_file = pd.read_csv(csv_filename, index_col=0)

    main.main(
        latitude=latitude,
        longitude=longitude,
        year=year,
        population=population,
        country=country
    )

    i = start
    while i <= stop:
        csv_file.loc[
            [variable_name], [variable_column]] = i
        #save csv
        csv_file.to_csv(csv_filename)

        main.apply_mvs(mvs_input_directory,
        mvs_output_directory)


        #copy excel sheets to loop_output_directory
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

        excel_file1="scalars.xlsx"
        new_excel_file1="scalars_" + str(j) +".xlsx"
        src_dir = os.path.join(mvs_output_directory, excel_file1)
        dst_dir = os.path.join(loop_output_directory, "scalars", new_excel_file1)
        shutil.copy(src_dir, dst_dir)

        excel_file2 = "timeseries_all_busses.xlsx"
        new_excel_file2 = "timeseries_all_busses_" + str(j) + ".xlsx"
        src_dir = os.path.join(mvs_output_directory,excel_file2)
        dst_dir = os.path.join(loop_output_directory, "timeseries", new_excel_file2)
        shutil.copy(src_dir, dst_dir)

        i = i + step

    # copy energyProduction.csv into loop_output_directory
    src_dir = os.path.join(mvs_input_directory, "csv_elements", "energyProduction.csv")
    dst_dir = os.path.join(loop_output_directory, "energyProduction.csv")
    shutil.copy(src_dir, dst_dir)




def plot_total_costs_from_scalars(variable, stop, loop_output_directory=None):

    if loop_output_directory == None:
        loop_output_directory = constants.DEFAULT_LOOP_OUTPUT_DIRECTORY
    energyProduction=pd.read_csv(os.path.join(loop_output_directory, "energyProduction.csv"), index_col=0)
    energyProduction = energyProduction.drop(["unit"], axis=1)
    pv_labels = energyProduction.loc["label"].values

    digits_index=len(str(stop))
    total_costs = pd.DataFrame()
    for filepath in list(glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))):
        file=pd.read_excel(filepath, header=0, index_col=1)
        i = filepath.split('.')[0][-digits_index:]
        for pv in pv_labels:
            total_costs.loc[int(i), pv] = file.at[pv, "costs_total"]

    plt.title(variable)
    plt.plot(total_costs, "o-")
    plt.legend()
    plt.savefig(os.path.join(loop_output_directory, 'plot_total_costs_' + str(variable) + ".png"))
    plt.show()






if __name__ == "__main__":
    latitude = 45.641603
    longitude = 5.875387
    year = 2014  # a year between 2011-2013!!!
    population = 48000
    country = "Spain"

    loop(latitude=latitude,
         longitude=longitude,
         year=year,
         population=population,
         country=country,
         variable_name="development_costs",
         variable_column= "pv_plant_03",
         csv_file_variable = "energyProduction.csv",
         start=600,
         stop=1400,
         step=200)

    plot_total_costs_from_scalars(variable="lifetime", stop=15, loop_output_directory=None)



    print(loop)