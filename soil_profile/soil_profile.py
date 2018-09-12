'''
Calculates the soil temperature profile for a 24 hour period given an average and change of
temperature and soil depth

Course: PSC 6500 - Environmental Physics of Land Ecosystems and Climate
Created: March 2017
Last edit: September 12th, 2018 (added docstrings)

@author: miksch
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class Profile(object):
    '''
    Creates soil temperature profile through depth and time
    
    Inputs:
    t : range of times (in hours) e.g. [0.,24.]
    z : range of soil depths (in meters) e.g. [0.,0.3]
    Tavg : Average temperature at surface
    T0 : Amplitude of temperature change at surface
    K : Thermal diffusivity of soil
    p : Period of time (24 hours)
    
    Internal functions:
    create_series
    temp_profile
    
    Properties:
    z_profile : profile of depths
    t_profile : profile of soil temperatures
    x : x-coordinates for plotting
    y : y-coordinates for plotting
    '''
    
    def __init__(self,t,z,Tavg,T0,K,p):
        self.ts = Profile.create_series(self,t) 
        self.z_profile = Profile.create_series(self,z)
        self.t_profile = Profile.temp_profile(self,self.ts,self.z_profile,Tavg,T0,K,p)
        self.x, self.y = np.meshgrid(self.ts,self.z_profile)
    
    #Create np.array to calculate t profile and grid for plotting  
    def create_series(self,rnge):
        series = np.linspace(rnge[0],rnge[1],num=500)
        return series
    
    #Calculates 2d np.array of temperatures    
    def temp_profile(self,ts,z_prof,Tavg,T0,K,p):
        w = (2*np.pi)/(p*3600)
        D = np.sqrt((2*K)/w)
        
        #correct ts and z_prof to make proper 2d graph
        ts.shape = (1,len(ts))
        z_prof.shape = (len(z_prof),1)
        
        #calculate profile
        t_prof = Tavg + T0*np.exp(-z_prof/D)*np.sin(w*ts*3600-z_prof/D)
        return t_prof                     

def subplots(ax,K_curve,K):
    ax.set_xlabel('Time [hour]')
    ax.set_xlim(0,24)
    ax.set_ylabel('Depth [m]')
    ax.set_ylim(0,.3)
    ax.set_zlabel('Temperature [deg C]')
    ax.set_zlim(0,25)
    
    #manually set contour interval
    cont_int_y = np.linspace(K_curve.y[0,0],K_curve.y[-1,-1],10)
    #cont_int_z = np.linspace(K_curve.t_profile.min(),K_curve.t_profile.max(),10)
    
    ax.plot_surface(K_curve.x, K_curve.y, K_curve.t_profile,
                    cmap=cm.coolwarm,linewidth=0,alpha=.8)
    ax.contour(K_curve.x, K_curve.y, K_curve.t_profile, 10, zdir='z', offset=-.3, cmap=cm.coolwarm)
    ax.contour(K_curve.x, K_curve.y, K_curve.t_profile, cont_int_y, zdir='y', offset=.3, cmap=cm.viridis_r)
    ax.set_title('Temperature Profile: K='+str(K))

def main():
    
    #CONSTANTS
    #Thermal diffusivity values [m^2s^-1]
    K1 = 2.0e-7
    K2 = 8.0e-7
    #period [Hours]
    p = 24.
    
    #Temperature values [C]
    Tavg = 15.
    T0 = 10.
    
    #Time and Z profile ranges [Hours], [m]
    t = [0.,24.]
    z = [0.,.3]
    
    K1_curve = Profile(t,z,Tavg,T0,K1,p)
    K2_curve = Profile(t,z,Tavg,T0,K2,p)
    
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(121,projection='3d')
    subplots(ax1,K1_curve,K1)
    ax2 = fig.add_subplot(122,projection='3d')
    subplots(ax2,K2_curve,K2) 

    plt.savefig('soil_profiles.png')
    
if __name__ == main():
    main()
