import cdflib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import os
import astropy.constants as constant
from scipy.interpolate import griddata
from matplotlib.colors import LogNorm

pas_l2_dir = r'E:\程序\Python\SolVDF\data\solar_orbiter_data\swa\science\l2\pas-vdf'
pas_name = 'solo_l2_swa-pas-vdf_20200714_v02.cdf'
pas_file = os.path.join(pas_l2_dir, pas_name)

data = cdflib.CDF(pas_file)
#%%
thetabin = data.varget('nb_Energy')
#%%
epoch = data.varget('Epoch')
vdf_time = cdflib.cdfepoch.to_datetime(epoch)
energybin = data.varget('Energy')  #'UNITS': 'eV'
thetabin = data.varget('Elevation')
phibin = data.varget('Azimuth')
rotmat_rtn_inst = data.varget('PAS_to_RTN')
vdf = data.varget('vdf')  #Units: 'eV/cm2-s-ster-eV'
speedbin = np.sqrt(2 * energybin * constant.e.value / constant.m_p.value) / 1000  # km/s
#%%
itime = 8000
vdf_temp = vdf[itime,:,:,:]
#%%
ele_arr = np.tile(thetabin[None, :, None], (11, 1, 96))
azi_arr = np.tile(phibin[:, None, None], (1, 9, 96))
vel_arr = np.tile(speedbin[None, None, :], (11, 9, 1))
vx = -np.cos(np.deg2rad(ele_arr)) * np.cos(np.deg2rad(azi_arr)) * vel_arr
vy = -np.cos(np.deg2rad(ele_arr)) * np.sin(np.deg2rad(azi_arr)) * vel_arr
vz = np.sin(np.deg2rad(ele_arr)) * vel_arr
#%%
good_ind = vdf_temp>0
vx_good = vx[good_ind]
vy_good = vy[good_ind]
vz_good = vz[good_ind]
vdf_good = vdf_temp[good_ind]
#%%
x_train = np.array([vx_good,vy_good,vz_good]).T
#%%
print([vx_good.max(),vx_good.min(),vy_good.max(),vy_good.min(),vz_good.max(),vz_good.min()])
#%%
vx_lst,vy_lst,vz_lst = np.linspace(-200,-900,71),np.linspace(-450,150,51),np.linspace(-200,300,51)
vx_arr,vy_arr,vz_arr = np.meshgrid(vx_lst,vy_lst,vz_lst,indexing='ij')
xi = np.array([vx_arr.ravel(),vy_arr.ravel(),vz_arr.ravel()]).T
#%%
clf = GaussianMixture(n_components=3,covariance_type='full')
clf.fit(x_train)
x_test = np.array([vx.ravel(),vy.ravel(),vz.ravel()]).T
g_prob = clf.predict_proba(x_test)

#%%
g1_vdf = vdf_temp*g_prob[:,0].reshape([11,9,96])
g2_vdf = vdf_temp*g_prob[:,1].reshape([11,9,96])
g3_vdf = vdf_temp*g_prob[:,2].reshape([11,9,96])
grid_g1_vdf = (griddata(x_test,g1_vdf.ravel(),xi,method='linear',fill_value=0.0)).reshape([71,51,51])
grid_g2_vdf = (griddata(x_test,g2_vdf.ravel(),xi,method='linear',fill_value=0.0)).reshape([71,51,51])
grid_g3_vdf = (griddata(x_test,g3_vdf.ravel(),xi,method='linear',fill_value=0.0)).reshape([71,51,51])
grid_vdf = (griddata(x_test,vdf_temp.ravel(),xi,method='linear',fill_value=0.0)).reshape([71,51,51])
#%%
fig = plt.figure()
fig,axs = plt.subplots(2,2,sharex=True,sharey=True)
cax=axs[0][0].pcolor(-vx_lst,vy_lst,grid_vdf[:,:,25].T,cmap='jet', norm=LogNorm(vmin=1e-14,vmax=1e-8))
axs[0][0].set_title('VDF origin')
axs[0][0].set_ylabel('$V_y$ (km/s)')
axs[0][1].pcolor(-vx_lst,vy_lst,grid_g1_vdf[:,:,25].T,cmap='jet', norm=LogNorm(vmin=1e-14,vmax=1e-8))
axs[0][1].set_title('VDF Group 1')
axs[1][0].pcolor(-vx_lst,vy_lst,grid_g2_vdf[:,:,25].T,cmap='jet', norm=LogNorm(vmin=1e-14,vmax=1e-8))
axs[1][0].set_title('VDF Group 2')
axs[1][0].set_ylabel('$V_y$ (km/s)')
axs[1][0].set_xlabel('$V_R$ (km/s)')
axs[1][1].pcolor(-vx_lst,vy_lst,grid_g3_vdf[:,:,25].T,cmap='jet', norm=LogNorm(vmin=1e-14,vmax=1e-8))
axs[1][1].set_title('VDF Group 3')
axs[1][1].set_xlabel('$V_R$ (km/s)')
fig.colorbar(cax, ax=axs, orientation='horizontal', fraction=.1, label=r'VDF $(cm^{-3}\cdot s^6)$')

axs[0]
#%%
np.linspace(-200,-900,36)
plt.show()
