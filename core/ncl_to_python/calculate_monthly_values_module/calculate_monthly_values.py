import xarray as xr
import numpy as np


def calculate_monthly_values(x, arith, nDim, opt):
    '''Calculate monthly values [avg, sum, min, max, var, std] from given DataArray.
    
    
    Parameters
    ----------
    x(objectDataArray) : Array containing the high frequency data.

        The following DataArray structures are supported. The dimension name 'time' is a place-holder. Any name can be used. 
        The nDim argument specifies the dimension number to be used.

            (time)                     # nDim=0
            (time,npts)
            (time,ny,nx)
            (time,nz,ny,nx)
            (time,ne,nz,ny,nx)         # nDim=0
            (ne,time,nz,ny,nx)         # nDim=1
       
    arith(string) : A scalar string value which specifies the operation to be performed. 
            Valid values are: "avg", "sum", "min", "max", "var", "std". 
    
    nDim(int) : The dimension of x on which to calculate the statistic. Currently, only nDim=0 or 1 is allowed.
    
    opt(objectDataArray) : A logical DataArray to which various optional arguments may be assigned as attributes.
                           Must be set to True prior to setting the attributes. 
                           If opt=True, the attribute 'nval_crit' (integer) will specify the minimum number of values need to calculate the desired statistic.
                           If fewer values than 'nval_crit' are available, the result will be set to NaN. The default is 1 (one). 
    Returns
    -------
    objectDataArray : An array of the same rank as x. 

    '''
    
    # Get the rank of dataarray
    len_of_dim = x.sizes
    rank_of_x = len(len_of_dim)
    
    # Check if the rank of dim is valid or invalid; if invalid, exit the function
    if (rank_of_x > 5):
        print("calculate_monthly_values: rank = {} [only 5 dimensions or fewer supported]".format(rank_of_x))
        return None
    
    
    # Get the variable name for time dimension
    time = x.dims[nDim]
    
    # Check if the DataArray already has monthly values or not
    days = x.time.dt.day
    uniq = np.unique(days)
    if (len(uniq) == 1):
        print("Data already in monthly format, or invalid.")
        return None
    
    if (rank_of_x <= 4):
        no_of_time = len_of_dim[x.dims[0]]
    else:
        no_of_time = len_of_dim[x.dims[1]]
        
    
    # First Year, Last Year and the number of years present in the DataArray
    yr_strt = x.time.dt.year[0].item()
    yr_last = x.time.dt.year[-1].item()
    no_of_years = yr_last - yr_strt + 1
    
    # Number of months in a year
    no_of_months = 12
    
    # Calculate the number of days for each month
    
    # A days per month dictionary to support different calendar types
    dpm = {'noleap': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '365_day': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'standard': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'proleptic_gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'all_leap': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '366_day': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '360_day': [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]}
    
    # Check if the year is leap year or not
    def leap_year(year, calendar='standard'):
        """Determine if year is a leap year"""
        leap = False
        if ((calendar in ['standard', 'gregorian',
            'proleptic_gregorian', 'julian']) and
            (year % 4 == 0)):
            leap = True
            if ((calendar == 'proleptic_gregorian') and
                (year % 100 == 0) and
                (year % 400 != 0)):
                leap = False
            elif ((calendar in ['standard', 'gregorian']) and
                     (year % 100 == 0) and (year % 400 != 0) and
                     (year < 1583)):
                leap = False
        return leap
    
    
    # Days per month function
    def get_dpm(time, calendar='standard'):
        """
        return an array of days per month corresponding to the months provided in `months`

        """
        month_length = np.zeros(len(time), dtype=np.int)

        cal_days = dpm[calendar]

        for i, (month, year) in enumerate(zip(time.month, time.year)):
            month_length[i] = cal_days[month]
            if leap_year(year, calendar=calendar):
                month_length[i] += 1
        return month_length
    
    
    # Save the month length values in a DataArray
    month_length = xr.DataArray(get_dpm(x.time.to_index(), calendar='noleap'),
                            coords=[x.time], name='month_length')
    
    # Ref. The functions leap_year and get_dpm are provided in the xarray documentation
    # Copy the original DataArray
    x_new = x.copy(data = x, deep = True)
    
    # Load the new DataArray into memory (necessary for chunked data)
    x_new.load()
    
    # Check opt and get the nval_crit value
    if (opt == False):
        pass
    elif (opt.item() == True):
        nCritical = opt.attrs['nval_crit']
        
        # Set the nan index
        nan_index = np.array([])
        for i in range(0,len(month_length)):
            if (month_length[i].item() < nCritical):
                nan_index = np.append(nan_index,i)
        
        
        # Replace values with NaN for monthly_length < nCritical :: as per NCL function
        if (rank_of_x < 5):
            for ind in nan_index:
                nan_val = int(ind)
                x_new[nan_val] = None
        
        elif (rank_of_x == 5):
            for ind in nan_index:
                nan_val = int(ind)
                x_new[:,nan_val,:,:,:] = None
   
    # Perform the Arithmetic Computations
    
    if (arith == "avg"):
        xReturn = x_new.resample(time = '1M').mean(time, skipna = False)

    elif (arith == "sum"):
        xReturn = x_new.resample(time = '1M').sum(time, skipna = False)

    elif (arith == "min"):
        xReturn = x_new.resample(time = '1M').min(time, skipna = False)

    elif (arith == "max"):
        xReturn = x_new.resample(time = '1M').max(time, skipna = False)

    elif (arith == "var"):
        xReturn = x_new.resample(time = '1M').var(time, skipna = False, ddof = 1)

    elif (arith == "std"):
        xReturn = x_new.resample(time = '1M').std(time, skipna = False, ddof = 1)

    else:
        print("Unsupported arithmetic {}".format(arith))
        return None
    
    # Add and copy the attributes and properties from original DataArray
    xReturn = xReturn.rename("xMon")
    xReturn.attrs = x.attrs
    xReturn.encoding = x.encoding

    xReturn.attrs["time"] = nDim
    xReturn.attrs["NCL_tag"] = "calculate_monthly_values: arith=" + arith
    
    
    return xReturn
