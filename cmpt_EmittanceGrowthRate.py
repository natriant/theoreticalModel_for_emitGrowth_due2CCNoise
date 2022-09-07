import sys
sys.path.append('../')
from utils.bunchLengthConversions import *
from utils.cmptTheoreticalEmitGrowth import *
from utils.NoiseConversions import *


noiseType = 'AN'

# Machine and beam parameters
betay = 73.81 #73.81  # m in CC2, ~76 in CC1 (MAD-X)
Vcc = 1e6  # V
clight = 299792458  # light speed in meters/second
circumference = 6911.5623  # m
frev = clight/circumference  # Hz
Eb = 270e9  # eV
beta_0 = 0.999999  # cmpt it from the rest
gamma_0 = 287.7 #287 #213 #287.7  # cmt it
f_CC_RF = 400e6  # CC frequency in Hz

sigma_t = 1.85e-9/4 #1.73e-9/4  # initial bunch 1, coast2-setting2
sigma_z = bunch_length_time_to_m(sigma_t, clight)
#sigma_z = 0.155

sigma_phi = bunch_length_m_to_rad(sigma_z, clight, f_CC_RF)

#PSD_PN = -114.75  # -101.48 #-101.48
PSD_PN = 1e-11 #9.95e-11 #6.9e-11 # rad^2/Hz
#PSD_ΑΝ = -115.71  #-115.71 #-101.48 #-101.48 #-106.99
PSD_AN = 1e-11 #3.10e-12 # rad^2/Hz

if noiseType == 'PN':
    myC_PN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='PN')
    #dey = emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN, ssb_2_dsb(PSD_PN), True)
    dey = emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN, PSD_PN, one_sided_psd = False)

if noiseType == 'AN':
    myC_AN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='AN')
    #dey = emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN, ssb_2_dsb(PSD_ΑΝ), True)
    dey = emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN, PSD_AN, one_sided_psd=False)

print(f'dey/dt = {dey*1e9*beta_0*gamma_0*1e-3*3600} um/h')
print(f'dey/dt = {dey*1e9*beta_0*gamma_0} nm/s')
