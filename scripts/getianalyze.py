import argparse
import matplotlib.pyplot as plt
import datetime
import sys

from . import AnalyzeEdit, AnalyzePlot, AnalyzeWeather, AnalyzeWeatherPlot

def analyze():
    ## ------------ ARGPARSE HANDLING ------------ ## 
    # handling argparse input
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str,
                        help="directory where .csv files of paraview output are located")
    parser.add_argument("-m", "--min-max", dest="min_max",
                        type=str, nargs=2,
                        help="minimum and maximum ID bounds results should be plotted")
    parser.add_argument("-p", "--parameter", type=str,
                        help="Give the parameter which should be plotted")
    parser.add_argument("-a", "--use-area", dest="area", action="store_true",
                        help="Use this flag to average the integrated results over the area")
    parser.add_argument("-i", "--index-file", dest="index_file", type=str,
                        help="Use this to include a datetime information and give the path to the .csv index file")
    parser.add_argument("-s", "--save", action="store_true",
                        help="Use this flag if you want to save the resulting figure within your directory")
    parser.add_argument("-w", "--weatherstations", nargs=2, type=str,
                        help="directory where the csv files for the weatherstations are located, the first one must be the mobile one!")
    parser.add_argument("-wp", "--weather-parameter", dest="weather_parameter",
                        type=str, default="prec_mm", 
                        help="The weather parameter to be plotted")
    args=parser.parse_args()

    ## ------------ PARAMETER HANDLING ------------ ## 
    # save argparse arguments into variables
    path = args.directory
    parameter = args.parameter
    index_file = args.index_file
    area = args.area
    save = args.save
    mobile_weatherstation = args.weatherstations[0]
    official_weatherstation = args.weatherstations[1]
    parameter_weather = args.weather_parameter
    
    ## ------------ ERROR HANDLING ------------ ## 
    # parsing  Datetime, check for errors and save into variables
    if args.min_max:
        try: # if min and max were parsed as date without time
            datetime.datetime.strptime(args.min_max[0], '%Y-%m-%d')
            datetime.datetime.strptime(args.min_max[1], '%Y-%m-%d')
            min_index = str(args.min_max[0])
            max_index = str(args.min_max[1])
        except ValueError:
            try: # if min and max were parsed as date with time
                datetime.datetime.strptime(args.min_max[0], '%Y-%m-%d %H:%M')
                datetime.datetime.strptime(args.min_max[1], '%Y-%m-%d %H:%M')
                min_index = str(args.min_max[0])
                max_index = str(args.min_max[1])
            except ValueError:
                parser.error("Incorrect data format, should be Year-month-day or Year-month-day Hour:Minute")
                sys.exit()
    else:
        if index_file:
            min_index = "1899-01-01"
            max_index = "2099-01-01"
        else:
            min_index = 0
            max_index = 9999999999999
    
    # check if min and max datetime are in correct order
    if min_index > max_index:
        print("Your Minimum Date is higher than your Maximum Date, should I change this?")
        answer = input("yes/no: ")
        if answer.lower()[0] == "y":
            min_index, max_index = max_index, min_index
        else:
            parser.error("Minimun and Maximum Date in wrong order")
    
    # error if weatherstation is given but no index for ERT Data
    if (not index_file) & (not not mobile_weatherstation):
        print("No ERT Index File given, should I continue without Index and Weatherstation?")
        answer = input("Yes/ No: ")
        if answer.lower()[0] == "y":
            mobile_weatherstation = official_weatherstation = None
        else:
            parser.error("No Index for ERT given, cant combine it with weatherstation.")
    
    ## ------------ CALCULATION ------------ ##           
    if index_file:
        result = AnalyzeEdit.add_index(path=path, parameter=parameter, index_file=index_file)
        if mobile_weatherstation:
            result_weather = AnalyzeWeather.WeatherData(mobile_weatherstation=mobile_weatherstation,
                                            official_weatherstation=official_weatherstation,
                                            ert_time=result)
    else:
        result = AnalyzeEdit.read_result(path=path, parameter=parameter)


    ## ------------ PLOTTING ------------ ##
    # Only ERT Plot
    if not mobile_weatherstation:
        AnalyzePlot.plot_results(result=result,
                                 min_index=min_index,
                                 max_index=max_index,
                                 parameter=parameter,
                                 area=area)

    # ERT and Weather Plot
    if mobile_weatherstation:
        AnalyzeWeatherPlot.plot_results_weather(result_weather=result_weather, 
                                                min_index=min_index, 
                                                max_index=max_index, 
                                                parameter_ert=parameter, 
                                                area=area, 
                                                parameter_weather=parameter_weather)
    
    ## ------------ SAVE/SHOW RESULTS ------------ ##
    plt.tight_layout()
    if save:
        print("Your resulting figure is saved at:")
        print(f"{path}/Result_GeTiTool_weather.png")
        plt.savefig(f"{path}/Result_GeTiTool_weather.png", dpi=200)
    else:
        plt.show()

    print("  ######   #   #   #   #   #####   #    #   ######   ###")
    print("  #        #   ##  #   #   #       #    #   #        #  #")
    print("  ###      #   # # #   #   #####   ######   ###      #   #")
    print("  #        #   #  ##   #       #   #    #   #        #  #")
    print("  #        #   #   #   #   #####   #    #   ######   ###")