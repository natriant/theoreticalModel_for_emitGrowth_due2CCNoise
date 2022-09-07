"""
Study the dependence of the growth rate on the bunch length for the phase and amplitude noise injected during all
coasts-settings of MD5.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../')
from utils.bunchLengthConversions import *
from utils.cmptTheoreticalEmitGrowth import *
from utils.NoiseConversions import *

# plotting parameters
params = {'legend.fontsize': 20,
          'figure.figsize': (9.5, 8.5),
          'axes.labelsize': 23,
          'axes.titlesize': 23,
          'xtick.labelsize': 23,
          'ytick.labelsize': 23,
          'image.cmap': 'jet',
          'lines.linewidth': 3,
          'lines.markersize':10,
          'font.family': 'sans-serif'}

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams.update(params)

savefig = False

# [coast1-setting1, coast1-setting2, coast2-setting1, coast2-setting2, coast3-setting1, coast3-setting2, coast3-setting3]
my_settings = ['Coast1-Setting1', 'Coast1-Setting2', 'Coast2-Setting1', 'Coast2-Setting2', 'Coast3-Setting1', 'Coast3-Setting2', 'Coast3-Setting3']
PSD_PN_list = [-122.75, -101.48, -115.22, -111.28, -111.03, -106.46, -101.48]
PSD_AN_list = [-128.15, -115.21, -124.06, -115.71, -116.92, -112.73, -106.99]

# Machine and beam parameters
betay = 73  # m in CC2, ~76 in CC1 (MAD-X)
Vcc = 1e6  # V
frev = 43.45e3  # Hz
Eb = 270e9  # eV
beta_0 = 0.999999  # cmpt it from the rest
gamma_0 = 287.7  # cmt it
clight = 299792458  # light speed in meters/second
f_CC_RF = 400.789e6  # CC frequency in Hz

# bunch length scan in rad, according to the paper of Themis&Phillipe Fig.4
sigma_phi_list = np.linspace(0, 1.6, 100)  # rad
sigma_phi_list = sigma_phi_list[1:]  # drop the first element bunch length equals zero is not realistic
sigma_z_list = bunch_length_rad_to_m(sigma_phi_list, clight, f_CC_RF)  # meters
sigma_t_list = bunch_length_m_to_time(sigma_z_list, clight)  # seconds

# Compute the correction factors due to the bunch length
myC_PN_list = cmpt_bunch_length_correction_factor(sigma_phi_list, noise_type='PN')
myC_AN_list = cmpt_bunch_length_correction_factor(sigma_phi_list, noise_type='AN')

dey_PN_list = []
dey_AN_list = []

# Compute the geometric growth in m/s
for PSD_PN in PSD_PN_list:
    dey_PN_list.append(emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN_list, ssb_2_dsb(PSD_PN), True))  # true for one-sided PSD
for PSD_AN in PSD_AN_list:
    dey_AN_list.append(emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN_list, ssb_2_dsb(PSD_AN), True))


# Plot the dependence for every noise setting
for index, setting in enumerate(my_settings):
    fig, ax = plt.subplots(1, 1)
    ax.plot(np.array(sigma_t_list)*4*1e9,  (np.array(dey_AN_list[index])+np.array(dey_PN_list[index]))*1e9*beta_0*gamma_0*1e-3*3600,'-', c='k')

    ax.set_title(f'PN: {PSD_PN_list[index]} dBc/Hz, AN: {PSD_AN_list[index]} dBc/Hz')
    ax.set_xlabel(r'$\mathrm{4 \sigma _t (ns)}$')
    ax.set_ylabel(r'$\mathrm{d \epsilon_y / dt}$' + ' ' +r'$\mathrm{\mu/h}$')
    ax.grid(linestyle='--')
    plt.tight_layout()
    if savefig:
        plt.savefig('./figures/dey_vs_4sigmat.png')
    #else:
        #plt.show()
    plt.close()

# A. Plot the relative dependence, so you can plot everything on the same plot
# Legend show the noise settings in dBc/Hz
savefig = False
fig, ax = plt.subplots(1, 1)
for index, setting in enumerate(my_settings):
    relative_growth = (np.array(dey_AN_list[index]) + np.array(dey_PN_list[index])) / (np.array(dey_AN_list[index][0]) + np.array(dey_PN_list[index][0]))

    ax.plot(np.array(sigma_t_list)*4*1e9, relative_growth, '-', c=f'C{index}', label=f'PN: {PSD_PN_list[index]} dBc/Hz, AN: {PSD_AN_list[index]} dBc/Hz')
ax.legend()
ax.set_xlabel(r'$\mathrm{4 \sigma _t (ns)}$')
ax.set_ylabel('relative '+r'$\mathrm{d \epsilon_y / dt}$')
ax.set_xlim(1.5, 2.4)
plt.ylim(0.5, 0.9)
ax.grid(linestyle='--')
plt.tight_layout()
if savefig:
    plt.savefig('./figures/relative_dey_vs_4sigmat_zoom.png')
else:
    plt.show()
plt.close()

# B. Plot the relative dependence, so you can plot everything on the same plot
# Legend show the noise settings

savefig = False
fig, ax = plt.subplots(1, 1)
for index, setting in enumerate(my_settings):
    relative_growth = (np.array(dey_AN_list[index]) + np.array(dey_PN_list[index])) / (np.array(dey_AN_list[index][0]) + np.array(dey_PN_list[index][0]))
    ax.plot(np.array(sigma_t_list)*4*1e9, relative_growth, '-', c=f'C{index}', label=f'{setting}')
ax.legend()
ax.set_xlabel(r'$\mathrm{4 \sigma _t (ns)}$')
ax.set_ylabel('relative '+r'$\mathrm{d \epsilon_y / dt}$')
#ax.set_xlim(1.5, 2.4)
#plt.ylim(0.5, 0.9)
ax.grid(linestyle='--')
plt.tight_layout()
if savefig:
    plt.savefig('./figures/relative_dey_vs_4sigmat_zoom_legnend.png')
else:
    plt.show()
plt.close()
