import numpy as np
import matplotlib.pyplot as plt
from my_functions import *

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

noise_type = 'BOTH'  # options: 'AN', 'PN', 'BOTH'

# the noise levels correspond to the coast2-setting2 ~ coast3-setting1
PSD_PN, PSD_AN = -111.28, -115.71  # PSD at fb in dBc/Hz

# Machine and beam parameters
betay = 73  # m in CC2, ~76 in CC1 (MAD-X)
Vcc = 1e6  # V
frev = 43.45e3  # Hz
Eb = 270e9  # eV
beta_0 = 0.999999  # cmpt it from the rest
gamma_0 = 287.7  # cmt it
clight = 299792458  # light speed in meters/second
f_RF = 400.789e6  # CC frequency in Hz
sigma_t = 1.7e-9/4
sigma_z = bunch_length_time_to_m(sigma_t, clight)
sigma_phi = bunch_length_m_to_rad(sigma_z, clight, f_RF)

dey_PN_list = []
dey_AN_list = []

myC_PN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='PN')
myC_AN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='AN')

Vcc_list = np.linspace(0.6e6, 1.3e6, 100)
for Vcc in Vcc_list:
    dey_PN_list.append(emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN, ssb_2_dsb(PSD_PN), True))  # true for one-sided PSD
    dey_AN_list.append(emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN, ssb_2_dsb(PSD_AN), True))




fig, ax = plt.subplots(1,1)
#ax.plot(np.array(sigma_t_list)*4*1e9, (np.array(dey_AN_list)+np.array(dey_PN_list))*1e9*beta_0*gamma_0**1e-3*3600 , '-')

#ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_PN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
#ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_AN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
ax.plot(Vcc_list/1e6,   (np.array(dey_AN_list)+np.array(dey_PN_list))*1e9*beta_0*gamma_0*1e-3*3600, '-', c='k')


#ax.legend()
ax.set_xlabel('Crab Cavity Voltage (MV)')
ax.set_ylabel(r'$d \epsilon_y / dt$' + ' ' +r'$\mu/h$')
ax.grid(linestyle='--')
#ax.set_xlim(1.5, 2.5)
#ax.set_ylim(4.8, 5.5)
plt.tight_layout()
#plt.show()

plt.savefig('./figures/dey_vs_Vcc_Coast2-Setting2_14_47.png')


