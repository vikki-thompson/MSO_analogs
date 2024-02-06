
# Figures for analog paper, ERA5
#
#
# Original: vikki.thompson 26/07/2023
# Last Editted 7 June 2023


### Load neccessary libraries
import subprocess
import numpy as np
import iris
import sys
import matplotlib.pyplot as plt
sys.path.append('/usr/people/thompson/WP1')
import functions_get_data as gdata
import functions_plot_data as pdata

import cartopy.crs as ccrs
import cartopy as cart
import cartopy.feature as cf
import glob
plt.ion(); plt.show()

## Variables
R1 = [70, 30, 30, -30] # analog region
R2 = [62, 42, 20, -10] # Hylke's region
R3 = [80, 20, 180, -180]
date = [2021, 'Jul', 14] # event date
##

## Analogues
region = R1
past_Y1 = 1950
past_Y2 = 1980
present_Y1 = 1993
present_Y2 = 2023

# Get data, find analogues based on streamfunction
psi_event = gdata.extract_region(gdata.extract_JJA(gdata.era5_mydata('psi250', range(2021,2023))), region)
event = gdata.pull_out_day_era(psi_event, date[0], date[1], date[2])
psi_past = gdata.extract_region(gdata.extract_JJA(gdata.era5_mydata('psi250', range(past_Y1,past_Y2))), region)
psi_present= gdata.extract_region(gdata.extract_JJA(gdata.era5_mydata('psi250', range(present_Y1,present_Y2))), region)
dates_past = gdata.analogs_datelist(psi_past, event)[:30] # find analogs
dates_present = gdata.analogs_datelist(psi_present, event)[:30]



## FOR LENTIS
psi_era = gdata.extract_region(gdata.extract_JJA(gdata.era5_mydata('psi250', range(2013,2023))), R1)
psi_lentis = gdata.extract_region(gdata.extract_JJA(gdata.lentis_mydata()), R1)
psi_lentis_future = gdata.extract_region((gdata.extract_JJA(gdata.lentis_mydata(run='F'))), R1)
psi_lentis = gdata.regrid(psi_lentis, event)
psi_lentis_future = gdata.regrid(psi_lentis_future, event)

date_list = ['0072003809', '0112009729', '0142004809', '0162002728', '0192002726', '0212005726', '0262008802', '0292003718', '0292006816', '0292008811', '0302002804', '0312002725', '0322000719', '0342007814', '0362003807', '0382000812', '0412001717', '0492003716', '0502001818', '0502003730', '0522001730', '0522002713', '0542002812', '0592008828', '0612001810', '0612005725', '0622003825', '0642004723', '0652002821', '0652007803', '0692009807', '0702001813', '0712003801', '0752006721', '0762000728', '0772003729', '0772005801', '0782001830', '0792008720', '0802008819', '0812005813', '0822003808', '0832007831', '0852004726', '0862003808', '0862008713', '0892004730', '0912005728', '0932004824', '0942002806', '0942007721', '0982000729', '1002000806', '1002009720', '1012002721', '1012004815', '1022003725', '1032006820', '1042000726', '1052003724', '1092006803', '1102004818', '1122002827', '1132002721', '1142008725', '1152002802', '1162000715', '1172001814', '1202001802', '1212009817', '1242002818', '1252002729', '1282009725', '1302000725', '1322009727', '1342003728', '1372004823', '1392004720', '1412004727', '1442000831', '1442008712', '1442009817', '1452005819', '1452007813', '1452008811', '1452009817', '1482001718', '1492003827', '1522002716', '1532008829', '1542003822', '1542004717', '1542009815', '1572002811', '1572007803']
euc_dist = [383769470.0, 398308450.0, 384022370.0, 363571840.0, 398164540.0, 391334000.0, 341080220.0, 360858750.0, 334284450.0, 370511230.0, 384829100.0, 302420860.0, 313260830.0, 385307000.0, 387248860.0, 372859500.0, 391929180.0, 388205500.0, 396093500.0, 374797600.0, 384613630.0, 362002560.0, 378028100.0, 368107970.0, 330554620.0, 299685980.0, 384467400.0, 392783400.0, 369541250.0, 324847780.0, 373609920.0, 348826180.0, 347052830.0, 392992300.0, 375121300.0, 398415140.0, 386062750.0, 322342370.0, 334164600.0, 394218140.0, 392157200.0, 352917440.0, 385773470.0, 380210240.0, 390425200.0, 397124400.0, 367475780.0, 352604320.0, 393712350.0, 312966700.0, 369285730.0, 388517900.0, 386747400.0, 364849020.0, 386885280.0, 363963600.0, 397069660.0, 345820800.0, 378979800.0, 374814340.0, 353899170.0, 382420060.0, 379821570.0, 378096200.0, 397395420.0, 346168130.0, 307852960.0, 376201570.0, 392388960.0, 334605630.0, 352790530.0, 365396300.0, 382002720.0, 321811680.0, 375482340.0, 380925820.0, 398847170.0, 366802620.0, 360340450.0, 332393730.0, 397358750.0, 329283740.0, 313233440.0, 390194100.0, 396939260.0, 381506430.0, 367474660.0, 370281630.0, 352665540.0, 398021200.0, 390068260.0, 396419420.0, 342712300.0, 388975940.0, 397890560.0]

