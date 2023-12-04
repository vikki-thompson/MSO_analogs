import xarray as xr
import os
import cdsapi
import subprocess
import numpy as np
import iris
import sys
import matplotlib.pyplot as plt
sys.path.append('/usr/people/thompson/WP1')
import functions_get_data as gdata
import functions_plot_data as pdata
sys.path.append('/usr/people/thompson/WP1/OTHER_EVENTS')
import functions_anyevent as adata
import cartopy.crs as ccrs
import cartopy as cart
import cartopy.feature as cf
import glob
from iris.util import equalise_attributes
from iris.util import unify_time_units
plt.ion(); plt.show()


####
## Define event date
#date = [2021, 'Jul', 14] # event date # Limburg
#date = [2021, 'Jun', 29] # Western north America heatwave 2021
date = [2023, 'Oct', 21] # Babet
season = 'son'  ## Match the month abaove (could be hardcoded)

## Define event region (N S E W)
R1 = [60, 30, 20, -20] # Storm Babet (climameter)
#R1 = [70, 30, 30, -30] # Limburg
#R1 = [65, 35, -110, -150] # Western North America

## Define time periods within which analogues are compared (2 periods)
P1_Y1 = 1979; P1_Y2 = 2002; P2_Y1 = 2001; P2_Y2 = 2023 # Climameter
#P1_Y1 = 1950; P1_Y2 = 1980; P2_Y1 = 1992; P2_Y2 = 2022 # Full ERA-5

## Define how many analogues to identify within each time period
N = 21 # Number of analogues to identify #Climameter uses 15 for 21 year period

## Define which variable analogues are identified from (psi or msl)
ana_var = 'msl'
####


if date[0] == 2023:
    print ('Data downloaded from ECMWF, using forecasts')
    datafile_surface = '/net/pc200023/nobackup/users/thompson/20231020_surface_v2.grib'
    datafile_rainfall = '/net/pc200023/nobackup/users/thompson/20231020_surface_ts24.grib'
    datafile_250 = '/net/pc200023/nobackup/users/thompson/20231020_250hpa_v4.grib'
    # Calculate the fields for the event  ### ASSUMES SON ###
    event_psi, event_msl, event_t2m, event_wind, event_tp = adata.event_data(datafile_surface, datafile_250, datafile_rainfall)
else:
    print('Using ERA5 for event')
    event_psi, event_msl, event_t2m, event_wind, event_tp = adata.event_data_era(date, season)



###
# ERA-5 data
P1_psi = adata.reanalysis_data('psi250', P1_Y1, P1_Y2, season)
P2_psi = adata.reanalysis_data('psi250', P2_Y1, P2_Y2, season)
P1_msl = adata.reanalysis_data('msl', P1_Y1, P1_Y2, season)
P2_msl = adata.reanalysis_data('msl', P2_Y1, P2_Y2, season)
P1_tp = adata.reanalysis_data('tp', P1_Y1, P1_Y2, season)
P2_tp = adata.reanalysis_data('tp', P2_Y1, P2_Y2, season)
P1_t2m = adata.reanalysis_data('t2m', P1_Y1, P1_Y2, season) ### 1990 breaks
P2_t2m = adata.reanalysis_data('t2m', P2_Y1, P2_Y2, season) ### 2014 breaks
P1_wind = adata.reanalysis_data('sfcWind', P1_Y1, P1_Y2, season)
P2_wind = adata.reanalysis_data('sfcWind', P2_Y1, P2_Y2, season)
#P1_z500 = adata.reanalysis_data('z500', P1_Y1, P1_Y2)
#P2_z500 = adata.reanalysis_data('z500', P2_Y1, P2_Y2)



'''
## Use this bit to change the methodology when not changing the time periods (to save time)
N = 15 # Number of analogues to identify
ana_var = 'msl'
R1 = [65, 40, 20, -20]
##
'''

### Plots Set:

