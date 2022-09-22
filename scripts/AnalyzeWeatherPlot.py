def plot_results_weather(result_weather, min_index, max_index, parameter_ert, area, parameter_weather):
    """
    Simple plot of the results using the parameter from user input and showing
    results within the given index range.

    Parameters
    ----------
    result_weather : Dataframe
        Pandas Dataframe including a column with the name given from user as
        'parameter' with the corresponding results.
    min_index : String
        BETA - should work with datetime in future as well
        Give the ID for the first step.
    max_index : String
        BETA - should work with datetime in future as well
        Give the ID for the first step.
    parameter_ert : String
        Give the ert parameter that should be shown in the plot.
    area : Boolean
        If true the averaged value over the area will be used. If false the 
        integrated value over the whole area will be used.
    parameter_weather : String
        Give the weather parameter that should be shown in the plot.
    """
    
    # set label for plotting ert plot to not be overwritten in next step
    label_ert = parameter_ert
    
    # set area to be plotted if set by user
    if area:
        label_ert = f"{parameter_ert} per Area"
        parameter_ert = "parameter_area"
        
   
    ax = result_weather[f"{parameter_ert}"][(result_weather.index > min_index)&(
        result_weather.index < max_index)].plot(
            xlabel="Date",ylabel=f"{label_ert}",color="r", label=f"{label_ert}")
    ax1=ax.twinx()
    result_weather[f"{parameter_weather}"][(result_weather.index > min_index)&(
        result_weather.index < max_index)].plot(
            ax=ax1, color="b", ylabel=f"{parameter_weather}", label = f"{parameter_weather}",
            title=f"Integrated geoelectrical timelapse and weather results\nERT: {label_ert}; Weather: {parameter_weather}")
    
    # handle labels for legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax1.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc=0)
    
    ax1.grid()
                                                
    