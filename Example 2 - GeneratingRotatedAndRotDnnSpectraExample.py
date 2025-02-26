'''

In this example we separately match each of the two horizontal components from 
a historic earthquake record to a RotD100 target spectrum. 

Then, the RotD100 response spectrum resulting from the 2 separately matched 
components is generated and compared with the target.

Luis A. Montejo (luis.montejo@upr.edu)

References:
    
    
    Montejo, L. A. (2021). Response spectral matching of horizontal ground motion 
    components to an orientation-independent spectrum (RotDnn). 
    Earthquake Spectra, 37(2), 1127-1144.
    
    Montejo, L. A. (2023). Spectrally matching pulse‐like records to a target 
    RotD100 spectrum. Earthquake Engineering & Structural Dynamics, 52(9), 2796-2811.
    
    Montejo, L. A., & Suarez, L. E. (2013). An improved CWT-based algorithm for 
    the generation of spectrum-compatible records.
    International Journal of Advanced Structural Engineering, 5(1), 26.
    
    Suarez, L. E., & Montejo, L. A. (2007). Applications of the wavelet transform
    in the generation and analysis of spectrum-compatible records. 
    Structural Engineering and Mechanics, 27(2), 173-197.
    
'''

from REQPY_Module import REQPY_single, load_PEERNGA_record, rotdnn
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

# input:

seed1     = 'RSN175_IMPVALL.H_H-E12140.AT2'   # seeed record comp1[g]
seed2     = 'RSN175_IMPVALL.H_H-E12230.AT2'   # seeed record comp2[g]
target    = 'ASCE7.txt'                        # target spectrum (T,PSA)
dampratio = 0.05                              # damping ratio for spectra
TL1 = 0.05; TL2 = 6                           # define period range for matching 
                                              # (T1=T2=0 matches the whole spectrum)

# load target spectrum and seed record:

s1,dt,n,name1 = load_PEERNGA_record(seed1)    # dt: time step, s: accelertion series
s2,dt,n,name2 = load_PEERNGA_record(seed2)

fs   = 1/dt                # sampling frequency (Hz)
tso = np.loadtxt(target)
To = tso[:,0]              # original target spectrum periods
dso = tso[:,1]             # original target spectrum psa

ccs1,rms1,misfit1,cvel1,cdespl1,PSAccs1,PSAs1,T,sf1 = REQPY_single(s1,fs,dso,To,
                                                    T1=TL1,T2=TL2,zi=dampratio,
                                                    nit=15,NS=100,
                                                    baseline=1,porder=-1,plots=0,nameOut=name1)

ccs2,rms2,misfit2,cvel2,cdespl2,PSAccs2,PSAs2,T,sf2 = REQPY_single(s2,fs,dso,To,
                                                    T1=TL1,T2=TL2,zi=dampratio,
                                                    nit=15,NS=100,
                                                    baseline=1,porder=-1,plots=0,nameOut=name2)

nn = 100
PSArotD100,PSA180 = rotdnn(ccs1,ccs2,dt,dampratio,T,nn)

plt.figure(figsize=(6.5,6.5))

plt.semilogx(T,PSA180.T,lw=1,color='silver',alpha=0.5)
plt.semilogx(To,dso,linewidth=2,color='navy',label='Target')
plt.semilogx(To,1.1*dso,'--',linewidth=2,color='navy',label='1.1*Target')
plt.semilogx(T,PSAccs1,color='cornflowerblue',label='H1')
plt.semilogx(T,PSAccs2,color='salmon',label='H2')
plt.semilogx(T,PSArotD100,color='darkred',label='RotD100')
plt.legend(frameon=False,ncol=5, bbox_to_anchor=(0.5,1.03),loc='center')
plt.xlim((0.015,13))
plt.xlabel('T [s]')
plt.ylabel('PSA [g]')
plt.tight_layout()
        
