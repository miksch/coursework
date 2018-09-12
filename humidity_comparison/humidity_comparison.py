'''
Comparison between humidity measurements made by a thermocouple psychrometer and a capacitance
RH sensor.

Course: PSC 6000 - Environmental Instrumentation
Created: September 18th, 2017
Last edit: September 12th, 2017 (added docstrings and comments)

@author: miksch
'''


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def Wexler_es(Temps):
    '''
    Compute the saturated vapor pressure using the equation from Wexler (1976) with coefficients
    from Hardy (1998)
    
    Inputs:
    Temps : np.array of temperatures [K]
    
    Outputs:
    es : np.array of saturation vapor pressures [Pa]
    '''
    
    #Hardy (1998) coefficients
    g = np.array((-2.8365744e3,
                 -6.028076559e3,
                 1.954263612e1,
                 -2.737830188e-2,
                 1.6261698e-5,
                 7.0229056e-10,
                 -1.8680009e-13,
                 2.7150305))
    
    es=np.empty(Temps.shape)
    for num, t in enumerate(Temps):
        tmp = 0
        for i in np.arange(0,7):
            temp_es = g[i]*t**(i-2)
            tmp = tmp + temp_es
        es[num] = np.e**(tmp + g[7]*np.log(t))
    return es

def scatter_box(df,var1,var2,var_range,var_name,scatter_c,f_out):
    '''
    Create scatter plot between the two variables along with box and whisker plots
    
    Inputs:
    df : dataframe where data is stored
    var1 : dataframe column name of first variable to be plotted
    var2 : dataframe column name of second variable to be plotted
    var_range : list or tuple of the limits for the scatter and box plots
    scatter_c : color of scatter plot
    f_out : name of figure file
    '''
    
    fig = plt.figure(figsize=(10,6))
    gs = gridspec.GridSpec(1,5)
    ax1 = fig.add_subplot(gs[0:3])
    ax2 = fig.add_subplot(gs[3:5])

    #Scatter plots
    ax1.scatter(df[var1],df[var2],color=scatter_c,alpha=.8)
    ax1.set_ylim(var_range[0],var_range[1])
    ax1.set_xlim(var_range[0],var_range[1])
    ax1.set_xlabel(var_name+', Psychrometer',fontsize='large')
    ax1.set_ylabel(var_name+', Temp/RH Probe',fontsize='large')
    

    labels_t = ['Psychrometric','Temp/RH Probe']
    
    #Box and whisker plots
    flierprops=dict(marker='D',markersize=1)
    medianprops=dict(linewidth=2.5,color='#000000')
    ax2.yaxis.tick_right()
    
    ax2.boxplot([df[var1],df[var2]], flierprops=flierprops, medianprops=medianprops, labels=labels_t)
    ax2.set_ylim(var_range[0],var_range[1])
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel(var_name,fontsize='large',rotation=270,va='baseline')
    fig.tight_layout()

    plt.savefig(f_out)

def main():
    
    #Read in data from csv file and convert temperature and RH to vapor pressure
    lab2_f = 'lab2.csv'
    lab2 = pd.read_csv(lab2_f,skiprows=[0,2,3],header=0,parse_dates=[0],na_values = 'NAN')
    lab2['e_ee08'] = (Wexler_es(lab2['EE08_T_Avg']+273.15)*(lab2['EE08_RH_Avg']/100))/1000
    lab2['pwv_ee08'] = (2170*lab2['e_ee08'])/(lab2['EE08_T_Avg']+273.15)
    
    #Printing statistics
    print(lab2.corr()) #Select columns based on which correlations are needed
    print('Standard Deviations:', lab2.std())
    print('Means: ', lab2.mean())
    
    #Create plots for temperature, RH, and absolute humidity
    scatter_box(lab2,'TC_1_Avg','EE08_T_Avg',[20.5,21.1],var_name='Temperature [$^\circ$C]',
                scatter_c='C3',f_out='t_scatter.png')
    
    scatter_box(lab2,'RH_Avg','EE08_RH_Avg',[40.5,43],var_name='RH [%]',
                scatter_c='C0',f_out='rh_scatter.png')

    scatter_box(lab2,'abs_RH_Avg','pwv_ee08',[7.3,7.8],var_name=r'Abs. Humidity [$\frac{g}{m^{3}}$]',
                scatter_c='C1',f_out='abs_scatter.png')

if __name__ == '__main__':
    main()
