'''
Script used to plot the spectral response over specified wavelengths

Course: PSC 6003 - Remote Sensing of Land Surfaces
Created: January 13th, 2017
Last edit: September 4th, 2018 (converted to Python 3.6 and added docstrings)

@author: miksch
'''

import math
import numpy as np
import matplotlib.pyplot as plt

class wavelength_spectra(object):
    '''
    Creates np.arrays of wavelengths and spectral response based on temperature using Planck's Law
    
    Inputs:
    lmbda : wavelengths of bounds for the array
    Ts : Temperature of source (K)
    
    Outputs:
    lmbda_series : np.array of wavelength values
    spectra: np.array of spectral response
    
    Methods:
    create_lmbda
    create_spectra
    '''
    
    def __init__(self,Ts,lmbda):     
        self.lmbda = lmbda #Wavelength bounds (create logspace) 
        self.Ts = Ts #Temperature of source
        self.lmbda_series = wavelength_spectra.create_lmbda(self,lmbda) #numpy array of wavelength values
        self.spectra = wavelength_spectra.create_spectra(self,Ts,self.lmbda_series)
       
    def create_lmbda(self,lmbda):
        #Currently using np.float128 as the dtype to avoid overflow error in create_spectra
        lmbda_series = np.linspace(lmbda[0],lmbda[1],num=200,dtype=np.dtype('float128'))
        return lmbda_series
    
    def create_spectra(self,T,lmbda_series):
        #Constants used in Planck's Law
        #Units: J s, J K^-1, m s^-1
        h = 6.63e-34 #Planck Constant
        c = 3.0e+8 #Speed of light
        k = 1.38e-23
        spectra = (2*math.pi*h*c**2)/(lmbda_series**5*(np.exp((h*c)/(lmbda_series*k*T))-1))
        return spectra        
        
def main():
    #Constants to determine W/m^2 at earth's orbit
    #Units: m, m
    rs = 6.95e8 #Radius of the sun
    ro = 1.49e11 #Radius of earth's orbit
    
    sun = wavelength_spectra(5800,[.05e-6,10.0e-6])
    Es_adj = sun.spectra*(rs/ro)**2
    earth = wavelength_spectra(290,[.05e-6,20.0e-6])
    
    #Plots showing the longwave and shortwave spectra, zooming into the bisects on the
    #2nd and 3rd subplots
    fig = plt.figure(figsize=(14,14))
    ax1 = fig.add_subplot(211)
    ax1.plot(sun.lmbda_series/1e-6,Es_adj,color='g',linewidth=3,label='Es at Earths Orbit')
    ax1.set_ylabel(r'Emission ' + r'$W/m^3$')
    ax1.set_xlabel(r'Wavelength ' + r'$\mu m$')
    ax1.set_title('Emission vs. Wavelength')
    ax1.plot(earth.lmbda_series/1e-6,earth.spectra,linewidth=3)
    ax1.set_xlim([0,10.0])

    
    ax21 = fig.add_subplot(223)
    ax21.plot(sun.lmbda_series/1e-6,sun.spectra,color='r',linewidth=3,label='Es at Surface of Sun')
    ax21.plot(earth.lmbda_series/1e-6,earth.spectra,linewidth=3)
    ax21.set_ylabel(r'Emission ' + r'$W/m^3$')
    ax21.set_xlabel(r'Wavelength ' + r'$\mu m$')
    ax21.set_title('Emission at Suns Surface vs. Wavelength')
    ax21.set_xlim(3,9)
    ax21.set_ylim(0,1.5e12)
    
    ax22 = fig.add_subplot(224)
    ax22.plot(sun.lmbda_series/1e-6,Es_adj,color='g',linewidth=3,label='Es at Earths Orbit')
    ax22.plot(earth.lmbda_series/1e-6,earth.spectra,linewidth=3)
    ax22.set_ylabel(r'Emission ' + r'$W/m^3$')
    ax22.set_xlabel(r'Wavelength ' + r'$\mu m$')
    ax22.set_title('Emission at Earths Orbit vs. Wavelength')
    ax22.set_xlim(3,9)
    ax22.set_ylim(0,3e7)

    plt.savefig('fullspectra.png')
    
if __name__ == '__main__':
    main()