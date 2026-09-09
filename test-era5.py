"""
This script fetches some data from the Earthmover Arraylake ERA5 store and does some simple performance benchmarking.

The data access requires authentication with a (free) Earthmover account.
"""
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import time

from arraylake import Client

print("--------------")
print("Opening a link to the Earthmover ERA5 data and authenticating")
client = Client()
client.login()

repo = client.get_repo("earthmover-public/era5")
session = repo.readonly_session("main")

interval = slice("2024-01","2024-03")

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
assert ((msl_spatial - msl_temporal) == 0.).all()
print("Datasets are exactly the same")
print("--------------")