# Next line sorts the date list by the euclidean distance (so I can plot events in minimum distance order)
Z = [x for _,x in sorted(zip(euc_dist, date_list))]

date_list_future = ['0002075814', '0002080807', '0012077814', '0022076722', '0022084803', '0032076801', '0032077731', '0042076812', '0072078805', '0072079715', '0092080805', '0122076726', '0122077803', '0122082815', '0132076803', '0132077818', '0142081809', '0172076717', '0182083808', '0182084824', '0192077719', '0202076817', '0222079714', '0232077804', '0252081811', '0262075720', '0302080809', '0312078716', '0312084821', '0322083721', '0332083808', '0342079731', '0382076710', '0392078804', '0412076815', '0412080801', '0422080802', '0432076710', '0442077822', '0442081817', '0462081802', '0482076817', '0492078807', '0492081801', '0502079814', '0542080803', '0542084721', '0552084806', '0562084730', '0572078813', '0572082806', '0582082820', '0592083810', '0602077721', '0612076813', '0612079810', '0622083823', '0632079802', '0632080803', '0642079817', '0652075728', '0672084805', '0682075724', '0682083821', '0682084728', '0692081809', '0692082730', '0702077720', '0702079814', '0702082822', '0752076813', '0752077731', '0772077803', '0792076807', '0792080802', '0802079820', '0822076823', '0852078726', '0852083827', '0862075726', '0862084711', '0872081816', '0882076823', '0892076817', '0892083812', '0892084815', '0902081727', '0922079817', '0962080819', '0962084801', '0982084825', '0992083805', '1002078823', '1012077831', '1032078822', '1032079806', '1032082821', '1042076720', '1052077724', '1052078721']
euc_dist_future = [387434560.0, 372560640.0, 339371200.0, 383333220.0, 379542800.0, 385648420.0, 370060640.0, 384461660.0, 345797600.0, 372931140.0, 380576000.0, 376262050.0, 371955200.0, 298734820.0, 385781440.0, 353624740.0, 381472930.0, 375835900.0, 385588130.0, 275282200.0, 385672670.0, 353011600.0, 347564130.0, 323102720.0, 335224480.0, 385430000.0, 373379700.0, 378114020.0, 374401660.0, 380882240.0, 311983330.0, 377431330.0, 366168540.0, 327430000.0, 378197400.0, 387038900.0, 380519140.0, 360085470.0, 383034850.0, 371432640.0, 311750140.0, 369696450.0, 356651940.0, 357363420.0, 365603870.0, 315797340.0, 371705300.0, 369408260.0, 374296320.0, 376013150.0, 364923000.0, 384782100.0, 375115420.0, 385457380.0, 374187900.0, 371577760.0, 326246460.0, 377671700.0, 348616260.0, 354374080.0, 344209020.0, 369619170.0, 360292350.0, 354216030.0, 376531700.0, 362650460.0, 374187040.0, 365925000.0, 371743100.0, 351688830.0, 368676030.0, 340654560.0, 384840640.0, 381814240.0, 377411940.0, 386327170.0, 289593400.0, 372517440.0, 290284830.0, 362183460.0, 374905000.0, 334149570.0, 379100000.0, 366104350.0, 362510340.0, 346076960.0, 361016670.0, 374965200.0, 354852450.0, 368357730.0, 342274600.0, 333252060.0, 360338750.0, 314502880.0, 334556500.0, 379501760.0, 372532900.0, 370394600.0, 311106620.0, 386914700.0]

