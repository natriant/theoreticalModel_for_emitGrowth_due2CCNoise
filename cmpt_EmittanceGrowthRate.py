import sys
sys.path.append('../')
from utils.bunchLengthConversions import *
from utils.cmptTheoreticalEmitGrowth import *
from utils.NoiseConversions import *


noiseType = 'PN'

# Machine and beam parameters
betay = 73  # m in CC2, ~76 in CC1 (MAD-X)
Vcc = 1e6  # V
frev = 43.45e3  # Hz
Eb = 270e9  # eV
beta_0 = 0.999999  # cmpt it from the rest
gamma_0 = 287.7  # cmt it
clight = 299792458  # light speed in meters/second
f_CC_RF = 400.789e6  # CC frequency in Hz

sigma_t = 1.7e-9/4  # initial bunch 1, coast2-setting2

sigma_z = bunch_length_time_to_m(sigma_t, clight)
sigma_phi = bunch_length_m_to_rad(sigma_z, clight, f_CC_RF)

PSD_PN = -106.99 # -101.48 #-101.48
PSD_ΑΝ =-106.99 #-115.71 #-101.48 #-101.48 #-106.99

if noiseType == 'PN':
    myC_PN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='PN')
    dey = emit_growth_phase_noise(betay, Vcc, frev, Eb, myC_PN, ssb_2_dsb(PSD_PN), True)

if noiseType == 'AN':
    myC_AN = cmpt_bunch_length_correction_factor(sigma_phi, noise_type='AN')
    dey = emit_growth_amplitude_noise(betay, Vcc, frev, Eb, myC_AN, ssb_2_dsb(PSD_ΑΝ), True)

print(f'dey/dt = {dey*1e9*beta_0*gamma_0*1e-3*3600} um/h')
