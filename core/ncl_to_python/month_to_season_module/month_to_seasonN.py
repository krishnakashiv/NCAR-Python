# import necessary libraries
import numpy as np
import pandas as pd
import xarray as xr


def month_to_season12(xMon):
    
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
        
        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for rank = 3
    if (rank_of_dim == 3):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:] = (xMon[0,:,:] + xMon[1,:,:]) * 0.5
        dr[(no_of_time-1),:,:] = (xMon[(no_of_time-2),:,:] + xMon[(no_of_time-1),:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for rank = 4
    if (rank_of_dim == 4):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:,:] = (xMon[0,:,:,:] + xMon[1,:,:,:]) * 0.5
        dr[(no_of_time-1),:,:,:] = (xMon[(no_of_time-2),:,:,:] + xMon[(no_of_time-1),:,:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        # Return the newly created DataArray
        return xSea


def month_to_seasonN(xMon, *SEASON):
    """Computes a user-specified list of three-month seasonal means (DJF, JFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDJ).

    
    Parameters
    ----------
    xMon : A one-, three-, or four-dimensional DataArray [xMon(time) or xMon(time,lat,lon) or xMon(time,lev,lat,lon)]
           of any numeric type. xMon must have named dimensions and the time (leftmost) dimension must be divisible by 12.
           The data are assumed to be monthly mean data and the first record is assumed to be January.
    
    *SEASON : An array of strings representing the seasons to calculate: e.g., "DJF","JJA".


    Returns
    -------
    objectDataArray : The return value will be of the same type and one more dimension than xMon. The leftmost dimension
                      will be N where N is the length of season. See the description below for more information.

                      If the input data contains metadata (e.g., coordinate variables and attributes), these will be retained.

                      In addition, the attributes "long_name" and "season" are returned.

    """
    
    
    
    # xMon is the DataArray and *SEASON are the seasons passed as an argument
    
    # Create a new array of seasons
    season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])
    N = len(SEASON)
    
    # Check if the SEASON argument is present in season array
    for i in SEASON:
        if i not in season:
            print("month_to_seasonN: You have atleast one spelling error " + 
                  "in your SEASON specification. {} is not valid.".format(i))
            return None
    
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
    no_of_years = no_of_time/no_of_months
    
    # Call the month_to_season12 function
    xSea12 = month_to_season12(xMon)
        
    
    # Store the size of latitude and longitude
    if (rank_of_dim >= 3):
        size_of_lat = len_of_dim[xMon.dims[rank_of_dim-2]]
        size_of_lon = len_of_dim[xMon.dims[rank_of_dim-1]]
    
    # Check the index of first SEASON passed in season array
    i = SEASON[0]
    NMO1 = np.where(season==i)[0].item()
    
    xSeaN = xSea12.copy()
    
    # Store the SEASONS in a numpy array
    sea = np.array([], dtype ='int')
    sea_code = np.array([], dtype = 'str')
    
    for n in range(0, N):
        NMO = np.where(season==SEASON[n])[0].item()
        sea = np.append(sea, NMO)
        sea_code = np.append(sea_code, season[NMO])
        
    # Create a new dataarray to store season co-ordinate data
    new_da = xr.DataArray(data = sea,dims = 'season', name='season')
    
    # Calculations for rank = 1
    if (rank_of_dim == 1):
        for ns in range(0,N):
            NMO = np.where(season==SEASON[ns])[0].item()
            if(NMO == sea[0]):
                xSeaN = xSea12[NMO:no_of_time:no_of_months]
            else:
                xS = xSea12[NMO:no_of_time:no_of_months]
                # Concat the data and pass the season co-ordinate
                xSeaN = xr.concat([xSeaN, xS])
    
    # Calculating seasonal mean for rank = 3
    if (rank_of_dim == 3):
        for ns in range(0,N):
            NMO = np.where(season==SEASON[ns])[0].item()
            if (NMO == sea[0]):
                xSeaN = xSea12[NMO:no_of_time:no_of_months,:,:]
            else:
                xS = xSea12[NMO:no_of_time:no_of_months,:,:]
                xSeaN = xr.concat([xSeaN, xS])
            
    
    # Calculating seasonal mean for rank = 4
    if (rank_of_dim == 4):
        for ns in range(0,N):
            NMO = np.where(season==SEASON[ns])[0].item()
            if (NMO == sea[0]):
                xSeaN = xSea12[NMO:no_of_time:no_of_months,:,:,:]
            else:
                xS = xSea12[NMO:no_of_time:no_of_months,:,:,:]
                xSeaN = xr.concat([xSeaN, xS])
    
    
    # Add and update the attributes
    if(xSeaN.attrs['long_name'] or xSeaN.attrs['description'] or xSeaN.attrs['standard_name']):
        xSeaN.attrs['long_name'] = "Seasonal Means: " + xSeaN.attrs['long_name']
        
        # Since the season co-ordinate contains indexes of data, we replace 
        # with the actual season string.
        xSeaN = xSeaN.rename({'concat_dims':'season'})
        xSeaN['season'] = sea_code
        xSeaN=xSeaN.rename("xSeaN")
        xSeaN.encoding=xMon.encoding
        # Remove null values from the dataset
        #xSeaN = xSeaN.resample(time = 'AS').mean('time')
            
        # Return the newly created DataArray
        return xSeaN