Z_future = [x for _,x in sorted(zip(euc_dist_future, date_list_future))]



# Quality measures
Q1_event = gdata.euclidean_quality_event(psi_past, event)
Q1_ana = gdata.euclidean_quality_analogs(psi_past, dates_past)
Q2_event = gdata.euclidean_quality_event(psi_present, event)
Q2_ana = gdata.euclidean_quality_analogs(psi_present, dates_present)

#Q1_mod_event = gdata.euclidean_quality_event_lentis(psi_lentis, event)
#Q1_mod = gdata.euclidean_quality_analogs_lentis(psi_lentis, Z[:30])
Q1_mod_event = 12762001000.0
Q1_mod = [11855182000.0, 11502760000.0, 11768051000.0, 11863191000.0, 9692483000.0, 13766084000.0, 11209950000.0, 11596837000.0, 11610051000.0, 11409138000.0, 12892709000.0, 13039930000.0, 11254094000.0, 12460042000.0, 11720471000.0, 10937802000.0, 12454405000.0, 11727070000.0, 12005048000.0, 14093509000.0, 12536372000.0, 11901165000.0, 11321923000.0, 10936279000.0, 10883772000.0, 11397091000.0, 14480349000.0, 12620607000.0, 10704527000.0, 11513945000.0]
#Q2_mod_event = gdata.euclidean_quality_event_lentis(psi_lentis_future, event)
#Q2_mod = gdata.euclidean_quality_analogs_lentis(psi_lentis_future, Z_future[:30])
Q2_mod_event = 12216121000.0
Q2_mod = [12564896000.0, 10183287000.0, 9773950000.0, 10224206000.0, 9846750000.0, 11121827000.0, 9834884000.0, 10722683000.0, 10309988000.0, 9683113000.0, 11124484000.0, 10819929000.0, 11954808000.0, 10437420000.0, 12144616000.0, 10197710000.0, 10251432000.0, 10907635000.0, 11688797000.0, 11568869000.0, 8653313000.0, 10297848000.0, 11624420000.0, 10594199000.0, 11467249000.0, 10068944000.0, 10456167000.0, 11905068000.0, 11186170000.0, 10250477000.0]

Q1_mod_v2 = []
for val in Q1_mod:
    Q1_mod_v2.append(val/1e10)

Q2_mod_v2 = []
for val in Q2_mod:
    Q2_mod_v2.append(val/1e10)

Q1_ana_v2 = []
for val in Q1_ana:
    Q1_ana_v2.append(val/1e10)

Q2_ana_v2 = []
for val in Q2_ana:
    Q2_ana_v2.append(val/1e10)


Q1_event = 1/(Q1_event/1e10)
Q2_event = 1/(Q2_event/1e10)
Q1_ana_v2 = 1/np.array(Q1_ana_v2)
Q2_ana_v2 = 1/np.array(Q2_ana_v2)

Q1_mod_event = 1/(Q1_mod_event/1e10)
Q2_mod_event = 1/(Q2_mod_event/1e10)
Q1_mod_v2 = 1/np.array(Q1_mod_v2)
Q2_mod_v2 = 1/np.array(Q2_mod_v2)
    
# Violin plots of quality
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(6,7))
v1 = ax[0,0].violinplot([Q1_ana_v2, Q2_ana_v2], [1, 1.6], showmeans=False, showextrema=False, showmedians=False)
colors = ['g','b']
for pc, color in zip(v1['bodies'], colors):
    pc.set_facecolor(color)

ax[0,0].plot(1, Q1_event, marker='o', color='r')
ax[0,0].plot(1.6, Q2_event, marker='o', color='r')
ax[0,0].axhline(np.mean(Q1_ana_v2), color='g')
ax[0,0].axhline(np.mean(Q2_ana_v2), color='b')
ax[0,0].set_xticks([1, 1.6])
ax[0,0].set_xticklabels(['Past', 'Present'])
ax[0,0].set_ylabel('T (x $10^{10}$ s/m$^2$)')
ax[0,0].set_title('Typicality')
ax[0,0].set_title('(a)', loc='left')
ax[0,0].set_ylim([.68, 1.18])

