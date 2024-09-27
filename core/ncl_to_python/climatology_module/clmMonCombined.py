# Import libraries

import xarray as xr


def clmMonCombined(n,x):
    """Calculates long term monthly means (monthly climatology) from monthly data.

    Parameters
    ----------
    n : (Integer) The index of time dimension in DataArray.

    x : A three/four dimensional DataArray. The time dimension must be a multiple of 12.

    Returns
    -------
    objectDataArray :  A DataArray of the same size and type as x except that the time dimension will be of size 12.

    """
    
    # Calculate the sizes of rank of dimensions
    len_of_dim = x.sizes
    rank = len(len_of_dim)
    
    # Check if rank of dimension is valid or not
    if (rank < 3 or rank > 4):
        print("Current rank not supported")
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    time_size = len_of_dim[x.dims[n]]
    no_of_months = 12
    if ((time_size % no_of_months) != 0):
        print("clmMonTLL: dimension must be a multiple of 12")
        return None
            
    time = x.dims[n]
    
    # Store as a string for groupby operation
    time_month = time + '.month'

    # Compute 12 months average
    ave_month = x.groupby(time_month).mean(time, skipna = True)

    # Copy and update the attributes
    ave_month.attrs = x.attrs
    ave_month = ave_month.rename("aveMonth")
    ave_month.attrs['time_op_ncl'] = "Climatology: " + str(int(time_size/no_of_months)) + " years"
    ave_month.attrs['info'] = "function clmMonCombined"

    # Copy the encoding from original DataArray
    ave_month.encoding = x.encoding
    
    # Return the results
    return ave_month
