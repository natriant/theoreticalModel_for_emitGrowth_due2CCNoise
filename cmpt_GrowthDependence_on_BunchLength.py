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

# bunch length scan in rad, according to the paper of Themis&Phillipe Fig.4
sigma_phi_list = np.linspace(0, 1.6, 100)  # rad
sigma_phi_list = sigma_phi_list[1:]  # drop the first element bunch length equals zero is not realistic

myC_PN_list = []
myC_AN_list = []
dey_PN_list = []
dey_AN_list = []

for sigma_phi in sigma_phi_list:
    myC_PN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='PN')
    myC_AN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='AN')
    myC_PN_list.append(myC_PN)
    myC_AN_list.append(myC_AN)

    dey_PN_list.append(emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN, ssb_2_dsb(PSD_PN), True))  # true for one-sided PSD
    dey_AN_list.append(emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN, ssb_2_dsb(PSD_AN), True))  # true for

sigma_z_list = []
for sigma_phi in sigma_phi_list:
    sigma_z_list.append(bunch_length_rad_to_m(sigma_phi, clight, f_RF))


sigma_t_list = []
for sigma_z in sigma_z_list:
    sigma_t_list.append(bunch_length_m_to_time(sigma_z, clight))

fig, ax = plt.subplots(1,1)
#ax.plot(np.array(sigma_t_list)*4*1e9, (np.array(dey_AN_list)+np.array(dey_PN_list))*1e9*beta_0*gamma_0**1e-3*3600 , '-')

#ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_PN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
#ax.plot(np.array(sigma_t_list)*4*1e9,  np.array(dey_AN_list)*1e9*beta_0*gamma_0*1e-3*3600 , '-')
ax.plot(np.array(sigma_t_list)*4*1e9,  (np.array(dey_AN_list)+np.array(dey_PN_list))*1e9*beta_0*gamma_0*1e-3*3600, '-', c='k')


sigma_t_points = [(1.71e-9)/4, (2.21e-9)/4,(2.13e-9)/4, (2.1e-9)/4 ]
#sigma_t_points = [(1.63e-9)/4, (2.15e-9)/4,(2.07e-9)/4, (2.05e-9)/4 ]


for index, my_sigma_t in enumerate(sigma_t_points):
    my_sigma_z = bunch_length_time_to_m(my_sigma_t, clight)
    my_sigma_phi = bunch_length_m_to_rad(my_sigma_z, clight, f_RF)
    my_C_PN = cmpt_bunch_length_correction_factor(my_sigma_phi, noise_type='PN')
    my_C_AN = cmpt_bunch_length_correction_factor(my_sigma_phi, noise_type='AN')

    dey_PN = emit_growth_phase_noise(betay, Vcc, frev, Eb, my_C_PN, ssb_2_dsb(PSD_PN), True)
    dey_AN = emit_growth_amplitude_noise(betay, Vcc, frev, Eb, my_C_AN, ssb_2_dsb(PSD_AN), True)

    ax.plot(my_sigma_t*4*1e9, (dey_AN+dey_PN)*1e9*beta_0*gamma_0*1e-3*3600, 'o', c='C{}'.format(index), label='bunch {}'.format(index+1))

ax.legend()
ax.set_xlabel(r'$4 \sigma _t (ns)$')
ax.set_ylabel(r'$d \epsilon_y / dt$' + ' ' +r'$\mu/h$')
ax.grid(linestyle='--')
#ax.set_xlim(1.5, 2.5)
#ax.set_ylim(4.8, 5.5)
plt.tight_layout()
#plt.show()

plt.savefig('./figures/dey_vs_4sigmat_Coast2-Setting2_14_47.png')


