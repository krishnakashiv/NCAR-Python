# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# import necessary libraries
import numpy as np
import pandas as pd
import xarray as xr


def month_to_season12(xMon):
    """Computes three-month seasonal means (DJF, JFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDJ).
    
    Parameters
    ----------
    xMon : A one-, three-, or four-dimensional DataArray [xMon(time) or xMon(time,lat,lon) or xMon(time,lev,lat,lon)]
           of any numeric type. xMon must have named dimensions and the time (leftmost) dimension must be divisible by 12.
           The data are assumed to be monthly mean data and the first record is assumed to be January.

    Returns
    -------
    objectDataArray : The return value will be of the same type and dimensionality as xMon. If the input data contains metadata 
                      (e.g., coordinate variables and attributes), these will be retained.

                      In addition, the attribute "season" is returned.

    """
    
    # xMon is the DataArray passed as an argument
    
    # Create a new array of seasons
    season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])
    
    # Get the rank of dataarray
    len_of_dim = xMon.sizes
    rank_of_dim = len(len_of_dim)
    
    # Check if the rank of dim is valid or invalid; if invalid, exit the function
    if (rank_of_dim == 2 or rank_of_dim >= 5):
        print("month_to_season12: rank = {}".format(rank_of_dim))
        print("----- rank currently not handled -----")
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    no_of_time = len_of_dim[xMon.dims[0]]
    if ((no_of_time % no_of_months) != 0):
        print("month_to_season12: dimension must be a multiple of 12")
        return None
    
    
    # Check if dimensions are named or not; if unnamed, exit the function
    for i in range(0, rank_of_dim):
        if xMon.dims[i] == None or xMon.dims[i] == "":
            print("mon_to_season12: All dimensions must be named")
            print("\t\tdimension {} is missing".format(i))
            return None
    
    # Calculating seasonal mean for rank = 1
    if (rank_of_dim == 1):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0] = (xMon[0] + xMon[1]) * 0.5
        dr[(no_of_time-1)] = (xMon[(no_of_time-2)] + xMon[(no_of_time-1)]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        
        xSea.encoding = xMon.encoding
        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for number of dimensions = 3
    if (num_of_dim == 3):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:].values = (xMon[0,:,:] + xMon[1,:,:]) * 0.5
        dr[(no_of_time-1),:,:].values = (xMon[(no_of_time-2),:,:] + xMon[(no_of_time-1),:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        xSea.encoding = xMon.encoding

        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for rank = 4
    if (rank_of_dim == 4):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:,:].values = (xMon[0,:,:,:] + xMon[1,:,:,:]) * 0.5
        dr[(no_of_time-1),:,:,:].values = (xMon[(no_of_time-2),:,:,:] + xMon[(no_of_time-1),:,:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        xSea.encoding = xMon.encoding

        # Return the newly created DataArray
        return xSea


