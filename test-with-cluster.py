import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import time
from arraylake import Client as alClient
from dask.distributed import Client as dClient
from dask_cloudprovider.aws import EC2Cluster

print("--------------")
print("Opening a link to the Earthmover ERA5 data and authenticating")
alclient = alClient()
alclient.login()

repo = alclient.get_repo("earthmover-public/era5")
session = repo.readonly_session("main")

interval = slice("2024-01","2024-03")

cluster = EC2Cluster()
cluster.scale(4)

dclient = dClient(cluster)
dclient

print("Starting our data test: spatial")
start_time = time.perf_counter()

ds_spatial = xr.open_zarr(session.store, group="single/spatial", chunks={})

msl_spatial = ds_spatial.msl.sel(valid_time=interval).mean(dim="valid_time").load()

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Data execution time: {execution_time:.6f} seconds")
print("--------------")
print("Starting next data test: temporal")
start_time = time.perf_counter()

ds_temporal = xr.open_zarr(session.store, group="single/temporal", chunks={})

msl_temporal = ds_temporal.msl.sel(valid_time=interval).mean(dim="valid_time").load()

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Data execution time: {execution_time:.6f} seconds")
print("--------------")
rtol = 1e-5
np.testing.assert_allclose(msl_spatial, msl_temporal, rtol=rtol)
print("Datasets match to within {} percent.".format(rtol*100))
print("--------------")

cluster.close()
