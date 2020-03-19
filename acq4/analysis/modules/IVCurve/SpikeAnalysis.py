"""
Analyze spike shapes - pulled out of IVCurve 2/6/2016 pbm.
Allows routine to be used to analyze spike trains independent of acq4's data models.
Create instance, then call setup to define the "Clamps" object and the spike threshold. 
The Clamps object must have the following variables defined:

    commandLevels (current injection levels, list)
    time_base (np.array of times corresponding to traces)
    data_mode (string, indicating current or voltgae clamp)
    tstart (time for start of looking at spikes; ms)
    tend (time to stop looking at spikes; ms)
    trace (the data trace itself, numpy array records x points)
    sample_interval (time between samples, sec)
    values (command waveforms; why it is called this in acq4 is a mystery)

Note that most of the results from this module are accessed either 
as class variables, or through the class variable analysis_summary,
a dictionary with key analysis results. 
IVCurve uses the analysis_summary to post results to an sql database.

Paul B. Manis, Ph.D. 2016-2017
for Acq4.

"""

from collections import OrderedDict
import os
import os.path
import pprint
import time
import itertools
import functools
import numpy as np
import scipy

import acq4.pyqtgraph as pg
from acq4.pyqtgraph.Qt import QtGui, QtCore
import acq4.analysis.tools.Utility as Utility  # pbm's utilities...
import acq4.analysis.tools.Fitting as Fitting  # pbm's fitting stuff...


