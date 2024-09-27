# Import Libraries
import sys
sys.path.insert(1, '../..')


import xarray as xr
from dask.distributed import Client
from dask_jobqueue import PBSCluster
from ncl_to_python.calculate_monthly_values_module import *
from dask import compute
import dask
import distributed
import time


cluster = PBSCluster(queue='research',
                     project='DaskOnPBS',
                     local_directory='/lus/dal/hpcs_rnd/Python_Data_Analysis/Jatin/ncl_to_python_v3/Parallel_Function_Testing/calc_monthly_values/DASK_OUT/',
                     cores=1,
                     processes=1,
                     memory='40GB',
                     walltime='24:00:00',
                     resource_spec='select=1:ncpus=36:mem=40GB:vntype=cray_compute',
                     env_extra=['aprun -n 1'])


j = sys.argv[1]
# Scale clusters to add j workers (j = number of jobs)
cluster.scale(j)


client = Client(cluster)


# Enter the path to the dataset
path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
print("PATH is {}".format(path1))
ds = xr.open_mfdataset(path1, chunks = {'lat':96, 'lon':144}, parallel = True)

var = ds["FLNS"]


# Change data=False in opt to data=True to use it
opt = xr.DataArray(data=False)
opt.attrs["nval_crit"] = 30

strt = time.time()
result = calculate_monthly_values(var, "max", 0, opt).compute()
end = time.time()



# Shutdown the client, workers and jobs running
client.shutdown()


print(result)
print("Time taken by the function: {} seconds".format(end-strt))



