# -*- coding: utf-8 -*-
import scipy.signal
from numpy import *
import numpy
import time, sys

sys.path.append('../../util')
sys.path.append('../..')
from nidaq import NiDAQ
from pyqtgraph.graphicsWindows import *
from pyqtgraph.functions import mkPen
pw = PlotWindow()


time.clock()
sr = 100000
dur = 2.0

data = zeros(int(sr*dur))
xVals = linspace(0, dur, len(data))

data += random.normal(size=len(data)) + 20.
data[100000:300000] += 20
data[300000:500000] += 30
data[200000]+= 1000
data += sin(xVals*40677*2.0*pi)*4.
#data = sin(linspace(0, dur, sr*dur)* linspace(0, sr*2, sr*dur))

methods = ['subsample', 'mean', 'fourier', 'bessel_mean', 'butterworth_mean']

colors = [mkColor((255,0,0)), mkColor((0,255,0)), mkColor((0,0,255)), mkColor((255,0,255)), mkColor((255,255,0))]
def run(ds):
    pw.plot(data, clear=True)
    for m, c in zip(methods, colors):
        d1 = data.copy()
        t = time.clock()
        d2 = NiDAQ.downsample(d1, ds, method=m)
        print "Method %d: %f" % (i, time.clock()-t)
        p = pw.plot(d2, linspace(0, len(d2)*ds, len(d2)), pen=mkPen(c))
        p.setZValue(10000)
        #pw.plot(d2, pen=mkPen(colors[i-1]))
    
def showDownsample(**kwargs):
    d1 = data.copy()
    d2 = NiDAQ.downsample(**kwargs)
    pw.plot(data, xVals, clear=True)
    pw.plot(data2, xVals, pen=mkPen((255, 0, 0)))
    


def showTransfer(**kwargs):
    sampr = 50000
    xVals = linspace(0, dur, sampr*dur)
    #data = sin(xVals* linspace(0, sampr*2, sampr*dur))
    data = random.normal(size=sampr*dur)
    
    data2 = NiDAQ.lowpass(data, **kwargs)

    pw.plot(data, xVals, clear=True)
    pw.plot(data2, xVals, pen=mkPen((255, 0, 0)))
    
    
    




#def downsample(data, ds, method=1):
    #if method == 1:
        ## Method 1:
        ## decimate by averaging points together (does not remove HF noise, just folds it down.)
        #newLen = int(data.shape[0] / ds) * ds
        #data = data[:newLen]
        #data.shape = (data.shape[0]/ds, ds)
        #data = data.mean(axis=1)
      
    #elif method == 2:
        ## Method 2:
        ## Decimate using fourier resampling -- causes ringing artifacts.
        #newLen = int(data.shape[0] / ds)
        #data = scipy.signal.resample(data, newLen, window=8) # Use a kaiser window with beta=8
   
    #elif method == 3:
        ## Method 3: 
        ## Decimate by lowpass filtering, then average points together. (slow, artifacts at beginning and end of traces)
        ## Not as good as signal.resample for removing HF noise, but does not generate artifacts either.
        
        ## worst at removing HF noise (??)
        #b,a = scipy.signal.bessel(8, 1.0/ds, btype='low') 
        #base = data.mean()
        #data = scipy.signal.lfilter(b, a, data-base) + base
        
        #newLen = int(data.shape[0] / ds) * ds
        #data = data[:newLen]
        #data.shape = (data.shape[0]/ds, ds)
        #data = data.mean(axis=1)
      
    #elif method == 4:
        ##Method 4:
        ### Pad data, forward+reverse bessel filter, then average down
        #b,a = scipy.signal.bessel(4, 1.0/ds, btype='low') 
        #padded = numpy.hstack([data[:100], data, data[-100:]])   ## can we intelligently decide how many samples to pad with?
        #data = scipy.signal.lfilter(b, a, scipy.signal.lfilter(b, a, padded)[::-1])[::-1][100:-100]  ## filter twice; once forward, once reversed. (This eliminates phase changes)
        ##data = scipy.signal.lfilter(b, a, padded)[100:-100]  ## filter twice; once forward, once reversed. (This eliminates phase changes)
     
        #newLen = int(data.shape[0] / ds) * ds
        #data = data[:newLen]
        #data.shape = (data.shape[0]/ds, ds)
        #data = data.mean(axis=1)
   
    #elif method == 5:
        ##Method 4:
        ### Pad data, forward+reverse butterworth filter, then average down
        
        #ord, Wn = scipy.signal.buttord(1.0/ds, 1.5/ds, 0.01, 0.99)
        #print "butt ord:", ord, Wn
        #b,a = scipy.signal.butter(ord, Wn, btype='low') 
        #padded = numpy.hstack([data[:100], data, data[-100:]])   ## can we intelligently decide how many samples to pad with?
        #data = scipy.signal.lfilter(b, a, scipy.signal.lfilter(b, a, padded)[::-1])[::-1][100:-100]  ## filter twice; once forward, once reversed. (This eliminates phase changes)
        ##data = scipy.signal.lfilter(b, a, padded)[100:-100]  ## filter twice; once forward, once reversed. (This eliminates phase changes)
     
        #newLen = int(data.shape[0] / ds) * ds
        #data = data[:newLen]
        #data.shape = (data.shape[0]/ds, ds)
        #data = data.mean(axis=1)
        
    #return data

