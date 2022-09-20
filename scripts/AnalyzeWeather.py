import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import os
# import glob

# ignore warning of setting a copy within for loop
pd.options.mode.chained_assignment = None  # default='warn'

# mobile_weatherstation = "20220713.csv"
# official_weatherstation = "Semriach_Messstation_raw.csv"

def WeatherData(mobile_weatherstation, official_weatherstation, ert_time):
    """
    Function to read data from weatherstations and combine then in a new dataframe

    Parameters
    ----------
    mobile_weatherstation : String
        Path to the csv file including the data of the mobile weatherstation.
    official_weatherstation : String
        Path to the csv file including the data of the fix weatherstation.
    ert_time : Dataframe
        Pandas Dataframe including ert Results with a hourly temporal resolution
        same as weatherstations have.

    Returns
    -------
    df_manipulated : Dataframe
        Pandas Dataframe with Hourly Weatherdata of the official and mobile 
        weatherstation. Outliers of the mobile weatherstation were deleted.
        

    """
    # read data of weather station
    df = pd.read_csv(mobile_weatherstation, delimiter=",", header=0)
    df['Time'] = pd.to_datetime(df['Time'], format='%d.%m.%Y %H:%M:%S')
    df.Time = df.Time.dt.floor("Min")
    df = df.set_index("Time", inplace=False)
    
    df.columns = ["Number", "winddirection_min", "winddirection_avg",
                  "winddirection_max", "windspeed_min", "windspeed_avg",
                  "windspeed_max", "Temperature_Celsius", "Humidity",
                  "Pressure_hPa", "mm_Pre", "s_Dura", "Precipitation_mm",
                  "Batteryload", "HK_Temp", "HK-rH%"]
    
    # join semriach weatherstation info
    #!!! Lücke muss vorher mit Empty getauscht werden --> im Editor
    weatherstation = pd.read_csv(official_weatherstation, index_col=0, delimiter=";", header=25, 
                           skipinitialspace=True, parse_dates=True)
    weatherstation = weatherstation.replace("Empty", np.nan)
    weatherstation = weatherstation.rename(columns={"Werte:": "value"})
    weatherstation.value = weatherstation.value.str.replace(",", ".").astype(float)
    weatherstation.index.names = ["Date"]
    df["official_weatherstation"] = weatherstation.value
    
    #!!! manipulation
    max_value = 30
    df["rain_manipulated"] = np.where(df.Precipitation_mm > max_value, 0, df.Precipitation_mm)
    
    # add values to new df in one hour temporal resolution
    df_manipulated = pd.DataFrame(index = df.Temperature_Celsius.resample("H").mean().index)
    df_manipulated["prec_mm"] = df.rain_manipulated.resample("H").sum() / 6
    df_manipulated["windspeed_avg"] = df.windspeed_avg.resample("H").mean()
    df_manipulated["temperature_telsius"] = df.Temperature_Celsius.resample("H").mean()
    df_manipulated["humidity"] = df.Humidity.resample("H").mean()
    df_manipulated["pressure_hPa"] = df.Pressure_hPa.resample("H").mean()
    df_manipulated["prec_official"] = df.official_weatherstation.resample("H").sum()
    df_manipulated["prec_diff"] = df_manipulated.prec_mm - df_manipulated.prec_official
    df_manipulated["prec_raw"] = df.Precipitation_mm.resample("H").sum() / 6
    
    ert_weather = pd.concat([ert_time, df_manipulated], axis = 1)
    return ert_weather