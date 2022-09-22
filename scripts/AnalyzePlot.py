def plot_results(result, min_index, max_index, parameter, area):
    """
    Simple plot of the results using the parameter from user input and showing
    results within the given index range.

    Parameters
    ----------
    result : Dataframe
        Pandas Dataframe including a column with the name given from user as
        'parameter' with the corresponding results.
    min_index : String
        BETA - should work with datetime in future as well
        Give the ID for the first step.
    max_index : String
        BETA - should work with datetime in future as well
        Give the ID for the first step.
    parameter : String
        Give the parameter that should be shown in the plot.
    area : Boolean
        If true the averaged value over the area will be used. If false the 
        integrated value over the whole area will be used.
    """
    
    # set label for plotting
    label = parameter
    # set area to be plotted if set by user
    if area:
        label = f"{parameter} per Area"
        parameter = "parameter_area"
        
    # plot results
    result[(result.index > min_index)&(
        result.index < max_index)][f"{parameter}"].plot(
            rot=45,xlabel="Date", ylabel=f"{label}",
            title="Integrated geoelectrical timelapse results") 