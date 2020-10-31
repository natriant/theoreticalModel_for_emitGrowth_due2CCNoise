import os, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../')
from utils.bunchLengthConversions import *
from utils.cmptTheoreticalEmitGrowth import *


# plotting parameters
params = {'legend.fontsize': 20,
          'figure.figsize': (9.5, 8.5),
          'axes.labelsize': 23,
          'axes.titlesize': 23,
          'xtick.labelsize': 23,
          'ytick.labelsize': 23,
          'image.cmap': 'jet',
          'lines.linewidth': 2,
          'lines.markersize':5,
          'font.family': 'sans-serif'}

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams.update(params)

clight = 299792458  # light speed in meters/second
f_RF = 400.789e6  # CC frequency in Hz
sigma_z_list = np.linspace(0, 0.19, 100) # rms bunch length in meters
noise_type = 'AN'  # options: 'PN', 'AN'
if noise_type == 'PN':
    my_color = 'mediumblue'
else:
    my_color = 'r'

# give a list of bunch length you want to appear on the dependence
bunch_lengths_in_s = [] # if no points --> [''] # 4sigma_t
bunch_lengths_in_m = []
bunch_lengths_in_rad = []

C_list = []
sigma_phi_list = []
for z in sigma_z_list[1:]:  # skip the first element as bunch length zero doesn't exist
    sigma_phi = bunch_length_m_to_rad(z, clight, f_RF)
    my_C = cmpt_bunch_length_correction_factor(sigma_phi, noise_type)

    sigma_phi_list.append(sigma_phi)
    C_list.append(my_C)



# A. Bunch length in meters
fig, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(sigma_z_list[1:], C_list, c=my_color)
#ax1.plot(sigma_z, C, 'o',color='r', markersize=7, label=r'$\rm \sigma_z$' +' at SPS CC tests')
if noise_type == 'PN':
    ax1.set_ylabel(r'$\rm C_{\Delta \phi} (\sigma_z) $')
else:
    ax1.set_ylabel(r'$\rm C_{\Delta A} (\sigma_z) $')
ax1.set_xlabel(r'$\rm \sigma_z(m)$')
ax1.grid(linestyle='--')
#ax1.legend()
plt.tight_layout()
plt.savefig('./figures/Correction_factor_bunch_length_sigmaZ_{}.png'.format(noise_type))
plt.close()

# B. Bunch length in rad
fig, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(sigma_phi_list, C_list, c=my_color)
#ax1.plot(sigma_z, C, 'o',color='r', markersize=7, label=r'$\rm \sigma_z$' +' at SPS CC tests')
if noise_type == 'PN':
    ax1.set_ylabel(r'$\rm C_{\Delta \phi} (\sigma_ \phi) $')
else:
    ax1.set_ylabel(r'$\rm C_{\Delta A} (\sigma_\phi) $')
ax1.set_xlabel(r'$\rm \sigma_ \phi(rad)$')
ax1.grid(linestyle='--')
#ax1.legend()
plt.tight_layout()
plt.savefig('./figures/Correction_factor_bunch_length_sigmaPhi_{}.png'.format(noise_type))
plt.close()

# B. Bunch length in seconds
sigma_t_list = []
for sigma_z in sigma_z_list[1:]:  # skip the first element as bunch length zero doesn't exist
    sigma_t_list.append(bunch_length_m_to_time(sigma_z, clight))

fig, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(np.array(sigma_t_list)*4*1e9, C_list, c=my_color)
#ax1.plot(sigma_z, C, 'o',color='r', markersize=7, label=r'$\rm \sigma_z$' +' at SPS CC tests')
if noise_type == 'PN':
    ax1.set_ylabel(r'$\rm C_{\Delta \phi} (\sigma_t) $')
else:
    ax1.set_ylabel(r'$\rm C_{\Delta A} (\sigma_t) $')
ax1.set_xlabel(r'$\rm 4 \sigma_ t(ns)$')
ax1.grid(linestyle='--')
#ax1.legend()
plt.tight_layout()
plt.savefig('./figures/Correction_factor_bunch_length_sigmat_{}.png'.format(noise_type))
plt.close()
