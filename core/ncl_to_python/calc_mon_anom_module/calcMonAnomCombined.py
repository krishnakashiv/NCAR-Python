# Import libraries

import xarray as xr


def calcMonAnomCombined(n, x, xAve):
    """Calculates monthly anomalies by subtracting the long term mean from each point (combined version).

    Parameters
    ----------
    n : (Integer) The index of time dimension in DataArray

    x : A three/four dimensional DataArray. The time dimension must be a multiple of 12.

    xAve : A three/four dimensional DataArray equal to the monthly averages of x.

    Returns
    -------
    objectDataArray : A DataArray of the same size and type as x.

    """
    # x is the dataarray and xAve is the monthly averages array of x
    
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

    # Store the time dimension name present in dataset as time variable
    time = x.dims[n]

    # Store as a string for groupby operation
    time_month = time + '.month'

    # Calculate anomalies by subtracting monthly means from actual dataarray
    xAnom = x.groupby(time_month) - xAve

    # Copy and update the attributes
    xAnom.attrs = x.attrs
    xAnom.attrs['anomaly_op_ncl'] = "Anomalies from Annual Cycle: calcMonAnomCombined"
    

    # Drop the extra month co-ordinate from xAnom DataArray
    xAnom = xAnom.drop('month')
    xAnom = xAnom.rename("xAnom")

    # Copy the encoding from the original DataArray
    xAnom.encoding = x.encoding


    # Return the new dataarray
    return xAnom