v2 = ax[1,0].violinplot([Q1_mod_v2, Q2_mod_v2], [1, 1.6], showmeans=False, showextrema=False, showmedians=False)
colors = ['b','m']
for pc, color in zip(v2['bodies'], colors):
    pc.set_facecolor(color)

ax[1,0].plot(1, Q1_mod_event, marker='o', color='r')
ax[1,0].plot(1.6, Q2_mod_event, marker='o', color='r')
ax[1,0].axhline(np.mean(Q1_mod_v2), color='b')
ax[1,0].axhline(np.mean(Q2_mod_v2), color='m')
ax[1,0].set_xticks([1, 1.6])
ax[1,0].set_xticklabels(['Present', 'Future'])
ax[1,0].set_ylabel('T (x $10^{10}$ s/m$^2$)')
ax[1,0].set_title('(b)', loc='left')
ax[1,0].set_ylim([.68, 1.18])




## from analog_persistence_130923.py
Pevent = 4
P_past =[2, 14, 9, 6, 4, 4, 8, 6, 11, 8, 8, 5, 3, 4, 3, 5, 3, 7, 4, 5, 6, 4, 10, 5, 2, 3, 3, 4, 3, 3]
P_present = [5, 4, 7, 5, 1, 3, 1, 4, 5, 13, 5, 6, 7, 4, 3, 4, 9, 4, 9, 7, 16, 14, 5, 5, 3, 5, 7, 4, 3, 6]
PL_present = [4, 8, 6, 7, 10, 5, 4, 4, 5, 5, 3, 2, 6, 7, 11, 4, 3, 5, 3, 5, 9, 3, 4, 2, 4, 7, 5, 2, 7, 6] 
PL_future = [5, 2, 6, 11, 9, 5, 6, 1, 5, 4, 3, 4, 6, 6, 11, 6, 5, 7, 5, 10, 8, 7, 3, 2, 5, 8, 8, 3, 1, 7]

# Top N
N= 30
P_past = P_past[:N]
P_present = P_present[:N]
PL_present = PL_present[:N]
PL_future = PL_future[:N]

# how many days remaining below 0.1 CC? for event it is 4
# Violin plots of persistence
v1 = ax[0,1].violinplot([P_past, P_present], [1, 1.6], showmeans=False, showextrema=False, showmedians=False)
colors = ['g','b']
for pc, color in zip(v1['bodies'], colors):
    pc.set_facecolor(color)

#ax[0,1].axhline(Pevent, color='r')
ax[0,1].plot(1, Pevent, marker='o', color='r')
ax[0,1].plot(1.6, Pevent, marker='o', color='r')
ax[0,1].axhline(np.mean(P_past), color='g')
ax[0,1].axhline(np.mean(P_present), color='b')
ax[0,1].set_xticks([1, 1.6])
ax[0,1].set_xticklabels(['Past', 'Present'])
ax[0,1].set_ylim([0,17])
ax[0,1].set_yticks([0, 5, 10, 15])
ax[0,1].set_title('Persistence')
ax[0,1].set_ylabel('P (days)')
ax[0,1].set_title('(c)', loc='left')


v2 = ax[1,1].violinplot([PL_present, PL_future], [1, 1.6], showmeans=False, showextrema=False, showmedians=False)
colors = ['b','m']
for pc, color in zip(v2['bodies'], colors):
    pc.set_facecolor(color)

#ax[1,1].axhline(Pevent, color='r')
ax[1,1].plot(1, Pevent, marker='o', color='r')
ax[1,1].plot(1.6, Pevent, marker='o', color='r')
ax[1,1].axhline(np.mean(PL_present), color='b')
ax[1,1].axhline(np.mean(PL_future), color='m')
ax[1,1].set_xticks([1, 1.6])
ax[1,1].set_xticklabels(['Present', 'Future'])
ax[1,1].set_ylim([0,17])
ax[1,1].set_yticks([0, 5, 10, 15])
ax[1,1].set_title('(d)', loc='left')
ax[1,1].set_ylabel('P (days)')


plt.subplots_adjust(left=0.3, wspace=.3)
plt.figtext(0.1, 0.72, 'ERA-5', fontsize = 12)
plt.figtext(0.05, 0.25, 'KNMI-LENTIS', fontsize = 12)





