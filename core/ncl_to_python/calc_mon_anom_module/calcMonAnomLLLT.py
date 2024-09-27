#Import libraries

import xarray as xr


def calcMonAnomLLLT(x, xAve):
    """Calculates monthly anomalies by subtracting the long term mean from each point (lev,lat,lon,time version)

    Parameters
    ----------
    x : A four-dimensional DataArray of any numeric type. Dimensions must be lev,lat, lon, time. The time dimension must be a multiple of 12.

    xAve : A four-dimensional DataArray equal to the monthly averages of x. The leftmost three dimensions are lev,lat,lon, while the rightmost must be of size 12.

    Returns
    -------
    objectDataArray : A DataArray of the same size and type as x.

    """
    # x is the dataarray and xAve is the monthly averages array of x
    
    len_of_dim = x.sizes
    no_of_time = len_of_dim[x.dims[3]] # no_of_time = Size of time dimension
    rank = len(len_of_dim)
    
    # Check if rank of dataarray matches the function
    if (rank != 4):
        print("Expected variable of rank = 4, recieved rank = {}".format(rank))
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    if ((no_of_time % no_of_months) != 0):
        print("month_to_season12: dimension must be a multiple of 12")
        return None
    
    # Store the time dimension name present in dataset as time variable
    time = x.dims[3]
    
    # Store as a string for groupby operation
    time_month = time + '.month'
    
    
    # Calculate anomalies by subtracting monthly means from actual dataarray
    xAnom = x.groupby(time_month) - xAve
        
    # Copy and update the attributes
    xAnom.attrs = x.attrs
    xAnom.attrs['anomaly_op_ncl'] = "Anomalies from Annual Cycle: calcMonAnomLLLT"
    
    # Drop the extra month co-ordinate from xAnom DataArray
    xAnom = xAnom.drop('month')
    xAnom = xAnom.rename("xAnom")

    # Copy the encoding from the original DataArray
    xAnom.encoding = x.encoding
    
    # Return the new dataarray
    return xAnom
