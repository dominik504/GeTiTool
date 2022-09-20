import argparse
import matplotlib.pyplot as plt
import datetime

from . import AnalyzeEdit
from . import AnalyzePlot

def analyze():
    
    # handling argparse input
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str,
                        help="directory where .csv files of paraview output are located")
    parser.add_argument("-m", "--min-max", dest="min_max",
                        type=int, nargs=2, default=[0, 99999],
                        help="minimum and maximum ID bounds results should be plotted")
    parser.add_argument("-p", "--parameter", type=str,
                        help="Give the parameter which should be plotted")
    parser.add_argument("-a", "--use-area", dest="area", action="store_true",
                        help="Use this flag to average the integrated results over the area")
    parser.add_argument("-i", "--index-file", dest="index_file", type=str,
                        help="Use this to include a datetime information and give the path to the .csv index file")
    parser.add_argument("-s", "--save", action="store_true",
                        help="Use this flag if you want to save the resulting figure within your directory")
    args=parser.parse_args()
    # save argparse arguments into variables
    path = args.directory
    min_index = args.min_max[0]
    max_index = args.min_max[1]
    parameter = args.parameter
    index_file = args.index_file
    area = args.area
    save = args.save
    
    # parsing min and max ID or Datetime and check for errors
    try: # if min and max were parsed as ID
        min_index = int(args.min_max[0])
        max_index = int(args.min_max[1])
    except ValueError:
        try: # if min and max were parsed as date without time
            datetime.datetime.strptime(args.min_max[0], '%Y-%m-%d')
            datetime.datetime.strptime(args.min_max[1], '%Y-%m-%d')
            min_index = args.min_max[0]
            max_index = args.min_max[1]
        except ValueError:
            try: # if min and max were parsed as date with time
                datetime.datetime.strptime(args.min_max[0], '%Y-%m-%d %H:%M')
                datetime.datetime.strptime(args.min_max[1], '%Y-%m-%d %H:%M')
                min_index = args.min_max[0]
                max_index = args.min_max[1]
            except ValueError:
                raise ValueError("Incorrect data format, should be Year-month-day or Year-month-day Hour:Minute")
    
    if  index_file != None:
        index = True 
    else:
        index = False
               
    if index:
        result = AnalyzeEdit.add_index(path=path, parameter=parameter, index_file=index_file)
        max_index = str(max_index)
        min_index = str(min_index)
    else:
        result = AnalyzeEdit.read_result(path=path, parameter=parameter)

    
    
    AnalyzePlot.plot_results(result=result, min_index=min_index,
                 max_index=max_index, parameter=parameter, area=area)
    plt.subplots_adjust(left=0.053, bottom=0.196, right=0.97, top=0.965)
    
    if save:
        print("Your resulting figure is saved at:")
        print(f"{path}/Figure_2.png")
        plt.savefig(f"{path}/Result_GeTiTool.png")
    
    plt.show()
    

    
    
    print("\n")
    print("######   #   #   #   #   #####   #    #   ######   ###")
    print("#        #   ##  #   #   #       #    #   #        #  #")
    print("###      #   # # #   #   #####   ######   ###      #   #")
    print("#        #   #  ##   #       #   #    #   #        #  #")
    print("#        #   #   #   #   #####   #    #   ######   ###")