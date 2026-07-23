# test-era5-access
Benchmark tests for the Earthmover ERA5 data store

To set up environment:
```
conda env create -f environment.yml
conda activate test-era5
```

To run tests:
```
python test-era5.py
```

## Steps to running the test on AWS EC2 instance:
```
sudo dnf install git -y
git clone https://github.com/brian-rose/test-era5-access.git
cd test-era5-access
"${SHELL}" <(curl -L micro.mamba.pm)
source ~/.bashrc
micromamba env create -f environment.yml 
micromamba activate test-era5
python test-era5.py
```

But the tests currently do not run on any of the free AWS tier instances because it requires at least 8.45 GiB memory.