# Calculate dates of top analogues for each period
event = gdata.extract_region(globals()['event_'+ana_var], R1) 
P1_field = gdata.extract_region(globals()['P1_'+ana_var], R1)
P2_field = gdata.extract_region(globals()['P2_'+ana_var], R1)
event = gdata.regrid(event, P1_field[0][0,...])
P1_dates = adata.analogue_dates(event, P1_field, R1)[:N]
P2_dates = adata.analogue_dates(event, P2_field, R1)[:N]
# Extra vars for plots titles
region_text =str(R1[0])+'-'+str(R1[1])+'N '+str(R1[3])+'-'+str(R1[2])+'W'
dates_text = str(P1_Y1)+'-'+str(P1_Y2)+', '+str(P2_Y1)+'-'+str(P2_Y2)
analogues_text = '#An='+str(N)
ana_variable = 'Analogue variable: '+ana_var
# Composite of psi
plot_title = '250hPa Streamfunction [x10^6 m2/s]: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable
comp_P1 = gdata.extract_region(gdata.composite_dates(P1_psi, P1_dates), R1) 
comp_P2 = gdata.extract_region(gdata.composite_dates(P2_psi, P2_dates), R1)
event_psi_reg = gdata.extract_region(event_psi, R1)
adata.field_figure('psi', event_psi_reg/10E6, comp_P1/10E6, comp_P2/10E6, plot_title)
fig_name='psi_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
# composite of slp
plot_title = 'Sea Level Pressure [hPa]: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable
comp_P1 = gdata.extract_region(gdata.composite_dates(P1_msl, P1_dates), R1) 
comp_P2 = gdata.extract_region(gdata.composite_dates(P2_msl, P2_dates), R1) 
event_msl_reg = gdata.extract_region(event_msl, R1)
event_msl_reg = gdata.regrid(event_msl_reg, comp_P1)
adata.field_figure('msl', event_msl_reg/100, comp_P1/100, comp_P2/100, plot_title)
fig_name='msl_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
## composite of t2m
#plot_title = 'Temperature at 2m [*C]: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable
#comp_P1 = gdata.extract_region(gdata.composite_dates(P1_t2m, P1_dates), R1) 
#comp_P2 = gdata.extract_region(gdata.composite_dates(P2_t2m, P2_dates), R1) 
#event_t2m_reg = gdata.extract_region(event_t2m, R1)
#event_t2m_reg = gdata.regrid(event_t2m_reg, comp_P1)
#adata.field_figure('t2m', event_t2m_reg, comp_P1, comp_P2, plot_title)
#fig_name='t2m_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
# composite of tp
plot_title = 'Daily rainfall [mm]: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable
comp_P1 = gdata.extract_region(gdata.composite_dates(P1_tp, P1_dates), R1) 
comp_P2 = gdata.extract_region(gdata.composite_dates(P2_tp, P2_dates), R1) 
event_tp_reg = gdata.extract_region(event_tp, R1)
event_tp_reg = gdata.regrid(event_tp_reg, comp_P1)
adata.field_figure('tp', event_tp_reg, comp_P1, comp_P2, plot_title)
fig_name='tp_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
# composite of wind
plot_title = 'Surface wind speed [m/s]: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable
comp_P1 = gdata.extract_region(gdata.composite_dates(P1_wind, P1_dates), R1) 
comp_P2 = gdata.extract_region(gdata.composite_dates(P2_wind, P2_dates), R1) 
event_wind_reg = gdata.extract_region(event_wind, R1)
event_wind_reg = gdata.regrid(event_wind_reg, comp_P1)
adata.field_figure('wind', event_wind_reg, comp_P1, comp_P2, plot_title)
fig_name='wind_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
#Quality measures
Q1_event = gdata.euclidean_quality_event(P1_field, event, N)
Q1_ana = gdata.euclidean_quality_analogs(P1_field, P1_dates, N)
Q2_event = gdata.euclidean_quality_event(P2_field, event, N)
Q2_ana = gdata.euclidean_quality_analogs(P2_field, P2_dates, N)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6,4))
v2 = ax.violinplot([Q1_ana, Q2_ana], [1, 1.6], showmeans=False, showextrema=False, showmedians=False)
ax.plot(1, Q1_event, marker='o', color='r')
ax.plot(1.6, Q2_event, marker='o', color='r')
ax.set_xticks([1, 1.6])
ax.set_xticklabels(['period 1', 'period 2'])
#ax.set_ylabel('250hPa Streamfunction, m^2/s')
ax.set_title('Analog Quality: '+dates_text+'. '+region_text+'. '+analogues_text+'. '+ana_variable)
fig_name='Q_'+region_text.replace(" ", "")+'_'+dates_text.replace(" ", "").replace(",","_")+'_AN'+str(N)+'_'+ana_var+'.png'
plt.savefig(fig_name)
