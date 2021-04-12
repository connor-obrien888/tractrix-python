# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:04:35 2020

    Library with a convenient implementation of the tractrix magnetopause
    model from O'Brien et al. (2021). More information can be found on my 
    Github at the URL https://github.com/connor-obrien888/tractrix

@author: connor o'brien
"""

import numpy as np

__all__ = ["tractrix", "sine_rectifier"]


def tractrix(sin_rec, p_dyn, n = 1000, 
             s_param = np.asarray([14.56,-0.0354,5.697]), 
             w_param = np.asarray([32.31,-0.265,11.80])):
    """
    Calculate a set of n points in GSE X and Y representing the predicted 
    magnetopause surface in 2D from the IMF sine rectifier sin_rec and
    the solar wind dynamic pressure p_dyn. If multiple sets of solar wind
    conditions are provided, a surface is calculated for each set.

    Parameters
    ----------
    sin_rec : float or array_like[ndim,]
        The sine rectifier of the IMF in nT given by 
        Btot * sin^2(clock angle/2). This can be a 1-dimensional array. A
        handy function to calculate this quantity from the three IMF
        components is given as sine_rectifier in this package.

    p_dyn : float or array_like[ndim,]
        The solar wind dynaimc pressure in units of nPa. This can be a single
        float or a 1-dimensional array.

    n : int
        The number of points that will be generated in each surface.

    s_param : array_like[3,]
        The three tuning parameters used in the subsolar standoff position
        function. Default values from O'Brien et al. (2021).

    w_param : array_like[3,]
       The three tuning parameters used in the asymptotic tail width function.
       Default values from O'Brien et al. (2021).
       
    Returns
    -------
    x : array_like[ndim,n]
       Set of n points in GSE X for the ndim solar wind conditions describing
       the tractrix surface for each set of conditions. Returns NaN for any
       curves where w < 0.
    
    y : array_like[ndim,n]
       Set of n points in GSE Y for the ndim solar wind conditions describing
       the tractrix surface for each set of conditions. Returns NaN for any
       curves where w < 0.
       
    """
    s = (s_param[0] + s_param[1] * sin_rec) * (p_dyn ** (-1 / s_param[2]))
    w = (w_param[0] + w_param[1] * sin_rec) * (p_dyn ** (-1 / w_param[2]))
    try:
        w = np.array([np.nan if i < 0 else i for i in w])
    except TypeError:
        w = np.nan if w < 0 else w
    y = np.linspace(0,w,num=n+1)
    x = s - w * np.log((w + np.sqrt(np.abs(w ** 2 - (w - y[:-1]) ** 2))) / 
                       np.abs(w - y[:-1])) + np.sqrt(np.abs(w**2 - (w - y[:-1]
                                                                    ) ** 2))
    return x, y[:-1]
    
    
    
def sine_rectifier(bx, by, bz):
    """
    Calculate the sine rectifier of the IMF in nT given its three components
    in GSE coordinates and nT.

    Parameters
    ----------
    bx : float or array_like[ndim,]
        The GSE X component of the IMF in nT. This can be a 1-dimensional 
        array.

    by : float or array_like[ndim,]
        The GSE Y component of the IMF in nT. This can be a 1-dimensional 
        array.

    bz : float or array_like[ndim,]
        The GSE Z component of the IMF in nT. This can be a 1-dimensional 
        array.

    Returns
    -------
    sin_rec : array_like[ndim,]
       Sine rectifier of the IMF in nT for the ndim provided solar wind 
       components. 
    """
    sin_rec = np.sqrt(bx**2+by**2+bz**2)*(np.sin(np.arctan2(by,bz)/2)**2)
    return sin_rec