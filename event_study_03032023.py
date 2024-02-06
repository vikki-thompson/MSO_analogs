# Identify streamfunction analogs
#
#
#
#
#
#
# Original: vikki.thompson 07/03/2023
# Last Editted 22 Mar 2023


# Load neccessary libraries
import subprocess
import iris
import iris.coord_categorisation as icc
from iris.coord_categorisation import add_season_membership
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy as cart
import glob
import matplotlib.cm as mpl_cm
import sys
import scipy.stats as sps
from scipy.stats import genextreme as gev
import random
import scipy.io
import xarray as xr
import netCDF4 as nc
import iris.coords
from iris.util import equalise_attributes
from iris.util import unify_time_units
import sys
sys.path.append('/usr/people/thompson/WP1')
import functions_get_data as gdata
import functions_plot_data as pdata
import cartopy.crs as ccrs
import cartopy as cart
import cartopy.feature as cf
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker

### Selection
# Event date
sel_year = 2021
sel_month = 'Jul'
sel_day = 14
# Analogs
N = 33



def var_event_data(var, N1, S1, E1, W1, date):
    if var == 'psi250':
        var_cube = gdata.era5_mydata(var, range(2021,2023))
    else:
        var_cube = gdata.era5_data(var, range(2021,2023))
    var_reg = gdata.extract_region(var_cube, N=N1, S=S1, E=E1, W=W1)
    if var == 'psi250':
        iris.coord_categorisation.add_month(var_reg, 'time')
        iris.coord_categorisation.add_day_of_month(var_reg, 'time')
    else: pass
    return gdata.pull_out_day_era(var_reg, date[0], date[1], date[2])
    



def var_map(N1, S1, E1, W1, date):
    # var data
    event_psi250 = var_event_data('psi250', N1, S1, E1, W1, date)
    event_slp = var_event_data('msl', N1, S1, E1, W1, date)/1000
    event_prec = var_event_data('tp', N1, S1, E1, W1, date)
    # plot data
    plt.ion(); plt.show()
    fig, axs = plt.subplots(nrows=1, ncols=3, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10,5))
    lats=event_psi250.coord('latitude').points
    lons=event_psi250.coord('longitude').points
    c = axs[0].contourf(lons, lats, event_psi250.data, levels=np.linspace(-8.2e7, 1e7, 10), cmap = plt.cm.get_cmap('RdBu_r'), transform=ccrs.PlateCarree(), extend='both')
    axs[0].set_title('psi250')
    cb = fig.colorbar(c, ax=axs[0], orientation="horizontal", pad=0.2)
    tick_locator1 = ticker.MaxNLocator(nbins=5)
    cb.locator = tick_locator1
    cb.update_ticks()
    lats=event_slp.coord('latitude').points
    lons=event_slp.coord('longitude').points
    c = axs[1].contourf(lons, lats, event_slp.data, levels=np.linspace(100, 103.3, 10), cmap = plt.cm.get_cmap('RdBu_r'), transform=ccrs.PlateCarree(), extend='both')
    axs[1].set_title('slp')
    cd = fig.colorbar(c, ax=axs[1], orientation="horizontal", pad=0.2)
    tick_locator2 = ticker.MaxNLocator(nbins=5)
    cd.locator = tick_locator2
    cd.update_ticks()
    c = axs[2].contourf(lons, lats, event_prec.data, levels=np.linspace(0, 100, 10), cmap = plt.cm.get_cmap('RdBu_r'), transform=ccrs.PlateCarree(), extend='both')
    axs[2].set_title('prec')
    ce = fig.colorbar(c, ax=axs[2], orientation="horizontal", pad=0.2)
    tick_locator3 = ticker.MaxNLocator(nbins=5)
    ce.locator = tick_locator3
    ce.update_ticks()
    for ax in axs:
        ax.add_feature(cf.BORDERS)
        ax.add_feature(cf.COASTLINE)
    #axs[0].colorbar(c, fraction=0.046, pad=0.04)
    plt.suptitle(str(date[2])+date[1]+str(date[0]))



def psi_map(N1, S1, E1, W1, date):
    event_psi250 = var_event_data('psi250', N1, S1, E1, W1, date)
    plt.ion(); plt.show()
    fig, axs = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10,5))
    lats=event_psi250.coord('latitude').points
    lons=event_psi250.coord('longitude').points
    c = axs.contourf(lons, lats, event_psi250.data, levels=np.linspace(-8.2e7, 1e7, 10), cmap = plt.cm.get_cmap('RdBu_r'), transform=ccrs.PlateCarree(), extend='both')
    axs.set_title(str(date[2])+date[1]+str(date[0])+', psi250')
    cb = fig.colorbar(c, ax=axs, orientation="horizontal", pad=0.04)
    tick_locator1 = ticker.MaxNLocator(nbins=5)
    cb.locator = tick_locator1
    cb.update_ticks()
    axs.add_feature(cf.BORDERS)
    axs.add_feature(cf.COASTLINE)
    #axs[0].colorbar(c, fraction=0.046, pad=0.04)



N1 = 70; S1 = 30; E1 = 25; W1 = -15
var_map(N1, S1, E1, W1, (2021, 'Jul', 11))
var_map(N1, S1, E1, W1, (2021, 'Jul', 12))
var_map(N1, S1, E1, W1, (2021, 'Jul', 13))
var_map(N1, S1, E1, W1, (2021, 'Jul', 14))
var_map(N1, S1, E1, W1, (2021, 'Jul', 15))
var_map(N1, S1, E1, W1, (2021, 'Jul', 16))

N1=90; S1=00; E1=180; W1=-180
psi_map(N1, S1, E1, W1, (2021, 'Jul', 11))
psi_map(N1, S1, E1, W1, (2021, 'Jul', 12))
psi_map(N1, S1, E1, W1, (2021, 'Jul', 13))
psi_map(N1, S1, E1, W1, (2021, 'Jul', 14))
psi_map(N1, S1, E1, W1, (2021, 'Jul', 15))
psi_map(N1, S1, E1, W1, (2021, 'Jul', 16))



