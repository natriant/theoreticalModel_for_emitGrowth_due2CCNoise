"""
Study the dependence of the growth rate on the bunch length for the phase and amplitude noise injected
for one noise setting only. Possibility to plot the points that correspond to the 4 bunches.
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
          'axes.labelsize': 25,
          'axes.titlesize': 25,
          'xtick.labelsize': 25,
          'ytick.labelsize': 25,
          'image.cmap': 'jet',
          'lines.linewidth': 4,
          'lines.markersize':15,
          'font.family': 'sans-serif'}

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams.update(params)

# [coast1-setting1, coast1-setting2, coast2-setting1, coast2-setting2, coast3-setting1, coast3-setting2, coast3-setting3]
PSD_PN_list = [-122.75, -101.48, -115.22, -111.28, -111.03, -106.46, -101.48] # PSD values at fb in dBc/Hz
PSD_AN_list = [-128.15, -115.21, -124.06, -115.71, -116.92, -112.73, -106.99]

#  correspond to the coast2-setting2
setting = 3
PSD_PN_list, PSD_AN_list = [PSD_PN_list[setting]], [PSD_AN_list[setting]]
print(f'PN: {PSD_PN_list} dBc/Hz AN: \n {PSD_AN_list} dBc/Hz ')

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

for setting in np.arange(len(PSD_PN_list)):
    fig, ax = plt.subplots(1, 1)
    #ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_PN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
    #ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_AN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
    ax.plot(np.array(sigma_t_list)*4*1e9,  (np.array(dey_AN_list[setting])+np.array(dey_PN_list[setting]))*1e9*beta_0*gamma_0*1e-3*3600,'-', c='k')



sigma_t_points = [(1.71e-9)/4, (2.21e-9)/4,(2.13e-9)/4, (2.1e-9)/4 ]
#sigma_t_points = [(1.63e-9)/4, (2.15e-9)/4,(2.07e-9)/4, (2.05e-9)/4 ]


for index, my_sigma_t in enumerate(sigma_t_points):
    my_sigma_z = bunch_length_time_to_m(my_sigma_t, clight)
    my_sigma_phi = bunch_length_m_to_rad(my_sigma_z, clight, f_CC_RF)
    my_C_PN = cmpt_bunch_length_correction_factor(my_sigma_phi, noise_type='PN')
    my_C_AN = cmpt_bunch_length_correction_factor(my_sigma_phi, noise_type='AN')

    dey_PN = emit_growth_phase_noise(betay, Vcc, frev, Eb, my_C_PN, ssb_2_dsb(PSD_PN), True)
    dey_AN = emit_growth_amplitude_noise(betay, Vcc, frev, Eb, my_C_AN, ssb_2_dsb(PSD_AN), True)

    ax.plot(my_sigma_t*4*1e9, (dey_AN+dey_PN)*1e9*beta_0*gamma_0*1e-3*3600, 'o', c='C{}'.format(index), label='bunch {}'.format(index+1))


ax.legend(loc=1)
ax.set_xlabel(r'$\mathrm{4 \sigma _t \ [ns]}$')
ax.set_ylabel(r'$\mathrm{d \epsilon_y / dt \ [\mu m/h]}$')
ax.grid(linestyle='--')
#ax.set_xlim(1.5, 2.5)
#ax.set_ylim(4.8, 5.5)
plt.tight_layout()
#plt.show()

plt.savefig('./figures/dey_vs_4sigmat_Coast2-Setting2_withBunches_v2.png')