class SpikeAnalysis:
    def __init__(self):
        pass
        self.threshold = 0.0
        self.Clamps = None
        self.analysis_summary = {}
        self.verbose = False
        self.FIGrowth = (
            1  # use function FIGrowth1 (can use simpler version FIGrowth 2 also)
        )

    def setup(self, clamps=None, threshold=None, verbose=False):
        """
        configure the inputs to the SpikeAnalysis class
        
        Paramters
        ---------
        clamps : class (default: None)
            PatchEphys clamp data holding/accessing all ephys data for this analysis
        
        threshold : float (default: None)
            Voltage threshold for spike detection
        
        verbose : boolean (default: False)
            Set true to get lots of print out while running - used
            mostly for debugging.
        """

        if clamps is None or threshold is None:
            raise ValueError("Spike Analysis requires defined clamps and threshold")
        self.Clamps = clamps
        self.threshold = threshold
        self.verbose = verbose

    def analyzeSpikes(self):
        """
        analyzeSpikes: Using the threshold set in the control panel, count the
        number of spikes in the stimulation window (self.Clamps.tstart, self.Clamps.tend)
        Updates the spike plot(s).

        The following class variables are modified upon successful analysis and return:
        self.spikecount: a 1-D numpy array of spike counts, aligned with the
            current (command)
        self.adapt_ratio: the adaptation ratio of the spike train
        self.fsl: a numpy array of first spike latency for each command level
        self.fisi: a numpy array of first interspike intervals for each
            command level
        self.nospk: the indices of command levels where no spike was detected
        self.spk: the indices of command levels were at least one spike
            was detected
        self.analysis_summary : Dictionary of results.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing, but see the list of class variables that are modified
        
        """
        twin = self.Clamps.tend - self.Clamps.tstart  # measurements window in seconds
        maxspkrate = 50  # max rate to count  in adaptation is 50 spikes/second
        minspk = 4
        maxspk = int(maxspkrate * twin)  # scale max dount by range of spike counts

        ntr = len(self.Clamps.traces)
        self.spikecount = np.zeros(ntr)
        self.fsl = np.zeros(ntr)
        self.fisi = np.zeros(ntr)
        ar = np.zeros(ntr)
        self.allisi = {}
        self.spikes = [[] for i in range(ntr)]
        self.spikeIndices = [[] for i in range(ntr)]
        # print 'clamp start/end: ', self.Clamps.tstart, self.Clamps.tend
        lastspikecount = 0
        for i in range(ntr):
            (spikes, spkx) = Utility.findspikes(
                self.Clamps.time_base,
                self.Clamps.traces[i],
                self.threshold,
                t0=self.Clamps.tstart,
                t1=self.Clamps.tend,
                dt=self.Clamps.sample_interval,
                mode="peak",  # best to use peak for detection
                interpolate=False,
                debug=False,
            )
            if len(spikes) == 0:
                # print 'no spikes found'
                continue
            self.spikes[i] = spikes
            # print 'found %d spikes in trace %d' % (len(spikes), i)
            self.spikeIndices[i] = [
                np.argmin(np.fabs(self.Clamps.time_base - t)) for t in spikes
            ]
            self.spikecount[i] = len(spikes)
            self.fsl[i] = (spikes[0] - self.Clamps.tstart) * 1e3
            if len(spikes) > 1:
                self.fisi[i] = (spikes[1] - spikes[0]) * 1e3  # first ISI
                self.allisi[i] = np.diff(spikes) * 1e3
            # for Adaptation ratio analysis: limit spike rate, and also only on monotonic increase in rate
            if (minspk <= len(spikes) <= maxspk) and (
                self.spikecount[i] > lastspikecount
            ):
                misi = np.mean(np.diff(spikes[-3:])) * 1e3  # late ISIs
                ar[i] = misi / self.fisi[i]
                lastspikecount = self.spikecount[i]  # update rate (sets max rate)

        iAR = np.where(ar > 0)  # valid AR and monotonically rising
        self.adapt_ratio = np.mean(ar[iAR])  # only where we made the measurement
        self.ar = ar  # stores all the ar values
        self.analysis_summary["AdaptRatio"] = self.adapt_ratio
        self.nospk = np.where(self.spikecount == 0)
        self.spk = np.where(self.spikecount > 0)[0]
        self.analysis_summary["FI_Curve"] = np.array(
            [self.Clamps.values, self.spikecount]
        )
        self.analysis_summary["FiringRate"] = np.max(self.spikecount) / (
            self.Clamps.tend - self.Clamps.tstart
        )
        #        print self.analysis_summary['FI_Curve']
        self.spikes_counted = True

    #        self.update_SpikePlots()

    def _timeindex(self, t):
        """
        Find the index into the time_base of the Clamps structure that 
        corresponds to the time closest to t
        
        Parameters
        ----------
        t : float (time, no default)
        
        Returns
        -------
        index : int (index to the closest time)
        """
        return np.argmin(self.Clamps.time_base - t)

    def analyzeSpikeShape(self, printSpikeInfo=False, begin_dV=12.0):
        """analyze the spike shape.
        Based on the analysis from Druckman et al. Cerebral Cortex, 2013
        
        The results of the analysis are stored in the SpikeAnalysis object
        as SpikeAnalysis.analysis_summary, a dictionary with specific keys.
        
        Every spike is measured, and a number of points on the waveform
            are defined for each spike, including the peak, the half-width
            on the rising phase, half-width on the falling phase, the
            peak of the AHP, the peak-trough time (AP peak to AHP peak),
            and a beginning, based on the slope (set in begin_dV)
        
        Parameters
        ----------
        printSpikeInfo : Boolean (default: Fase)
            Flag; when set prints arrays, etc, for debugging purposes
        
        begin_dV : float (default: 12 mV/ms)
            Slope used to define onset of the spike. The default value
            is from Druckmann et al; change this at your own peril!
        
        Returns
        -------
        Nothing (but see doc notes above)
        """

        ntr = len(self.Clamps.traces)
        #        print 'analyzespikeshape, self.spk: ', self.spk
        self.spikeShape = OrderedDict()
        rmp = np.zeros(ntr)
        iHold = np.zeros(ntr)
        for i in range(ntr):
            if len(self.spikes[i]) == 0:
                continue
            trspikes = OrderedDict()
            if printSpikeInfo:
                print(np.array(self.Clamps.values))
                print(len(self.Clamps.traces))
            (rmp[i], r2) = Utility.measure(
                "mean",
                self.Clamps.time_base,
                self.Clamps.traces[i],
                0.0,
                self.Clamps.tstart,
            )
            (iHold[i], r2) = Utility.measure(
                "mean",
                self.Clamps.time_base,
                self.Clamps.cmd_wave[i],
                0.0,
                self.Clamps.tstart,
            )
            for j in range(len(self.spikes[i])):
                thisspike = {
                    "trace": i,
                    "AP_number": j,
                    "AP_beginIndex": None,
                    "AP_endIndex": None,
                    "peakIndex": None,
                    "peak_T": None,
                    "peak_V": None,
                    "AP_Latency": None,
                    "AP_beginV": None,
                    "halfwidth": None,
                    "trough_T": None,
                    "trough_V": None,
                    "peaktotroughT": None,
                    "current": None,
                    "iHold": None,
                    "pulseDuration": None,
                    "tstart": self.Clamps.tstart,
                }  # initialize the structure
                thisspike["current"] = self.Clamps.values[i] - iHold[i]
                thisspike["iHold"] = iHold[i]
                thisspike["pulseDuration"] = (
                    self.Clamps.tend - self.Clamps.tstart
                )  # in seconds
                thisspike["peakIndex"] = self.spikeIndices[i][j]
                thisspike["peak_T"] = self.Clamps.time_base[thisspike["peakIndex"]]
                thisspike["peak_V"] = self.Clamps.traces[i][
                    thisspike["peakIndex"]
                ]  # max voltage of spike
                thisspike["tstart"] = self.Clamps.tstart

                # find the minimum going forward - that is AHP min
                dt = self.Clamps.time_base[1] - self.Clamps.time_base[0]
                dv = np.diff(self.Clamps.traces[i]) / dt
                k = self.spikeIndices[i][j] + 1
                if (
                    j < self.spikecount[i] - 1
                ):  # find end of spike (top of next, or end of trace)
                    kend = self.spikeIndices[i][j + 1]
                else:
                    kend = len(self.Clamps.traces[i])
                try:
                    km = (
                        np.argmin(dv[k:kend]) + k
                    )  # find fastst falling point, use that for start of detection
                except:
                    continue
                #                v = self.Clamps.traces[i][km]
                #                vlast = self.Clamps.traces[i][km]
                # kmin = np.argmin(np.argmin(dv2[k:kend])) + k  # np.argmin(np.fabs(self.Clamps.traces[i][k:kend]))+k
                kmin = np.argmin(self.Clamps.traces[i][km:kend]) + km
                thisspike["AP_endIndex"] = kmin
                thisspike["trough_T"] = self.Clamps.time_base[thisspike["AP_endIndex"]]
                thisspike["trough_V"] = self.Clamps.traces[i][kmin]

                if thisspike["AP_endIndex"] is not None:
                    thisspike["peaktotrough"] = (
                        thisspike["trough_T"] - thisspike["peak_T"]
                    )
                k = self.spikeIndices[i][j] - 1
                if j > 0:
                    kbegin = self.spikeIndices[i][
                        j - 1
                    ]  # trspikes[j-1]['AP_endIndex']  # self.spikeIndices[i][j-1]  # index to previ spike start
                else:
                    kbegin = k - int(0.002 / dt)  # for first spike - 4 msec prior only
                    if kbegin * dt <= self.Clamps.tstart:
                        kbegin = kbegin + int(0.0002 / dt)  # 1 msec
                # revise k to start at max of rising phase
                try:
                    km = np.argmax(dv[kbegin:k]) + kbegin
                except:
                    continue
                if km - kbegin < 1:
                    km = kbegin + int((k - kbegin) / 2.0) + 1
                kthresh = (
                    np.argmin(np.fabs(dv[kbegin:km] - begin_dV)) + kbegin
                )  # point where slope is closest to begin
                thisspike["AP_beginIndex"] = kthresh
                thisspike["AP_Latency"] = self.Clamps.time_base[kthresh]
                thisspike["AP_beginV"] = self.Clamps.traces[i][
                    thisspike["AP_beginIndex"]
                ]
                if (
                    thisspike["AP_beginIndex"] is not None
                    and thisspike["AP_endIndex"] is not None
                ):
                    halfv = 0.5 * (thisspike["peak_V"] + thisspike["AP_beginV"])
                    kup = np.argmin(
                        np.fabs(
                            self.Clamps.traces[i][
                                thisspike["AP_beginIndex"] : thisspike["peakIndex"]
                            ]
                            - halfv
                        )
                    )
                    kup += thisspike["AP_beginIndex"]
                    kdown = np.argmin(
                        np.fabs(
                            self.Clamps.traces[i][
                                thisspike["peakIndex"] : thisspike["AP_endIndex"]
                            ]
                            - halfv
                        )
                    )
                    kdown += thisspike["peakIndex"]
                    if kup is not None and kdown is not None:
                        thisspike["halfwidth"] = (
                            self.Clamps.time_base[kdown] - self.Clamps.time_base[kup]
                        )
                        thisspike["hw_up"] = self.Clamps.time_base[kup]
                        thisspike["hw_down"] = self.Clamps.time_base[kdown]
                        thisspike["hw_v"] = halfv
                trspikes[j] = thisspike
            self.spikeShape[i] = trspikes
        if printSpikeInfo:
            pp = pprint.PrettyPrinter(indent=4)
            for m in sorted(self.spikeShape.keys()):
                print(
                    "----\nTrace: %d  has %d APs"
                    % (m, len(list(self.spikeShape[m].keys())))
                )
                for n in sorted(self.spikeShape[m].keys()):
                    pp.pprint(self.spikeShape[m][n])
        self.iHold = np.mean(iHold)
        self.analysis_summary[
            "spikes"
        ] = self.spikeShape  # save in the summary dictionary too
        self.analysis_summary["iHold"] = np.mean(iHold)
        self.analysis_summary["pulseDuration"] = self.Clamps.tend - self.Clamps.tstart
        self.getClassifyingInfo()  # build analysis summary here as well.

    def getIVCurrentThresholds(self):
        """ figure out "threshold" for spike, get 150% and 300% points.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        tuple: (int, int)
            The tuple contains the index to command threshold for spikes, and 150% of that threshold
            The indices are computed to be as close to the command step values
            that are actually used (so, the threshold is absolute; the 150%
            value will be the closest estimate given the step sizes used to
            collect the data)
        """
        nsp = []
        icmd = []
        for m in sorted(self.spikeShape.keys()):
            n = len(list(self.spikeShape[m].keys()))  # number of spikes in the trace
            if n > 0:
                nsp.append(len(list(self.spikeShape[m].keys())))
                icmd.append(self.spikeShape[m][0]["current"])
        try:
            iamin = np.argmin(icmd)
        except:
            raise ValueError(
                "IVCurve:SpikeAnalysis:getIVCurrentThresholds - icmd seems to be ? : ", icmd
            )
        imin = np.min(icmd)
        ia150 = np.argmin(np.abs(1.5 * imin - np.array(icmd)))
        iacmdthr = np.argmin(np.abs(imin - self.Clamps.values))
        ia150cmdthr = np.argmin(np.abs(icmd[ia150] - self.Clamps.values))
        # print 'thr indices and values: ', iacmdthr, ia150cmdthr, self.Clamps.values[iacmdthr], self.Clamps.values[ia150cmdthr]
        return (
            iacmdthr,
            ia150cmdthr,
        )  # return threshold indices into self.Clamps.values array at threshold and 150% point

    def getClassifyingInfo(self):
        """
        Adds the classifying information according to Druckmann et al., Cerebral Cortex, 2013
        to the analysis summary
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        
        Modifies the class analysis_summary dictionary to contain a number of results
        regarding the AP train, including the first and second spike latency,
        the first and second spike halfwidths, the firing rate at 150% of threshold,
        and the depth of the AHP
        """

        (
            jthr,
            j150,
        ) = (
            self.getIVCurrentThresholds()
        )  # get the indices for the traces we need to pull data from
        jthr = int(jthr)
        j150 = int(j150)
        if j150 not in list(self.spikeShape.keys()):
            return
        if jthr == j150 and self.verbose:
            # print '\n%s:' % self.filename
            print("Threshold current T and 1.5T the same: using next up value for j150")
            print("jthr, j150, len(spikeShape): ", jthr, j150, len(self.spikeShape))
            print("1 ", self.spikeShape[jthr][0]["current"] * 1e12)
            print("2 ", self.spikeShape[j150 + 1][0]["current"] * 1e12)
            print(
                " >> Threshold current: %8.3f   1.5T current: %8.3f, next up: %8.3f"
                % (
                    self.spikeShape[jthr][0]["current"] * 1e12,
                    self.spikeShape[j150][0]["current"] * 1e12,
                    self.spikeShape[j150 + 1][0]["current"] * 1e12,
                )
            )
            j150 = jthr + 1
        if (
            len(self.spikeShape[j150]) >= 1
            and self.spikeShape[j150][0]["halfwidth"] is not None
        ):
            self.analysis_summary["AP1_Latency"] = (
                self.spikeShape[j150][0]["AP_Latency"]
                - self.spikeShape[j150][0]["tstart"]
            ) * 1e3
            self.analysis_summary["AP1_HalfWidth"] = (
                self.spikeShape[j150][0]["halfwidth"] * 1e3
            )
        else:
            self.analysis_summary["AP1_Latency"] = np.inf
            self.analysis_summary["AP1_HalfWidth"] = np.inf
        if (
            len(self.spikeShape[j150]) >= 2
            and 1 in list(self.spikeShape[j150].keys())
            and self.spikeShape[j150][1]["halfwidth"] is not None
        ):
            self.analysis_summary["AP2_Latency"] = (
                self.spikeShape[j150][1]["AP_Latency"]
                - self.spikeShape[j150][1]["tstart"]
            ) * 1e3
            self.analysis_summary["AP2_HalfWidth"] = (
                self.spikeShape[j150][1]["halfwidth"] * 1e3
            )
        else:
            self.analysis_summary["AP2_Latency"] = np.inf
            self.analysis_summary["AP2_HalfWidth"] = np.inf

        rate = (
            len(self.spikeShape[j150]) / self.spikeShape[j150][0]["pulseDuration"]
        )  # spikes per second, normalized for pulse duration
        # first AHP depth
        # print 'j150: ', j150
        # print self.spikeShape[j150][0].keys()
        # print self.spikeShape[j150]
        AHPDepth = (
            self.spikeShape[j150][0]["AP_beginV"] - self.spikeShape[j150][0]["trough_V"]
        )
        self.analysis_summary["FiringRate_1p5T"] = rate
        self.analysis_summary["AHP_Depth"] = AHPDepth * 1e3  # convert to mV
        # pprint.pprint(self.analysis_summary)
        # except:
        #     raise ValueError ('Failed Classification for cell: %s' % self.filename)

    def fitOne(self, x, yd, info="", fixNonMonotonic=True, excludeNonMonotonic=False):
        """Fit the FI plot to an equation that is piecewise linear up to the threshold
            called Ibreak, then (1-exp(F/Frate)) for higher currents
        
        Parameters
        ---------- 
            x : numpy array (no default)
                The x data to fit (typically an array of current levels)
        
            yd : numpy array (no default)
                The y data to fit (typically an array of spike counts)
        
            info : string (default: '')
                information to add to a fitted plot
        
            fixNonMonotonic : Boolean (default: True)
                If True, only use data up to the maximal firing rate,
                discarding the remainder of the steps under the assumption
                that the cell is entering depolarization block.
        
            excludeNonMonotonic : Boolean (default: False)
                if True, does not even try to fit, and returns None
        
        Returns
        -------
        None if there is no fitting to be done (excluding non-monotonic or no spikes)
        tuple of (fpar, xf, yf, names, error, f, func)
            These are the fit parameters
        """
        #        print('fitone called')
        ymax = np.max(yd)
        if fixNonMonotonic and ymax > yd[-1]:  # clip at max firing rate
            imaxs = [
                i for i, y in enumerate(yd) if y == ymax
            ]  # handle duplicate firing rates
            imax = max(imaxs)  # find highest index
            dypos = list(range(0, imax + 1))
            x = x[dypos]
            yd = yd[dypos]
            ymax = np.max(yd)
        if np.max(x) < 0.0:  # skip if max rate is < 0 current
            return None
        ymin = 5.0
        if ymax < ymin:
            ymin = 0.0
        if ymax > yd[-1] and excludeNonMonotonic:
            nonmono += 1
            return None

        fpnt = np.where(yd > 0)  # find first point where cell fires
        fbr = fpnt[0][0] - 1
        ibreak0 = x[fbr]  # use point before first spike as the initial break point
        dx = np.abs(np.mean(np.diff(x)))  # get current steps
        xp = x[fpnt]
        xp = xp - ibreak0 - dx
        yp = yd[fpnt]  # save data with responses

        testMethod = "SLSQP"  #  'SLSQP'  # L-BFGS-B simplex, SLSQP, 'TNC', 'COBYLA'
        if fbr - 3 >= 0:  # set start and end of fit
            x0 = fbr - 3
        else:
            x0 = 0
        if fbr + 3 < len(x):
            x1 = fbr + 3
        else:
            x1 = len(x) - 1
        if self.FIGrowth == 1:
            #            print('exponential model fit')
            bounds = (
                (0.0, yp[0] + 40.0),
                np.sort([x[x0], x[x1]]),
                (0.0, 2),
                (0.0, ymax * 5.0),
                (0.00001, 100.0),
            )
            # # parameters for FIGrowth 1: ['Fzero', 'Ibreak', 'F1amp', 'F2amp', 'Irate']
            fitbreak0 = ibreak0
            if fitbreak0 > 0.0:
                fitbreak0 = 0.0
            ixb = np.argwhere(yd > 0)[0][0]
            #            print ('ixb: ', ixb)
            cons = (
                {"type": "eq", "fun": lambda xc: xc[0]},  # lock F0 at >= 0
                {
                    "type": "ineq",
                    "fun": lambda xc: xc[1] - x[ixb - 1],
                },  #  ibreak between last no spike and first spiking level
                {
                    "type": "ineq",
                    "fun": lambda xc: x[ixb] - xc[1],
                },  #  ibreak between last no spike and first spiking level
                {"type": "eq", "fun": lambda xc: xc[2]},  # F1amp >= 0
                {
                    "type": "ineq",
                    "fun": lambda xc: xc[3] - xc[2],
                },  # F2amp > F1amp (must be!)
                {"type": "ineq", "fun": lambda xc: xc[4]},
            )

            initpars = [0.0, ibreak0, 0.0, ymax / 2.0, 0.001]
            func = "FIGrowth1"
            f = Fitting.Fitting().fitfuncmap[func]
            # now fit the full data set
            (fpar, xf, yf, names) = Fitting.Fitting().FitRegion(
                np.array([1]),
                0,
                x,
                yd,
                t0=fitbreak0,
                t1=np.max(x[fpnt]),
                fitFunc=func,
                fitPars=initpars,
                bounds=bounds,
                constraints=cons,
                weights=None,  # np.sqrt,
                fixedPars=None,
                method=testMethod,
            )
            error = Fitting.Fitting().getFitErr()
            self.FIKeys = f[6]
            for i, k in enumerate(self.FIKeys):
                self.analysis_summary[k] = fpar[0][i]
        elif self.FIGrowth == 2:  # FIGrowth is 2, so use simpler fit
            #            print ('Fitting with 1 simple')
            bounds = (np.sort([x[x0], x[x1]]), (0.0, ymax * 5.0), (0.0001, 100.0))
            # # parameters for FIGrowth 2: ['Fzero', 'Ibreak', 'F1amp', 'F2amp', 'Irate']
            fitbreak0 = ibreak0
            if fitbreak0 > 0.0:
                fitbreak0 = 0.0
            initpars = [ibreak0, ymax / 2.0, 0.001]
            func = "FIGrowth2"
            f = Fitting.Fitting().fitfuncmap[func]
            # now fit the full data set
            (fpar, xf, yf, names) = Fitting.Fitting().FitRegion(
                np.array([1]),
                0,
                x,
                yd,
                t0=fitbreak0,
                t1=np.max(x[fpnt]),
                fitFunc=func,
                fitPars=initpars,
                bounds=bounds,
                fixedPars=None,
                method=testMethod,
            )
            error = Fitting.Fitting().getFitErr()
            self.FIKeys = f[6]
            imap = [-1, 0, -1, 1, 2]
            for i, k in enumerate(FIKeys):
                if imap[i] == -1:
                    self.analysis_summary[k] = 0.0
                else:
                    self.analysis_summary[k] = fpar[0][
                        imap[i]
                    ]  # translate in FIGrowth 2 style...
        elif self.FIGrowth == 3:  # use piecewise linear, 3 segment fit
            #            print ('Fitting with 3 segment line')
            # # parameters for pwl3 (piecewise linear...): ['Ibreak', 'Rate0', 'Ibreak1', 'Irate1', 'Irate2', 'Irate3']
            fitbreak0 = ibreak0
            if fitbreak0 > 0.0:
                fitbreak0 = 0.0
            x1 = np.argwhere(yd > 0.0)
            initpars = (x[x1[0] - 1], 0.0, x[x1[0]], 0.0, 0.01, 0.2)
            bounds = (
                (0.0, np.max(x)),  # Ibreak forced to first spike level almost
                (0.0, 0.0),  # Rate0 (y0)
                (0.0, np.max(x)),  # Ibreak1 (x1)  # spread it out?
                (0.0, 0.0),  # IRate1  (k1, k2, k3)
                (0.0, 1),  # IRate2
                (0.0, 1),  # Irate3
            )
            cons = (
                {"type": "ineq", "fun": lambda x: x[0]},
                {"type": "ineq", "fun": lambda x: x[1]},
                {
                    "type": "ineq",
                    "fun": lambda x: x[2] - [x[0] + 50.0],
                },  # ibreak1 > 100pA + ibreak0
                {"type": "ineq", "fun": lambda x: x[3]},
                {"type": "ineq", "fun": lambda x: x[4] - x[3]},
                {"type": "ineq", "fun": lambda x: x[4] * 0.5 - x[5]},
            )

            func = "pwl3"
            f = Fitting.Fitting().fitfuncmap[func]
            # now fit the full data set
            (fpar, xf, yf, names) = Fitting.Fitting().FitRegion(
                np.array([1]),
                0,
                x,
                yd,
                t0=fitbreak0,
                t1=np.max(x[fpnt]),
                fitFunc=func,
                fitPars=initpars,
                bounds=bounds,
                constraints=cons,
                fixedPars=None,
                method=testMethod,
            )
            error = Fitting.Fitting().getFitErr()
            self.FIKeys = f[6]
            # imap = [-1, 0, -1, 1, 2]
            for i, k in enumerate(self.FIKeys):
                self.analysis_summary[k] = fpar[0][
                    i
                ]  # translate in FIGrowth 2 style...
        elif self.FIGrowth == 5:
            #            print ('Fitting with sublinear power function FI')
            # # parameters for power (piecewise linear...): [c, s, 'd']
            # data oare only fit for the range over which the cell fires
            #
            fitbreak0 = ibreak0
            if fitbreak0 > 0.0:
                fitbreak0 = 0.0
            ix1 = np.argwhere(yd > 0.0)  # find first point with spikes
            x1 = x[ix1[0]][0]
            #            print ('x1: ', x1)
            initpars = (x1, 3.0, 0.5)  #
            bds = [(0.0, 500.0), (0.01, 100.0), (0.01, 1.0)]

            # cons = ( {'type': 'ineq', 'fun': lambda x:  x[0]},
            #           {'type': 'ineq', 'fun': lambda x: x[1]},
            #           {'type': 'ineq', 'fun': lambda x: x[2] - [x[0] + 50.]}, # ibreak1 > 100pA + ibreak0
            #           {'type': 'ineq', 'fun': lambda x: x[3]},
            #           {'type': 'ineq', 'fun': lambda x: x[4] - x[3]},
            #           {'type': 'ineq', 'fun': lambda x: x[4]*0.5 - x[5]},
            #      )
            #
            func = "FIPower"
            f = Fitting.Fitting().fitfuncmap[func]
            # now fit the full data set
            #            print('Xrange: ', np.min(x), np.max(x), x1, np.max(x[fpnt]))
            (fpar, xf, yf, names) = Fitting.Fitting().FitRegion(
                np.array([1]),
                0,
                x,
                yd,
                t0=fitbreak0,
                t1=np.max(x[fpnt]),
                fitFunc=func,
                fitPars=initpars,
                bounds=bds,
                constraints=None,
                fixedPars=None,
                method=testMethod,
            )
            error = Fitting.Fitting().getFitErr()
            self.FIKeys = f[6]
            # imap = [-1, 0, -1, 1, 2]
            #            print self.FIKeys
            for i, k in enumerate(self.FIKeys):
                self.analysis_summary[k] = fpar[0][
                    i
                ]  # translate in FIGrowth 2 style...
        else:
            raise ValueError(
                "SpikeAnalysis: FIGrowth value %d ot known" % self.FIGrowth
            )
        return (fpar, xf, yf, names, error, f, func)