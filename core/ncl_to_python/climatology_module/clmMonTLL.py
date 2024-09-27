# import libraries

import xarray as xr

def clmMonTLL(x):
    """Calculates long term monthly means (monthly climatology) from monthly data: (time,lat,lon) version.

    Parameters
    ----------
    x : A three dimensional DataArray. Dimensions must be time, lat, lon. The time dimension must be a multiple of 12. The dimensions must be named.

    Returns
    -------
    objectDataArray : A DataArray of the same size and type as x except that the leftmost dimension will be of size 12.

    """
    
    # Calculate the sizes of time dimension
    len_of_dim = x.sizes
    time_size = len_of_dim[x.dims[0]]
    rank = len(len_of_dim)

    # Check if rank of dataarray matches the function
    if (rank != 3):
        print("Expected variable of rank = 3, recieved rank = {}".format(rank))
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    if ((time_size % no_of_months) != 0):
        print("clmMonTLL: dimension must be a multiple of 12")
        return None
    
    # Store the time dimension name present in dataset as time variable
    time = x.dims[0]
    
    # Store as a string for groupby operation
    time_month = time + '.month'
    
    # Compute 12 months average
    ave_month = x.groupby(time_month).mean(time, skipna = True)
    
    # Copy and update the attributes
    ave_month.attrs = x.attrs
    ave_month = ave_month.rename("aveMonth")
    ave_month.attrs['time_op_ncl'] = "Climatology: " + str(int(time_size/no_of_months)) + " years"
    ave_month.attrs['info'] = "function clmMonTLL"

    # Copy the encoding from original DataArray
    ave_month.encoding = x.encoding
    
    # Return the results
    return ave_month

