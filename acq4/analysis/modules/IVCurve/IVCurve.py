# -*- coding: utf-8 -*-
"""
IVCurve: Analysis module that analyzes current-voltage and firing
relationships from current clamp data.
This is part of Acq4

Paul B. Manis, Ph.D.
2011-2013.

Pep8 compliant (via pep8.py) 10/25/2013
Refactoring begun 3/21/2015

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
from acq4.pyqtgraph.Qt import QtGui, QtCore, QAPP
from acq4.analysis.AnalysisModule import AnalysisModule

import acq4.util.matplotlibexporter as matplotlibexporter
import acq4.analysis.tools.Utility as Utility  # pbm's utilities...
import acq4.analysis.tools.Fitting as Fitting  # pbm's fitting stuff...
import acq4.analysis.tools.ScriptProcessor as ScriptProcessor
from . import ctrlTemplate
from . import SpikeAnalysis
from . import RmTauAnalysis

# noinspection PyPep8
class IVCurve(AnalysisModule):
    """
    IVCurve is an Analysis Module for Acq4.

    IVCurve performs analyses of current-voltage relationships in
    electrophysiology experiments. The module is interactive, and is primarily
    designed to allow a preliminary examination of data collected in current clamp and voltage clamp.
    Results analyzed include:
    Resting potential (average RMP through the episodes in the protocol).
    Input resistance (maximum slope if IV relationship below Vrest)
    Cell time constant (single exponential fit)
    Ih Sag amplitude and tau
    Spike rate as a function of injected current
    Interspike interval as a function of time for each current level
    RMP as a function of time through the protocol
    """

    def __init__(self, host):
        AnalysisModule.__init__(self, host)

        self.Clamps = (
            self.dataModel.GetClamps()
        )  # access the "GetClamps" class for reading data
        self.Clamps.time_base = None
        # data_template is a dictionary of describing how an analysis run will be printed to the terminal

        self.data_template = OrderedDict(
            [
                ("Species", (12, "{:>12s}", 1.0)),
                ("Age", (5, "{:>5s}", 1.0)),
                ("Sex", (3, "{:>3s}", 1.0)),
                ("Weight", (6, "{:>6s}", 1.0)),
                ("Temperature", (10, "{:>10s}", 1.0)),
                ("ElapsedTime", (11, "{:>11.2f}", 1.0)),
                ("RMP", (5, "{:>5.1f}", 1.0)),
                ("Rin", (5, "{:>5.1f}", 1.0)),
                ("Bridge", (5, "{:>5.1f}", 1.0)),
                ("tau", (5, "{:>6.2f}", 1.0)),
                ("AdaptRatio", (9, "{:>9.3f}", 1.0)),
                ("tauh", (5, "{:>5.1f}", 1.0)),
                ("Gh", (6, "{:>6.2f}", 1e9)),
                ("FiringRate_1p5T", (12, "{:>9.1f}", 1.0)),
                ("AP1_HalfWidth", (13, "{:>12.3f}", 1.0)),
                ("AP1_Latency", (11, "{:>9.3f}", 1.0)),
                ("AP2_HalfWidth", (13, "{:>12.3f}", 1.0)),
                ("AP2_Latency", (11, "{:>9.3f}", 1.0)),
                ("AHP_Depth", (9, "{:>9.2f}", 1.0)),
                ("Fzero", (9, "{:>9.2f}", 1.0)),
                ("Ibreak", (9, "{:>9.3f}", 1.0)),
                ("F1amp", (9, "{:>9.3f}", 1.0)),
                ("F2amp", (9, "{:>9.3f}", 1.0)),
                ("Irate", (12, "{:>12.6f}", 1.0)),
                ("Description", (11, "{:s}", 1.0)),
            ]
        )
        self.Script = ScriptProcessor.ScriptProcessor(host)
        self.Script.setAnalysis(
            analysis=self.updateAnalysis,
            fileloader=self.loadFileRequested,
            template=self.data_template,
            clamps=self.Clamps,
            printer=self.printAnalysis,
            dbupdate=self.dbStoreClicked,
        )  # specify the routines to be called and data sets to be used
        self.SA = (
            SpikeAnalysis.SpikeAnalysis()
        )  # create instances of our analysis routines
        self.RmTau = RmTauAnalysis.RmTauAnalysis()
        self.loaded = None
        self.filename = None
        self.dirsSet = None
        self.lrss_flag = True  # show is default
        self.lrpk_flag = True
        self.rmp_flag = True
        self.bridgeCorrection = None  # bridge  correction in Mohm.
        self.showFISI = (
            True  # show FISI or ISI as a function of spike number (when False)
        )
        self.lrtau_flag = False
        self.regions_exist = False
        self.tauh_fits = {}
        self.tauh_fitted = {}
        self.tau_fits = {}
        self.regions_exist = False
        self.regions = {}
        self.analysis_summary = (
            {}
        )  # dictionary of the results of various analyses. Used for sql database and printing
        self.tx = None
        self.keep_analysis_count = 0
        self.dataMarkers = []
        self.doUpdates = True
        self.colors = ["w", "g", "b", "r", "y", "c"]
        self.symbols = ["o", "s", "t", "d", "+"]
        self.color_list = itertools.cycle(self.colors)
        self.symbol_list = itertools.cycle(self.symbols)
        self.script_header = False
        self.Clamps.data_mode = "IC"  # analysis depends on the type of data we have.
        self.plot_list = []


        # --------------graphical elements-----------------
        self._sizeHint = (1280, 900)  # try to establish size of window
        self.ctrlWidget = QtGui.QWidget()
        self.ctrl = ctrlTemplate.Ui_Form()
        self.ctrl.setupUi(self.ctrlWidget)
        self.main_layout = pg.GraphicsView()  # instead of GraphicsScene?
        # make fixed widget for the module output
        self.widget = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout()
        self.widget.setLayout(self.gridLayout)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(1)
        # Setup basic GUI
        self._elements_ = OrderedDict(
            [
                ("File Loader", {"type": "fileInput", "size": (170, 50), "host": self}),
                (
                    "Parameters",
                    {
                        "type": "ctrl",
                        "object": self.ctrlWidget,
                        "host": self,
                        "size": (160, 700),
                    },
                ),
                (
                    "Plots",
                    {
                        "type": "ctrl",
                        "object": self.widget,
                        "pos": ("right",),
                        "size": (400, 700),
                    },
                ),
            ]
        )
        self.initializeElements()
        self.file_loader_instance = self.getElement("File Loader", create=True)
        # grab input form the "Ctrl" window
        self.ctrl.IVCurve_Update.clicked.connect(self.updateAnalysis)
        self.ctrl.IVCurve_PrintResults.clicked.connect(
            functools.partial(self.printAnalysis, printnow=True, script_header=True)
        )

        if not matplotlibexporter.HAVE_MPL:
            self.ctrl.IVCurve_MPLExport.setEnabled = False  # make button inactive
        #        self.ctrl.IVCurve_MPLExport.clicked.connect(self.matplotlibExport)
        else:
            self.ctrl.IVCurve_MPLExport.clicked.connect(self.to_mpl)
            # self.ctrl.IVCurve_MPLExport.clicked.connect(
            #     functools.partial(matplotlibexporter.matplotlibExport, gridlayout=self.gridLayout,
            #                       title=self.filename))
        self.ctrl.IVCurve_KeepAnalysis.clicked.connect(self.resetKeepAnalysis)
        self.ctrl.IVCurve_getFileInfo.clicked.connect(self.get_file_information)
        [
            self.ctrl.IVCurve_RMPMode.currentIndexChanged.connect(x)
            for x in [self.update_rmpAnalysis, self.analyzeSpikes]
        ]
        self.ctrl.IVCurve_FISI_ISI_button.clicked.connect(self.displayFISI_ISI)
        self.ctrl.dbStoreBtn.clicked.connect(self.dbStoreClicked)
        self.ctrl.IVCurve_OpenScript_Btn.clicked.connect(self.read_script)
        self.ctrl.IVCurve_RunScript_Btn.clicked.connect(self.rerun_script)
        self.ctrl.IVCurve_PrintScript_Btn.clicked.connect(
            self.Script.print_script_output
        )
        # self.scripts_form.PSPReversal_ScriptCopy_Btn.clicked.connect(self.copy_script_output)
        # self.scripts_form.PSPReversal_ScriptFormatted_Btn.clicked.connect(self.print_formatted_script_output)
        self.ctrl.IVCurve_ScriptName.setText("None")
        self.layout = self.getElement("Plots", create=True)

        # instantiate the graphs using a gridLayout (also facilitates matplotlib export; see export routine below)
        self.data_plot = pg.PlotWidget()
        self.gridLayout.addWidget(self.data_plot, 0, 0, 3, 1)
        self.label_up(self.data_plot, "T (s)", "V (V)", "Data")

        self.cmd_plot = pg.PlotWidget()
        self.gridLayout.addWidget(self.cmd_plot, 3, 0, 1, 1)
        self.label_up(self.cmd_plot, "T (s)", "I (A)", "Command")

        self.RMP_plot = pg.PlotWidget()
        self.gridLayout.addWidget(self.RMP_plot, 1, 1, 1, 1)
        self.label_up(self.RMP_plot, "T (s)", "V (mV)", "RMP")

        self.fiPlot = pg.PlotWidget()
        self.gridLayout.addWidget(self.fiPlot, 2, 1, 1, 1)
        self.label_up(self.fiPlot, "I (pA)", "Spikes (#)", "F-I")

        self.fslPlot = pg.PlotWidget()
        self.gridLayout.addWidget(self.fslPlot, 3, 1, 1, 1)
        self.label_up(self.fslPlot, "I (pA)", "Fsl/Fisi (ms)", "FSL/FISI")

        self.IV_plot = pg.PlotWidget()
        self.gridLayout.addWidget(self.IV_plot, 0, 1, 1, 1)
        self.label_up(self.IV_plot, "I (pA)", "V (V)", "I-V")
        for row, s in enumerate([20, 10, 10, 10]):
            self.gridLayout.setRowStretch(row, s)

            #    self.tailPlot = pg.PlotWidget()
            #    self.gridLayout.addWidget(self.fslPlot, 3, 1, 1, 1)
            #    self.label_up(self.tailPlot, 'V (V)', 'I (A)', 'Tail Current')

            # Add a color scale
        self.color_scale = pg.GradientLegend((20, 150), (-10, -10))
        self.data_plot.scene().addItem(self.color_scale)
        self.ctrl.IVCurve_Reset.clicked.connect(
            functools.partial(self.initialize_regions, reset=True)
        )
        self.ctrl.IVCurve_RMPMode.setCurrentIndex(
            1
        )  # put in IV mode with current axis.
        self.AllPlots = [self.data_plot, self.cmd_plot, 
                        self.fiPlot, self.fslPlot, self.IV_plot, self.RMP_plot]
        self.clear_results()

    def clear_results(self):
        """
        Clear results resets variables.
        This is typically required *every* time a new data set is loaded.
        
        Parameters
        ----------
        None
        
        Returns
        ------
        Nothing. 
        
        Many class variables are reinitialized by calling the routine.
        """

        for p in self.AllPlots:
            p.clearPlots()

        self.filename = ""
        self.r_in = 0.0
        self.tau = 0.0
        self.adapt_ratio = 0.0
        self.spikes_counted = False
        self.nospk = []
        self.spk = []
        self.Sequence = ""
        self.ivss = []  # steady-state IV (window 2)
        self.ivss_cmd = []
        self.ivpk = []  # peak IV (window 1)
        self.fsl = []  # first spike latency
        self.fisi = []  # first isi
        self.rmp = []  # resting membrane potential during sequence
        self.analysis_summary = {}
        self.script_header = True


    def resetKeepAnalysis(self):
        """
        Simply reset the counter for keeping analyses...
        Parameters: None
        Returns: Nothing
        """
        self.keep_analysis_count = 0  # reset counter.

    def show_or_hide(self, lrregion="", forcestate=None):
        """
        Show or hide specific regions in the display
        
        Parameters
        ----------
        lrregion : string (default: '')
            name of the region('lrwin0', etc)
        
        forcestate : None or Boolean (default: None)
            Set True to force the show status, False to Hide. 
            If forcestate is None, then uses the region's 'shstate' value 
            to set the state.
        
        Returns
        -------
        Nothing
        
        """
        if lrregion == "":
            print(("PSPReversal:show_or_hide:: lrregion is {:<s}".format(lrregion)))
            return
        region = self.regions[lrregion]
        if forcestate is not None:
            if forcestate:
                region["region"].show()
                region["state"].setChecked(QtCore.Qt.Checked)
                region["shstate"] = True
            else:
                region["region"].hide()
                region["state"].setChecked(QtCore.Qt.Unchecked)
                region["shstate"] = False
        else:
            if not region["shstate"]:
                region["region"].show()
                region["state"].setChecked(QtCore.Qt.Checked)
                region["shstate"] = True
            else:
                region["region"].hide()
                region["state"].setChecked(QtCore.Qt.Unchecked)
                region["shstate"] = False

    def displayFISI_ISI(self):
        """
        Control display of first interspike interval/first spike latency
        versus ISI over time.
        """
        if self.showFISI:  # currently showin FISI/FSL; switch to ISI over time
            self.showFISI = False
        else:
            self.showFISI = True
        self.update_SpikePlots()

    def initialize_regions(self, reset=False):
        """
        initialize_regions sets the linear regions on the displayed data

        Here we create the analysis regions in the plot. However, this should
        NOT happen until the plot has been created
        Note the the information about each region is held in a dictionary,
        which for each region has a dictionary that accesses the UI and class
        methods for that region. This later simplifies the code and reduces
        repetitive sections.
        
        Parameters
        ----------
        reset : Boolean (default: False)
            forces a reset of the region positions after they have been moved
            (does not recreate them)
        
        Returns
        -------
        Nothing (but rests/initializes internal state of many variables)
        """
        # hold all the linear regions in a dictionary
        if not self.regions_exist:
            self.regions["lrleak"] = {
                "name": "leak",  # use a "leak" window
                "region": pg.LinearRegionItem(
                    [0, 1],
                    orientation=pg.LinearRegionItem.Horizontal,
                    brush=pg.mkBrush(255, 255, 0, 50.0),
                ),
                "plot": self.cmd_plot,
                "state": self.ctrl.IVCurve_subLeak,
                "shstate": False,  # keep internal copy of the state
                "mode": self.ctrl.IVCurve_subLeak.isChecked(),
                "start": self.ctrl.IVCurve_LeakMin,
                "stop": self.ctrl.IVCurve_LeakMax,
                "updater": self.updateAnalysis,
                "units": "pA",
            }
            self.ctrl.IVCurve_subLeak.region = self.regions["lrleak"][
                "region"
            ]  # save region with checkbox
            self.regions["lrwin0"] = {
                "name": "win0",  # peak window
                "region": pg.LinearRegionItem(
                    [0, 1], brush=pg.mkBrush(128, 128, 128, 50.0)
                ),
                "plot": self.data_plot,
                "state": self.ctrl.IVCurve_showHide_lrpk,
                "shstate": True,  # keep internal copy of the state
                "mode": None,
                "start": self.ctrl.IVCurve_pkTStart,
                "stop": self.ctrl.IVCurve_pkTStop,
                "updater": self.updateAnalysis,
                "units": "ms",
            }
            self.ctrl.IVCurve_showHide_lrpk.region = self.regions["lrwin0"][
                "region"
            ]  # save region with checkbox
            self.regions["lrwin1"] = {
                "name": "win2",  # ss window
                "region": pg.LinearRegionItem(
                    [0, 1], brush=pg.mkBrush(0, 0, 255, 50.0)
                ),
                "plot": self.data_plot,
                "state": self.ctrl.IVCurve_showHide_lrss,
                "shstate": True,  # keep internal copy of the state
                "mode": None,
                "start": self.ctrl.IVCurve_ssTStart,
                "stop": self.ctrl.IVCurve_ssTStop,
                "updater": self.updateAnalysis,
                "units": "ms",
            }
            self.ctrl.IVCurve_showHide_lrss.region = self.regions["lrwin1"][
                "region"
            ]  # save region with checkbox
            # self.lrtau = pg.LinearRegionItem([0, 1],
            # brush=pg.mkBrush(255, 0, 0, 50.))
            self.regions["lrrmp"] = {
                "name": "rmp",
                "region": pg.LinearRegionItem(
                    [0, 1], brush=pg.mkBrush(255, 255, 0, 25.0)
                ),
                "plot": self.data_plot,
                "state": self.ctrl.IVCurve_showHide_lrrmp,
                "shstate": True,  # keep internal copy of the state
                "mode": None,
                "start": self.ctrl.IVCurve_rmpTStart,
                "stop": self.ctrl.IVCurve_rmpTStop,
                "updater": self.update_rmpAnalysis,
                "units": "ms",
            }
            self.ctrl.IVCurve_showHide_lrrmp.region = self.regions["lrrmp"][
                "region"
            ]  # save region with checkbox
            # establish that measurement is on top, exclusion is next, and reference is on bottom
            self.regions["lrtau"] = {
                "name": "tau",
                "region": pg.LinearRegionItem(
                    [0, 1], brush=pg.mkBrush(255, 255, 0, 25.0)
                ),
                "plot": self.data_plot,
                "state": self.ctrl.IVCurve_showHide_lrtau,
                "shstate": False,  # keep internal copy of the state
                "mode": None,
                "start": self.ctrl.IVCurve_tau2TStart,
                "stop": self.ctrl.IVCurve_tau2TStop,
                "updater": self.update_Tauh,
                "units": "ms",
            }
            self.ctrl.IVCurve_showHide_lrtau.region = self.regions["lrtau"][
                "region"
            ]  # save region with checkbox

            self.regions["lrwin0"]["region"].setZValue(500)
            self.regions["lrwin1"]["region"].setZValue(100)
            self.regions["lrtau"]["region"].setZValue(1000)
            self.regions["lrrmp"]["region"].setZValue(1000)
            self.regions["lrleak"]["region"].setZValue(1000)

            for regkey, reg in list(self.regions.items()):  # initialize region states
                self.show_or_hide(lrregion=regkey, forcestate=reg["shstate"])

            for regkey, reg in list(self.regions.items()):
                reg["plot"].addItem(reg["region"])
                reg["state"].clicked.connect(
                    functools.partial(self.show_or_hide, lrregion=regkey)
                )
                if reg["updater"] is not None:
                    reg["region"].sigRegionChangeFinished.connect(
                        functools.partial(reg["updater"], region=reg["name"])
                    )
                    # if self.regions[reg]['mode'] is not None:
                    #     self.regions[reg]['mode'].currentIndexChanged.connect(self.interactive_analysis)
        if reset:
            for regkey, reg in list(self.regions.items()):  # initialize region states
                self.show_or_hide(lrregion=regkey, forcestate=reg["shstate"])
        for reg in self.regions.values():
            for s in ["start", "stop"]:
                reg[s].setSuffix(" " + reg["units"])
        self.regions_exist = True

    def get_file_information(self, default_dh=None):
        """
        get_file_information reads the sequence information from the
        currently selected data file
        Two-dimensional sequences are supported.
        
        Parameter
        ---------
        default_dh : data handle (default: None)
            the data handle to use to access the file information
            if default_dh is None, then we use the currently selected
            file from the fileloader.
            
        Return
        ------
        nothing
        """

        if default_dh is None:
            dh = self.file_loader_instance.selectedFiles()
        else:
            dh = default_dh
        if not dh or len(dh) == 0:  # when using scripts, the fileloader may not know..
            return
        dh = dh[0]  # only the first file
        sequence = self.dataModel.listSequenceParams(dh)
        keys = list(sequence.keys())
        leftseq = [str(x) for x in sequence[keys[0]]]
        if len(keys) > 1:
            rightseq = [str(x) for x in sequence[keys[1]]]
        else:
            rightseq = []
        leftseq.insert(0, "All")
        rightseq.insert(0, "All")

        ### specific to our program - relocate
        self.ctrl.IVCurve_Sequence1.clear()
        self.ctrl.IVCurve_Sequence2.clear()
        self.ctrl.IVCurve_Sequence1.addItems(leftseq)
        self.ctrl.IVCurve_Sequence2.addItems(rightseq)
        self.sequence = sequence

    def updaterStatus(self, mode="on"):
        """
        Change the auto updater status
        
        Parameters
        ----------
        mode : string (default: 'on')
            sets the "auto update" mode for the regions to on or off.
        
        Returns
        -------
        Nothing
        """
        for regkey, reg in list(self.regions.items()):
            if mode in ["on", "On", True]:
                self.doUpdates = True
                reg["region"].sigRegionChangeFinished.connect(
                    functools.partial(reg["updater"], region=reg["name"])
                )
            if mode in ["off", "Off", None, False]:
                self.doUpdates = False
                try:
                    reg["region"].sigRegionChangeFinished.disconnect()
                except:  # may already be disconnected...so fail gracefully
                    pass

    def loadFileRequested(self, dh, analyze=True, bridge=None):
        """
        loadFileRequested is called by "file loader" when a file is requested.
            FileLoader is provided by the AnalysisModule class
            dh is the handle to the currently selected directory (or directories)

        This function loads all of the successive records from the specified protocol.
        Ancillary information from the protocol is stored in class variables.
        Extracts information about the commands, sometimes using a rather
        simplified set of assumptions. Much of the work for reading the data is
        performed in the GetClamps class in PatchEPhys.
        
        Parameters
        ----------
        dh : directory handle (no default)
            the directory handle (or list of handles) representing the selected
            entitites from the FileLoader in the Analysis Module
        
        analyze : Boolean (default: True)
            Enables the analysis to begin immediately after loading the file
        
        bridge : float (default: None)
            sets the initial bridge balance used to correct the data in current
            clamp. A value of None disables the correction.
        
        Returns
        -------
        True if successful; otherwise raises an exception
        
        modifies: plots, sequence, data arrays, data mode, etc.
        """

        self.data_plot.clearPlots()
        self.cmd_plot.clearPlots()
        self.clear_results()
        self.updaterStatus("Off")

        if len(dh) == 0:
            raise Exception(
                "IVCurve::loadFileRequested: " + "Select an IV protocol directory."
            )
        if len(dh) != 1:
            raise Exception(
                "IVCurve::loadFileRequested: " + "Can only load one file at a time."
            )

        self.get_file_information(
            default_dh=dh
        )  # Get info from most recent file requested
        dh = dh[0]  # just get the first one
        self.filename = dh.name()
        self.current_dirhandle = dh  # this is critical!
        self.loaded = dh
        self.analysis_summary = self.dataModel.cell_summary(
            dh
        )  # get other info as needed for the protocol
        # print 'analysis summary: ', self.analysis_summary

        pars = {}  # need to pass some parameters from the GUI
        pars[
            "limits"
        ] = (
            self.ctrl.IVCurve_IVLimits.isChecked()
        )  # checkbox: True if loading limited current range
        pars[
            "cmin"
        ] = self.ctrl.IVCurve_IVLimitMin.value()  # minimum current level to load
        pars[
            "cmax"
        ] = self.ctrl.IVCurve_IVLimitMax.value()  # maximum current level to load
        pars["KeepT"] = self.ctrl.IVCurve_KeepT.isChecked()  # keep timebase
        # sequence selections:
        # pars[''sequence'] is a dictionary
        # The dictionary has  'index' (currentIndex()) and 'count' from the GUI
        pars["sequence1"] = {"index": [self.ctrl.IVCurve_Sequence1.currentIndex() - 1]}
        pars["sequence1"]["count"] = self.ctrl.IVCurve_Sequence1.count() - 1
        pars["sequence2"] = {"index": [self.ctrl.IVCurve_Sequence2.currentIndex() - 1]}
        pars["sequence2"]["count"] = self.ctrl.IVCurve_Sequence2.count() - 1

        ci = self.Clamps.getClampData(dh, pars)
        if ci is None:
            return False
        self.ctrl.IVCurve_dataMode.setText(self.Clamps.data_mode)
        # self.bridgeCorrection = 200e6

        # print 'bridge: ', bridge
        if bridge is not None:
            self.bridgeCorrection = bridge
            self.ctrl.IVCurve_bridge.setValue(self.bridgeCorrection)
            # for i in range(self.Clamps.traces.shape[0]):
            print("******** Doing bridge correction: ", self.bridgeCorrection)
            self.Clamps.traces = self.Clamps.traces - (
                self.bridgeCorrection * self.Clamps.cmd_wave
            )
        else:
            br = self.ctrl.IVCurve_bridge.value() * 1e6
            # print 'br: ', br
            if br != 0.0:
                self.bridgeCorrection = br
                self.Clamps.traces = self.Clamps.traces - (
                    self.bridgeCorrection * self.Clamps.cmd_wave
                )
            else:
                self.bridgeCorrection = None
                
        if self.Clamps.data_mode in self.dataModel.ic_modes:
            self.label_up(self.RMP_plot, "T (s)", "V (mV)", "RMP")
        else:
            self.label_up(self.RMP_plot, "T (s)", "I (pA)", "Ihold")
        # now plot and analyze the data
        self.ctrl.IVCurve_tauh_Commands.clear()
        self.ctrl.IVCurve_tauh_Commands.addItems(ci["cmdList"])
        self.color_scale.setIntColorScale(0, len(ci["dirs"]), maxValue=200)
        self.make_map_symbols()
        self.plot_traces()
        self.setup_regions()
        self.get_window_analysisPars()  # prepare the analysis parameters
        self.updaterStatus("on")  # re-enable update status
        if (
            analyze
        ):  # only do this if requested (default). Don't do in script processing ....yet
            self.updateAnalysis()
        return True

    def plot_traces(self, multimode=False):
        """
        Plot the current data traces.
       
        Parameters
        ---------_
        multimode: Boolean (default: False)
            If true, try using "multiline plot routine" to speed up plots (no color though)
        
        Returns
        -------
        Nothing
        """

        if self.ctrl.IVCurve_KeepAnalysis.isChecked():
            self.keep_analysis_count += 1
        else:
            self.keep_analysis_count = 0  # always make sure is reset
            # this is the only way to reset iterators.
            self.color_list = itertools.cycle(self.colors)
            self.symbol_list = itertools.cycle(self.symbols)
        self.clearDecorators()
        self.make_map_symbols()
        self.data_plot.plotItem.clearPlots()
        self.cmd_plot.plotItem.clearPlots()
        ntr = self.Clamps.traces.shape[0]
        self.data_plot.setDownsampling(auto=False, mode="mean")
        self.data_plot.setClipToView(
            False
        )  # setting True deletes some points used for decoration of spikes by shape
        self.cmd_plot.setDownsampling(auto=False, mode="mean")
        self.cmd_plot.setClipToView(
            True
        )  # can leave this true since we do not put symbols on the plot
        self.data_plot.disableAutoRange()
        self.cmd_plot.disableAutoRange()
        cmdindxs = np.unique(self.Clamps.commandLevels)  # find the unique voltages
        colindxs = [
            int(np.where(cmdindxs == self.Clamps.commandLevels[i])[0])
            for i in range(len(self.Clamps.commandLevels))
        ]  # make a list to use

        if multimode:
            pass
            # datalines = MultiLine(self.Clamps.time_base, self.Clamps.traces, downsample=10)
            # self.data_plot.addItem(datalines)
            # cmdlines = MultiLine(self.Clamps.time_base, self.Clamps.cmd_wave, downsample=10)
            # self.cmd_plot.addItem(cmdlines)
        else:
            for i in range(ntr):
                atrace = self.Clamps.traces[i]
                acmdwave = self.Clamps.cmd_wave[i]
                p = self.data_plot.plot(
                    x=self.Clamps.time_base,
                    y=atrace,
                    downSample=10,
                    downSampleMethod="mean",
                    pen=pg.intColor(colindxs[i], len(cmdindxs), maxValue=255),
                )
                self.plot_list.append(p)
                p = self.cmd_plot.plot(
                    x=self.Clamps.time_base,
                    y=acmdwave,
                    downSample=10,
                    downSampleMethod="mean",
                    pen=pg.intColor(colindxs[i], len(cmdindxs), maxValue=255),
                )
                self.plot_list.append(p)

        if self.Clamps.data_mode in self.dataModel.ic_modes:
            self.label_up(self.data_plot, "T (s)", "V (V)", "Data")
            self.label_up(
                self.cmd_plot, "T (s)", "I (%s)" % self.Clamps.command_units, "Data"
            )
        elif self.Clamps.data_mode in self.dataModel.vc_modes:  # voltage clamp
            self.label_up(self.data_plot, "T (s)", "I (A)", "Data")
            self.label_up(
                self.cmd_plot, "T (s)", "V (%s)" % self.Clamps.command_units, "Data"
            )
        else:  # mode is not known: plot both as V
            self.label_up(self.data_plot, "T (s)", "V (V)", "Data")
            self.label_up(
                self.cmd_plot, "T (s)", "V (%s)" % self.Clamps.command_units, "Data"
            )
        self.data_plot.autoRange()
        self.cmd_plot.autoRange()

    def setup_regions(self):
        """
        Initialize the positions of the lr regions on the display.
        We attempt to use a logical set of values based on the timing of command steps
        and stimulus events
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """

        self.initialize_regions()  # now create the analysis regions, if not already existing
        if (
            self.ctrl.IVCurve_KeepT.isChecked() is False
        ):  # change regions; otherwise keep...
            tstart_pk = self.Clamps.tstart
            tdur_pk = self.Clamps.tdur * 0.4  # use first 40% of trace for peak
            tstart_ss = self.Clamps.tstart + 0.75 * self.Clamps.tdur
            tdur_ss = self.Clamps.tdur * 0.25
            tstart_tau = self.Clamps.tstart + 0.1 * self.Clamps.tdur
            tdur_tau = 0.9 * self.Clamps.tdur
            # tauh window
            self.regions["lrtau"]["region"].setRegion(
                [tstart_tau, tstart_tau + tdur_tau]
            )
            # peak voltage window
            self.regions["lrwin0"]["region"].setRegion([tstart_pk, tstart_pk + tdur_pk])
            # steady-state meausurement:
            self.regions["lrwin1"]["region"].setRegion([tstart_ss, tstart_ss + tdur_ss])
            # rmp measurement
            self.regions["lrrmp"]["region"].setRegion(
                [0.0, self.Clamps.tstart * 0.9]
            )  # rmp window
            # print 'rmp window region: ', self.Clamps.tstart * 0.9
        for r in ["lrtau", "lrwin0", "lrwin1", "lrrmp"]:
            self.regions[r]["region"].setBounds(
                [0.0, np.max(self.Clamps.time_base)]
            )  # limit regions to data

    def get_window_analysisPars(self):
        """
        Retrieve the settings of the lr region windows, and some other general values
        in preparation for analysis
        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
        self.analysis_parameters = {}  # start out empty so we are not fooled by priors
        for region in ["lrleak", "lrwin0", "lrwin1", "lrrmp", "lrtau"]:
            rgninfo = self.regions[region]["region"].getRegion()  # from the display
            self.regions[region]["start"].setValue(
                rgninfo[0] * 1.0e3
            )  # report values to screen
            self.regions[region]["stop"].setValue(rgninfo[1] * 1.0e3)
            self.analysis_parameters[region] = {"times": rgninfo}
        # for region in ['lrwin0', 'lrwin1', 'lrwin2']:
        #            if self.regions[region]['mode'] is not None:
        #                self.analysis_parameters[region]['mode'] = self.regions[region]['mode'].currentText()
        #         self.get_alternation()  # get values into the analysisPars dictionary
        #         self.get_baseline()
        #         self.get_junction()

    def updateAnalysis(self, presets=None, region=None):
        """updateAnalysis re-reads the time parameters and re-analyzes the spikes
        
        Parameters
        ----------
        presets : boolean or dict (default: None)
            sets up selected keys in analysis_summary with the values in presets
        
        region : None or Boolean (default: None)
            Set True to force the show status, False to Hide. 
            If forcestate is None, then uses the region's 'shstate' value 
            to set the state.
        
        Returns
        -------
        Nothing
        
        """
        #        print 'self.Script.script: ', self.Script.script['Cells'].keys()
        if presets in [True, False]:
            presets = None
        #        print '\n\n*******\n', traceback.format_stack(limit=7)
        if presets is not None and type(presets) == type(
            {}
        ):  # copy from dictionary of presets into analysis parameters
            for k in list(presets.keys()):
                self.analysis_summary[k] = presets[k]
            if "SpikeThreshold" in list(presets.keys()):
                self.ctrl.IVCurve_SpikeThreshold.setValue(
                    float(presets["SpikeThreshold"])
                )
                # print 'set threshold to %f' % float(presets['SpikeThreshold'])
            if "bridgeCorrection" in list(presets.keys()):
                self.bridgeCorrection = presets["bridgeCorrection"]
                print("####### BRIDGE CORRRECTION #######: ", self.bridgeCorrection)
            else:
                self.bridgeCorrection = 0.0
        self.get_window_analysisPars()
        self.readParsUpdate(clearFlag=True, pw=False)

    def readParsUpdate(self, clearFlag=False, pw=False):
        """
        Read the parameter window entries, set the lr regions to the values
        in the window, and do an update on the analysis
        
        Parameters
        ----------
        clearFlag : Boolean, False
            appears to be unused
        
        pw : Boolean (default:  False)
            Passed to update_rmpAnalysis
        
        Returns
        -------
        Nothing
        """
        if not self.doUpdates:
            return
        # analyze spikes first (gets information on which traces to exclude/include for other calculations)
        #        print 'readparsupdate, calling analyze spikes'
        # self.SA.setup(self.Clamps, 0)
        self.analyzeSpikes()

        self.analysis_summary[
            "tauh"
        ] = np.nan  # define these because they may not get filled...
        self.analysis_summary["Gh"] = np.nan

        (pen, filledbrush, emptybrush, symbol, n, clearFlag) = self.map_symbol()
        # update RMP first as we might need it for the others.
        if self.ctrl.IVCurve_showHide_lrrmp.isChecked():
            rgnx1 = self.ctrl.IVCurve_rmpTStart.value() / 1.0e3
            rgnx2 = self.ctrl.IVCurve_rmpTStop.value() / 1.0e3
            self.regions["lrrmp"]["region"].setRegion([rgnx1, rgnx2])
            self.update_rmpAnalysis(clear=clearFlag, pw=pw)

        if self.ctrl.IVCurve_showHide_lrss.isChecked():
            rgnx1 = self.ctrl.IVCurve_ssTStart.value() / 1.0e3
            rgnx2 = self.ctrl.IVCurve_ssTStop.value() / 1.0e3
            self.regions["lrwin1"]["region"].setRegion([rgnx1, rgnx2])
            self.update_ssAnalysis()

        if self.ctrl.IVCurve_showHide_lrpk.isChecked():
            rgnx1 = self.ctrl.IVCurve_pkTStart.value() / 1.0e3
            rgnx2 = self.ctrl.IVCurve_pkTStop.value() / 1.0e3
            self.regions["lrwin0"]["region"].setRegion([rgnx1, rgnx2])
            self.update_pkAnalysis(clear=clearFlag, pw=pw)

        if self.ctrl.IVCurve_subLeak.isChecked():
            rgnx1 = self.ctrl.IVCurve_LeakMin.value() / 1e3
            rgnx2 = self.ctrl.IVCurve_LeakMax.value() / 1e3
            self.regions["lrleak"]["region"].setRegion([rgnx1, rgnx2])
            self.update_ssAnalysis()
            self.update_pkAnalysis()

        if self.ctrl.IVCurve_showHide_lrtau.isChecked():
            # include tau in the list... if the tool is selected
            rgnx1 = self.ctrl.IVCurve_tau2TStart.value() / 1e3
            rgnx2 = self.ctrl.IVCurve_tau2TStop.value() / 1e3
            self.regions["lrtau"]["region"].setRegion([rgnx1, rgnx2])
            self.update_Tauh()

        if self.ctrl.IVCurve_PeakMode.currentIndexChanged:
            self.peakmode = self.ctrl.IVCurve_PeakMode.currentText()
            self.update_pkAnalysis()

        if self.Clamps.data_mode in self.dataModel.ic_modes:
            self.analyzeSpikeShape()  # finally do the spike shape
        self.ctrl.IVCurve_bridge.setValue(0.0)  # reset bridge value after analysis.

    def read_script(self):
        """
        read a script file from disk, and use that information to drive the analysis
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """

        self.script_name = self.Script.read_script()
        if self.script_name is None:
            print("Failed to read script")
            self.ctrl.IVCurve_ScriptName.setText("None")
            return
        self.ctrl.IVCurve_ScriptName.setText(os.path.basename(self.script_name))
        self.Script.run_script()

    def rerun_script(self):
        """
        revalidate and run the current script
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """
        self.Script.run_script()

    def analyzeSpikes(self):
        """
        analyzeSpikes: Using the threshold set in the control panel, count the
        number of spikes in the stimulation window (self.Clamps.tstart, self.Clamps.tend)
        Updates the spike plot(s).

        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        
        The following variables are set:
        self.SA.spikecount: a 1-D numpy array of spike counts, aligned with the
            current (command)
        self.adapt_ratio: the adaptation ratio of the spike train
        self.fsl: a numpy array of first spike latency for each command level
        self.fisi: a numpy array of first interspike intervals for each
            command level
        self.nospk: the indices of command levels where no spike was detected
        self.spk: the indices of command levels were at least one spike
            was detected
        """
        if self.Clamps.data_mode in self.dataModel.vc_modes:
            return  # skip doing spike plots in voltage clamp
        if self.keep_analysis_count == 0:
            clearFlag = True
        else:
            clearFlag = False
        self.analysis_summary["FI_Curve"] = None
        # print '***** analyzing Spikes'
        if (
            self.Clamps.data_mode not in self.dataModel.ic_modes
            or self.Clamps.time_base is None
        ):
            # print(
            #     (
            #         "IVCurve::analyzeSpikes: Cannot count spikes, "
            #         + "and dataMode is ",
            #         self.Clamps.data_mode,
            #         "and ICModes are: ",
            #         self.dataModel.ic_modes,
            #         "tx is: ",
            #         self.tx,
            #     )
            # )
            self.ctrl.IVCurve_AR.setText("%7.3f" % 0.0)
            
            self.SA.spikecount = []
            p = self.fiPlot.plot(
                x=[],
                y=[],
                clear=clearFlag,
                pen="w",
                symbolSize=6,
                symbolPen="b",
                symbolBrush=(0, 0, 255, 200),
                symbol="s",
            )
            self.plot_list.append(p)
            p = self.fslPlot.plot(
                x=[],
                y=[],
                pen="w",
                clear=clearFlag,
                symbolSize=6,
                symbolPen="g",
                symbolBrush=(0, 255, 0, 200),
                symbol="t",
            )
            self.plot_list.append(p)
            p = self.fslPlot.plot(
                x=[],
                y=[],
                pen="w",
                symbolSize=6,
                symbolPen="y",
                symbolBrush=(255, 255, 0, 200),
                symbol="s",
            )
            self.plot_list.append(p)
            return
        threshold = self.ctrl.IVCurve_SpikeThreshold.value() * 1e-3
        self.analysis_summary[
            "SpikeThreshold"
        ] = self.ctrl.IVCurve_SpikeThreshold.value()

        self.SA.setup(self.Clamps, threshold)

        self.SA.analyzeSpikes()
        self.adapt_ratio = (
            self.SA.adapt_ratio
        )  # np.mean(ar[iAR])  # only where we made the measurement
        self.analysis_summary["AdaptRatio"] = self.SA.adapt_ratio
        self.ctrl.IVCurve_AR.setText("%7.3f" % self.SA.adapt_ratio)
        self.nospk = np.where(self.SA.spikecount == 0)
        self.spk = np.where(self.SA.spikecount > 0)[0]
        self.analysis_summary["FI_Curve"] = np.array(
            [self.Clamps.values, self.SA.spikecount]
        )
        #        print self.analysis_summary['FI_Curve']
        self.spikes_counted = True
        self.update_SpikePlots()

    def _timeindex(self, t):
        """
        Get the index of the current time_base
        
        Parameters
        ----------
        t : float
        
        Returns
        -------
        Index of the time in the time base closest to t
        """
        return np.argmin(self.Clamps.time_base - t)

    def analyzeSpikeShape(self):
        """
        Wrapper to get spike shape data and store in the
        local analysis_summary dictionary
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """
        self.SA.analyzeSpikeShape()
        self.spikeShape = self.SA.spikeShape
        self.analysis_summary[
            "spikes"
        ] = self.SA.spikeShape  # save in the summary dictionary too
        self.analysis_summary["iHold"] = np.mean(self.SA.iHold)
        self.analysis_summary["pulseDuration"] = self.Clamps.tend - self.Clamps.tstart
        # self.getClassifyingInfo()  # build analysis summary here as well.
        # copy all the analysis summary from the SA to here.
        for k in list(self.SA.analysis_summary.keys()):
            self.analysis_summary[k] = self.SA.analysis_summary[k]
        self.clearDecorators()
        self.spikeDecorator()

    def spikeDecorator(self):
        """
        Put markers on the spikes to visually confirm the analysis of thresholds, etc.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """
        # get colors
        cmdindxs = np.unique(self.Clamps.commandLevels)  # find the unique voltages
        colindxs = [
            int(np.where(cmdindxs == self.Clamps.commandLevels[i])[0])
            for i in range(len(self.Clamps.commandLevels))
        ]  # make a list to use
        alllats = []
        allpeakt = []
        allpeakv = []
        for i, trace in enumerate(self.spikeShape):
            aps = []
            tps = []
            paps = []
            ptps = []
            taps = []
            ttps = []
            hwv = []
            tups = []
            tdps = []

            for j, spk in enumerate(self.spikeShape[trace]):
                aps.append(self.spikeShape[trace][spk]["AP_beginV"])
                alllats.append(self.spikeShape[trace][spk]["AP_Latency"])
                tps.append(self.spikeShape[trace][spk]["AP_Latency"])
            u = self.data_plot.plot(
                tps, aps, pen=None, symbol="o", brush=pg.mkBrush("g"), symbolSize=4
            )
            self.dataMarkers.append(u)
            for j, spk in enumerate(self.spikeShape[trace]):
                paps.append(self.spikeShape[trace][spk]["peak_V"])
                ptps.append(self.spikeShape[trace][spk]["peak_T"])
                allpeakt.append(self.spikeShape[trace][spk]["peak_T"] + 0.01)
                allpeakv.append(self.spikeShape[trace][spk]["peak_V"])
            # u = self.data_plot.plot(allpeakt, allpeakv, pen=None, symbol='o', brush=pg.mkBrush('r'), size=2)
            # self.dataMarkers.append(u)

            u = self.data_plot.plot(
                ptps, paps, pen=None, symbol="t", brush=pg.mkBrush("w"), symbolSize=4
            )
            self.dataMarkers.append(u)

            for j, spk in enumerate(self.spikeShape[trace]):
                taps.append(self.spikeShape[trace][spk]["trough_V"])
                ttps.append(self.spikeShape[trace][spk]["trough_T"])
            u = self.data_plot.plot(
                ttps, taps, pen=None, symbol="+", brush=pg.mkBrush("r"), symbolSize=4
            )
            self.dataMarkers.append(u)
            for j, spk in enumerate(self.spikeShape[trace]):
                tups.append(self.spikeShape[trace][spk]["hw_up"])
                tdps.append(self.spikeShape[trace][spk]["hw_down"])
                hwv.append(self.spikeShape[trace][spk]["hw_v"])
            u = self.data_plot.plot(
                tups, hwv, pen=None, symbol="d", brush=pg.mkBrush("c"), symbolSize=4
            )
            self.dataMarkers.append(u)
            d = self.data_plot.plot(
                tdps, hwv, pen=None, symbol="s", brush=pg.mkBrush("c"), symbolSize=4
            )
            self.dataMarkers.append(d)

    def clearDecorators(self):
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """
        if len(self.dataMarkers) > 0:
            [self.dataMarkers[k].clear() for k, m in enumerate(self.dataMarkers)]
            # [self.dataMarkers[k].removeItem() for k, m in enumerate(self.dataMarkers)]
        self.dataMarkers = []

    def update_Tau_membrane(
        self, peak_time=None, printWindow=False, whichTau=1, vrange=[-5.0, -20.0]
    ):
        """
        Compute time constant (single exponential) from the
        onset of the response
        using lrpk window, and only steps that produce a voltage change between 5 and 20 mV below rest
        or as specified
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Nothing
        """

        if (
            len(self.Clamps.commandLevels) == 0
        ):  # probably not ready yet to do the update.
            return
        if self.Clamps.data_mode not in self.dataModel.ic_modes:  # only permit in IC
            return
        rgnpk = list(self.regions["lrwin0"]["region"].getRegion())
        self.RmTau.setup(clamps=self.Clamps, spikes=self.SA, dataplot=self.data_plot)
        self.RmTau.tau_membrane(
            peak_time=None,
            printWindow=False,
            whichTau=1,
            vrange=[-5.0, -20.0],
            region=rgnpk,
        )

        self.ctrl.IVCurve_Tau.setText("%18.1f ms" % (self.RmTau.taum_taum * 1.0e3))
        self.analysis_summary["tau"] = self.RmTau.taum_taum * 1.0e3
        tautext = "Mean Tau: %8.1f"
        if printWindow:
            print(tautext % (self.RmTau.taum_taum * 1e3))
        self.show_taum_plot()

    def show_taum_plot(self):
        Fits = Fitting.Fitting()
        fitPars = self.RmTau.taum_pars
        xFit = np.zeros((len(self.RmTau.taum_pars), 500))
        for i in range(len(self.RmTau.taum_pars)):
            xFit[i, :] = np.arange(
                0,
                self.RmTau.taum_win[1] - self.RmTau.taum_win[0],
                (self.RmTau.taum_win[1] - self.RmTau.taum_win[0]) / 500.0,
            )
        yFit = np.zeros((len(fitPars), xFit.shape[1]))
        fitfunc = Fits.fitfuncmap[self.RmTau.taum_func]
        if len(list(self.RmTau.taum_fitted.keys())) > 0:
            [
                self.RmTau.taum_fitted[k].clear()
                for k in list(self.RmTau.taum_fitted.keys())
            ]
        self.RmTau.taum_fitted = {}
        for k, whichdata in enumerate(self.RmTau.taum_whichdata):
            yFit[k] = fitfunc[0](
                fitPars[k], xFit[k], C=None
            )  # +self.ivbaseline[whichdata]
            self.RmTau.taum_fitted[k] = self.data_plot.plot(
                xFit[k] + self.RmTau.taum_win[0],
                yFit[k],
                pen=pg.mkPen("r", width=2, style=QtCore.Qt.DashLine),
            )
            self.plot_list.append(self.RmTau.taum_fitted[k])
            
    def update_Tauh(self, region=None, printWindow=False):
        """
        Compute tau (single exponential) from the onset of the markers
        using lrtau window, and only for the step closest to the selected
        current level in the GUI window.
        
        Parameters
        ----------
        region : dummy argument, default : None
        printWindow : Boolean, default : False
            
        region is a dummy argument... 
        Also compute the ratio of the sag from the peak (marker1) to the
        end of the trace (marker 2).
        Based on analysis in Fujino and Oertel, J. Neuroscience 2001,
        to type cells based on different Ih kinetics and magnitude.
        """
        self.analysis_summary["tauh"] = np.nan
        self.analysis_summary["Gh"] = np.nan
        if not self.ctrl.IVCurve_showHide_lrtau.isChecked():
            return
        rgn = self.regions["lrtau"]["region"].getRegion()
        pkRgn = self.regions["lrwin0"]["region"].getRegion()
        ssRgn = self.regions["lrwin1"]["region"].getRegion()
        current = self.ctrl.IVCurve_tauh_Commands.currentIndex()
        self.ctrl.IVCurve_tau2TStart.setValue(rgn[0] * 1.0e3)
        self.ctrl.IVCurve_tau2TStop.setValue(rgn[1] * 1.0e3)

        self.RmTau.tau_h(
            current, rgn, pkRgn, ssRgn
        )  # compute tauh and associated parameters

        bluepen = pg.mkPen("b", width=2, style=QtCore.Qt.DashLine)
        self.RmTau.tauh_fitted[0] = self.data_plot.plot(
            self.RmTau.tauh_xf[0]+rgn[0], self.RmTau.tauh_yf[0], pen=bluepen
        )
        self.plot_list.append(self.RmTau.taum_fitted[0])
        self.ctrl.IVCurve_Tauh.setText("%8.1f ms" % (self.RmTau.tauh_meantau * 1.0e3))
        self.ctrl.IVCurve_Ih_ba.setText("%8.1f" % (self.RmTau.tauh_bovera * 100.0))
        self.ctrl.IVCurve_ssAmp.setText(
            "%8.2f" % (self.RmTau.tauh_vss - self.RmTau.tauh_vrmp)
        )
        self.ctrl.IVCurve_pkAmp.setText(
            "%8.2f" % (self.RmTau.tauh_vpk - self.RmTau.tauh_vrmp)
        )
        self.ctrl.IVCurve_Gh.setText("%8.2f nS" % (self.RmTau.tauh_Gh * 1e9))
        if self.RmTau.tauh_bovera < 0.55 and self.RmTau.tauh_meantau < 0.015:  #
            self.ctrl.IVCurve_FOType.setText("D Stellate")
        else:
            self.ctrl.IVCurve_FOType.setText("T Stellate")
        self.analysis_summary["tauh"] = self.RmTau.tauh_meantau * 1.0e3
        self.analysis_summary["Gh"] = self.RmTau.tauh_Gh

    def update_ssAnalysis(self):
        """
        Compute the steady-state IV from the selected time window

        Parameters
        ----------
            None.
        
        Returns
        -------
            nothing.
        
        modifies:
            ivss, yleak, ivss_cmd, cmd.

        The IV curve is only valid when there are no spikes detected in
            the window. The values in the curve are taken as the mean of the
            current and the voltage in the time window, at each command step.
        We also compute the input resistance.
        For voltage clamp data, we can optionally remove the "leak" current.
        The resulting curve is plotted.
        """
        if self.Clamps.traces is None:
            return
        rgnss = self.regions["lrwin1"]["region"].getRegion()
        r1 = rgnss[1]
        if rgnss[1] == rgnss[0]:
            print("Steady-state regions have no width; using 100 msec. window for ss ")
            r1 = rgnss[0] + 0.1
        self.ctrl.IVCurve_ssTStart.setValue(rgnss[0] * 1.0e3)
        self.ctrl.IVCurve_ssTStop.setValue(r1 * 1.0e3)
        data1 = self.Clamps.traces["Time" : rgnss[0] : r1]
        #       print 'data shape: ', data1.shape
        if data1.shape[1] == 0 or data1.shape[0] == 1:
            return  # skip it
        self.ivss = []
        self.ivss_cmd = []

        # check out whether there are spikes in the window that is selected
        threshold = self.ctrl.IVCurve_SpikeThreshold.value() * 1e-3
        ntr = len(self.Clamps.traces)
        if not self.spikes_counted and self.Clamps.data_mode in self.dataModel.ic_modes:
            self.analyzeSpikes()

        self.ivss = data1.mean(axis=1)  # all traces
        if self.ctrl.IVCurve_SubBaseline.isChecked() and self.Clamps.data_mode in self.dataModel.ic_modes:
            self.ivss = self.ivss - self.RmTau.ivbaseline

        if len(self.nospk) >= 1:
            # Steady-state IV where there are no spikes
            self.ivss = self.ivss[self.nospk]
            self.ivss_cmd = self.Clamps.commandLevels[self.nospk]
            #            self.commandLevels = commands[self.nospk]
            # compute Rin from the SS IV:
            # this makes the assumption that:
            # successive trials are in order (as are commands)
            # commands are not repeated...
            if len(self.ivss_cmd) > 1 and len(self.ivss) > 1:
                self.r_in = np.max(np.diff(self.ivss) / np.diff(self.ivss_cmd))
                self.ctrl.IVCurve_Rin.setText("%9.1f M\u03A9" % (self.r_in * 1.0e-6))
                self.analysis_summary["Rin"] = self.r_in * 1.0e-6
            else:
                self.ctrl.IVCurve_Rin.setText("No valid points")
        else:
            self.ivss_cmd = self.Clamps.commandLevels
        if self.Clamps.data_mode in self.dataModel.vc_modes:
            self.ivss_cmd = self.ivss_cmd + self.Clamps.holding
        self.yleak = np.zeros(len(self.ivss))
        if self.ctrl.IVCurve_subLeak.isChecked() and self.Clamps.data_mode in self.dataModel.ic_modes:
            if self.Clamps.data_mode in self.dataModel.ic_modes:
                sf = 1e-12
            elif self.Clamps.data_mode in self.dataModel.vc_modes:
                sf = 1e-3
            else:
                sf = 1.0
            (x, y) = Utility.clipdata(
                self.ivss,
                self.ivss_cmd,
                self.ctrl.IVCurve_LeakMin.value() * sf,
                self.ctrl.IVCurve_LeakMax.value() * sf,
            )
            try:
                p = np.polyfit(x, y, 1)  # linear fit
                self.yleak = np.polyval(p, self.ivss_cmd)
                self.ivss = self.ivss - self.yleak
            except:
                raise ValueError("IVCurve Leak subtraction: no valid points to correct")
        if len(self.ivss_cmd) > 0:
            isort = np.argsort(self.ivss_cmd)
            self.ivss_cmd = self.ivss_cmd[isort]
            self.ivss = self.ivss[isort]
        self.analysis_summary["IV_Curve_ss"] = [self.ivss_cmd, self.ivss]
        self.update_IVPlot()

    def update_pkAnalysis(self, clear=False, pw=False):
        """
        Compute the peak IV (minimum) from the selected window
        mode can be 'min', 'max', or 'abs'

        Parameters
        ----------
        clear : Boolean, False
        pw : Boolean, False
            pw is passed to update_taumembrane to control printing.
        """
        if self.Clamps.traces is None:
            return
        mode = self.ctrl.IVCurve_PeakMode.currentText()
        rgnpk = self.regions["lrwin0"]["region"].getRegion()
        self.ctrl.IVCurve_pkTStart.setValue(rgnpk[0] * 1.0e3)
        self.ctrl.IVCurve_pkTStop.setValue(rgnpk[1] * 1.0e3)
        data2 = self.Clamps.traces["Time" : rgnpk[0] : rgnpk[1]]
        if data2.shape[1] == 0:
            return  # skip it - window missed the data
        # check out whether there are spikes in the window that is selected
        # but only in current clamp
        nospk = []
        peak_pos = None
        if self.Clamps.data_mode in self.dataModel.ic_modes:
            threshold = self.ctrl.IVCurve_SpikeThreshold.value() * 1e-3
            ntr = len(self.Clamps.traces)
            if not self.spikes_counted:
                self.analyzeSpikes()
            spikecount = np.zeros(ntr)

        if mode == "Min":
            self.ivpk = data2.min(axis=1)
            peak_pos = np.argmin(data2, axis=1)
        elif mode == "Max":
            self.ivpk = data2.max(axis=1)
            peak_pos = np.argmax(data2, axis=1)
        elif mode == "Abs":  # find largest regardless of the sign ('minormax')
            x1 = data2.min(axis=1)
            peak_pos1 = np.argmin(data2, axis=1)
            x2 = data2.max(axis=1)
            peak_pos2 = np.argmax(data2, axis=1)
            self.ivpk = np.zeros(data2.shape[0])
            for i in range(data2.shape[0]):
                if -x1[i] > x2[i]:
                    self.ivpk[i] = x1[i]
                    peak_pos = peak_pos1
                else:
                    self.ivpk[i] = x2[i]
                    peak_pos = peak_pos2
                    # self.ivpk = np.array([np.max(x1[i], x2[i]) for i in range(data2.shape[0]])
                    # self.ivpk = np.maximum(np.fabs(data2.min(axis=1)), data2.max(axis=1))
        if self.ctrl.IVCurve_SubBaseline.isChecked():
            self.ivpk = self.ivpk - self.RmTau.ivbaseline
        if len(self.nospk) >= 1 and self.Clamps.data_mode in self.dataModel.ic_modes:
            # Peak (min, max or absmax voltage) IV where there are no spikes
            self.ivpk = self.ivpk[self.nospk]
            self.ivpk_cmd = self.Clamps.commandLevels[self.nospk]
        else:
            self.ivpk_cmd = self.Clamps.commandLevels
        self.ivpk = self.ivpk.view(np.ndarray)
        if self.ctrl.IVCurve_subLeak.isChecked() and self.Clamps.data_mode in self.dataModel.ic_modes:
            self.ivpk = self.ivpk - self.yleak
        # now sort data in ascending command levels
        if self.Clamps.data_mode in self.dataModel.vc_modes:
            self.ivpk_cmd = self.ivpk_cmd + self.Clamps.holding
        isort = np.argsort(self.ivpk_cmd)
        self.ivpk_cmd = self.ivpk_cmd[isort]
        self.ivpk = self.ivpk[isort]
        self.analysis_summary["IV_Curve_pk"] = [self.ivpk_cmd, self.ivpk]
        self.update_IVPlot()
        peak_time = self.Clamps.time_base[peak_pos]
        self.update_Tau_membrane(peak_time=peak_time, printWindow=pw)

    def update_rmpAnalysis(self, **kwargs):
        """
        Compute the RMP over time/commands from the selected window
        """
        try:
            if self.Clamps.traces is None:
                return
        except:
            return
        if self.RmTau.Clamps is None:
            self.RmTau.setup(
                clamps=self.Clamps, spikes=self.SA, dataplot=self.data_plot
            )
        rgnrmp = self.regions["lrrmp"]["region"].getRegion()
        self.RmTau.rmp_analysis(rgnrmp)
        self.ctrl.IVCurve_rmpTStart.setValue(rgnrmp[0] * 1.0e3)
        self.ctrl.IVCurve_rmpTStop.setValue(rgnrmp[1] * 1.0e3)
        self.ctrl.IVCurve_vrmp.setText("%8.2f" % self.RmTau.rmp)
        self.update_RMPPlot()
        self.analysis_summary["RMP"] = self.RmTau.rmp

    def make_map_symbols(self):
        """
        Given the current state of things, (keeping the analysis, when
        superimposing multiple results, for example),
        sets self.currentSymDict with a dict of pen, fill color, empty color, a symbol from
        our lists, and a clearflag. Used to overplot different data.
        """
        n = self.keep_analysis_count
        pen = next(self.color_list)
        filledbrush = pen
        emptybrush = None
        symbol = next(self.symbol_list)
        if n == 0:
            clearFlag = True
        else:
            clearFlag = False
        self.currentSymDict = {
            "pen": pen,
            "filledbrush": filledbrush,
            "emptybrush": emptybrush,
            "symbol": symbol,
            "n": n,
            "clearFlag": clearFlag,
        }

    def map_symbol(self):
        cd = self.currentSymDict
        if cd["filledbrush"] == "w":
            cd["filledbrush"] = pg.mkBrush((128, 128, 128))
        if cd["pen"] == "w":
            cd["pen"] = pg.mkPen((128, 128, 128))
        self.lastSymbol = (
            cd["pen"],
            cd["filledbrush"],
            cd["emptybrush"],
            cd["symbol"],
            cd["n"],
            cd["clearFlag"],
        )
        return self.lastSymbol

    def update_IVPlot(self):
        """
        Draw the peak and steady-sate IV to the I-V window
        Note: x axis is always I or V, y axis V or I
        """
        if self.ctrl.IVCurve_KeepAnalysis.isChecked() is False:
            self.IV_plot.clear()
        (pen, filledbrush, emptybrush, symbol, n, clearFlag) = self.map_symbol()
        if self.Clamps.data_mode in self.dataModel.ic_modes:
            if len(self.ivss) > 0 and self.ctrl.IVCurve_showHide_lrss.isChecked():
                p = self.IV_plot.plot(
                    self.ivss_cmd * 1e12,
                    self.ivss * 1e3,
                    symbol=symbol,
                    pen=pen,
                    symbolSize=6,
                    symbolPen=pen,
                    symbolBrush=filledbrush,
                )
                self.plot_list.append(p)
            if len(self.ivpk) > 0 and self.ctrl.IVCurve_showHide_lrpk.isChecked():
                p = self.IV_plot.plot(
                    self.ivpk_cmd * 1e12,
                    self.ivpk * 1e3,
                    symbol=symbol,
                    pen=pen,
                    symbolSize=6,
                    symbolPen=pen,
                    symbolBrush=emptybrush,
                )
                self.plot_list.append(p)
            self.label_up(self.IV_plot, "I (pA)", "V (mV)", "I-V (CC)")
        if self.Clamps.data_mode in self.dataModel.vc_modes:
            if len(self.ivss) > 0 and self.ctrl.IVCurve_showHide_lrss.isChecked():
                p = self.IV_plot.plot(
                    np.array(self.ivss_cmd) * 1e3,
                    np.array(self.ivss) * 1e9,
                    symbol=symbol,
                    pen=pen,
                    symbolSize=6,
                    symbolPen=pen,
                    symbolBrush=filledbrush,
                )
                self.plot_list.append(p)
            if len(self.ivpk) > 0 and self.ctrl.IVCurve_showHide_lrpk.isChecked():
                p = self.IV_plot.plot(
                    np.array(self.ivpk_cmd) * 1e3,
                    np.array(self.ivpk) * 1e9,
                    symbol=symbol,
                    pen=pen,
                    symbolSize=6,
                    symbolPen=pen,
                    symbolBrush=emptybrush,
                )
                self.plot_list.append(p)
            self.label_up(self.IV_plot, "V (mV)", "I (nA)", "I-V (VC)")

    def update_RMPPlot(self):
        """
        Draw the RMP to the I-V window
        Note: x axis can be I, T, or  # spikes
        """
        if self.ctrl.IVCurve_KeepAnalysis.isChecked() is False:
            self.RMP_plot.clear()
        if len(self.RmTau.ivbaseline) > 0:
            (pen, filledbrush, emptybrush, symbol, n, clearFlag) = self.map_symbol()
            mode = self.ctrl.IVCurve_RMPMode.currentIndex()
            if self.Clamps.data_mode in self.dataModel.ic_modes:
                sf = 1e3
                self.RMP_plot.setLabel("left", "V (mV)")
                self.RMP_plot.setTitle("RMP")
                self.RMP_plot.setLabel("bottom", "I (pA)")
            else:
                sf = 1e12
                self.RMP_plot.setLabel("left", "I (pA)")
                self.RMP_plot.setTitle("Ihold")
                self.RMP_plot.setLabel("bottom", "V (V)")
            if mode == 0:
                p = self.RMP_plot.plot(
                    self.Clamps.trace_StartTimes,
                    sf * np.array(self.RmTau.ivbaseline),
                    symbol=symbol,
                    pen=pen,
                    symbolSize=6,
                    symbolPen=pen,
                    symbolBrush=filledbrush,
                )
                self.plot_list.append(p)
                self.RMP_plot.setLabel("bottom", "T (s)")
            elif mode == 1:
                p = self.RMP_plot.plot(
                    self.Clamps.commandLevels,
                    1.0e3 * np.array(self.RmTau.ivbaseline),
                    symbolSize=6,
                    symbol=symbol,
                    pen=pen,
                    symbolPen=pen,
                    symbolBrush=filledbrush,
                )
                self.RMP_plot.setLabel("bottom", "I (pA)")
                self.plot_list.append(p)
            elif mode == 2 and self.Clamps.data_mode in self.dataModel.ic_modes:
                p = self.RMP_plot.plot(
                    self.SA.spikecount,
                    1.0e3 * np.array(self.RmTau.ivbaseline),
                    symbolSize=6,
                    symbol=symbol,
                    pen=pen,
                    symbolPen=pen,
                    symbolBrush=emptybrush,
                )
                self.plot_list.append(p)
                self.RMP_plot.setLabel("bottom", "Spikes")
            else:
                pass

    def update_SpikePlots(self):
        """
        Draw the spike counts to the FI and FSL windows
        Note: x axis can be I, T, or  # spikes
        """
        if self.Clamps.data_mode in self.dataModel.vc_modes:
            self.fiPlot.clear()  # no plots of spikes in VC
            self.fslPlot.clear()
            return
        (pen, filledbrush, emptybrush, symbol, n, clearFlag) = self.map_symbol()
        fitpen = pg.mkPen("r")
        mode = self.ctrl.IVCurve_RMPMode.currentIndex()  # get x axis mode
        self.spcmd = self.Clamps.commandLevels[
            self.spk
        ]  # get command levels iwth spikes
        iscale = 1.0e12  # convert to pA
        yfslsc = 1.0  # convert to msec
        if mode == 0:  # plot with time as x axis
            xfi = self.Clamps.trace_StartTimes
            xfsl = self.Clamps.trace_StartTimes
            select = list(range(len(self.Clamps.trace_StartTimes)))
            xlabel = "T (s)"
        elif mode == 1:  # plot with current as x
            select = self.spk
            xfi = self.Clamps.commandLevels * iscale
            xfsl = self.spcmd * iscale
            xlabel = "I (pA)"
        elif mode == 2:  # plot with spike counts as x
            xfi = self.SA.spikecount
            xfsl = self.SA.spikecount
            select = list(range(len(self.SA.spikecount)))
            xlabel = "Spikes (N)"
        else:
            return  # mode not in available list
        p = self.fiPlot.plot(
            x=xfi,
            y=self.SA.spikecount,
            clear=clearFlag,
            symbolSize=6,
            symbol=symbol,
            pen=pen,
            symbolPen=pen,
            symbolBrush=filledbrush,
        )
        self.plot_list.append(p)
        # also fit the data and compute FI values
        # xdata must be current levels
        xfit = self.Clamps.commandLevels * iscale
        if np.max(self.SA.spikecount) > 0:
            spike_fit_result = self.SA.fitOne(
                xfit,
                self.SA.spikecount,
                info="FI",
                fixNonMonotonic=True,
                excludeNonMonotonic=False,
            )
            if spike_fit_result is not None:
                (fpar, xf, yf, names, error, f, func) = spike_fit_result
                p = self.fiPlot.plot(x=xf[0], y=yf[0], clear=False, pen=fitpen)
                self.plot_list.append(p)

        fslmax = 0.0
        if self.showFISI:
            p = self.fslPlot.plot(
                x=xfsl,
                y=self.SA.fsl[select] * yfslsc,
                clear=clearFlag,
                symbolSize=6,
                symbol=symbol,
                pen=pen,
                symbolPen=pen,
                symbolBrush=filledbrush,
            )
            self.plot_list.append(p)
            p = self.fslPlot.plot(
                x=xfsl,
                y=self.SA.fisi[select] * yfslsc,
                symbolSize=6,
                symbol=symbol,
                pen=pen,
                symbolPen=pen,
                symbolBrush=emptybrush,
            )
            self.plot_list.append(p)
            if len(xfsl) > 0:
                self.fslPlot.setXRange(0.0, np.max(xfsl))
                self.fslPlot.setYRange(
                    0.0, max(max(self.SA.fsl[select]), max(self.SA.fisi[select]))
                )
            ylabel = "Fsl/Fisi (ms)"
            xfsllabel = xlabel
            self.fslPlot.setTitle("FSL/FISI")
        else:
            maxspk = 0
            maxisi = 0.0
            clear = clearFlag
            for i, k in enumerate(self.allisi.keys()):
                nspk = len(self.allisi[k])
                xisi = np.arange(nspk)
                p = self.fslPlot.plot(
                    x=xisi,
                    y=self.SA.allisi[k] * yfslsc,
                    clear=clear,
                    symbolSize=6,
                    symbol=symbol,
                    pen=pen,
                    symbolPen=pen,
                    symbolBrush=filledbrush,
                )
                self.plot_list.append(p)
                clear = False
                maxspk = max(nspk, maxspk)
                maxisi = max(np.max(self.allisi[k]), maxisi)
            self.fslPlot.setXRange(0.0, maxspk)
            self.fslPlot.setYRange(0.0, maxisi)
            xfsllabel = "Spike Number"
            ylabel = "ISI (s)"
            self.fslPlot.setTitle("ISI vs. Spike Number")
        self.fiPlot.setLabel("bottom", xlabel)
        self.fslPlot.setLabel("bottom", xfsllabel)
        self.fslPlot.setLabel("left", ylabel)

    def to_mpl(self):
        title = f"{self.analysis_summary['CellID']:s}::{self.analysis_summary['Protocol']:s}"
        matplotlibexporter.matplotlibExport(gridlayout=self.gridLayout, title=title)

    def printAnalysis(self, printnow=True, script_header=True, copytoclipboard=True):
        """
        Print the analysis summary information (Cell, protocol, etc)
        in a nice formatted version to the terminal.
        The output can be copied to another program (excel, prism) for further analysis
        Parameters
        ----------
        printnow : Boolean, optional
            Set true to print to terminal, default: True
        script_header : Boolean, optional
            Set to print the header line, default: True
        copytoclipboard : Boolean, optional
            copy the text to the system clipboard, default: False
        
        Return
        ------
        ltxt : string
            The text that would be printed. Might be useful to capture for other purposes
        """

        # Dictionary structure: key = information about
        if (
            self.Clamps.data_mode in self.dataModel.ic_modes
            or self.Clamps.data_mode == "vc"
        ):
            data_template = self.data_template
        else:
            raise ValueError(
                "No data tempate for data mode: self.Clamps.data_mode=",
                self.Clamps.data_mode,
            )

        # summary table header is written anew for each cell
        htxt = ""
        if script_header:
            htxt = f"{'Cell':34s}\t{'Genotype':15s}\t{'Protocol':24s}\t"
            for k in list(data_template.keys()):
                cnv = "{:<%ds}" % (data_template[k][0])
                # print 'cnv: ', cnv
                htxt += (cnv + "\t").format(k)
            script_header = False
            htxt += "\n"

        ltxt = ""
        if "Genotype" not in list(self.analysis_summary.keys()):
            self.analysis_summary["Genotype"] = "Unknown"
        ltxt += f"{self.analysis_summary['CellID']:34s}\t{self.analysis_summary['Genotype']:15s}"
        ltxt += f"\t{self.analysis_summary['Protocol']:24s}\t"
        print(("AP1_Halfwidth: ", self.analysis_summary["AP1_HalfWidth"]))
        for a in list(data_template.keys()):
            if a in list(self.analysis_summary.keys()):
                txt = self.analysis_summary[a]
                if a in ["Description", "Notes"]:
                    txt = txt.replace("\n", " ").replace(
                        "\r", ""
                    )  # remove line breaks from output, replace \n with space
                # print a, data_template[a]
                if isinstance(txt, (float, int)):
                    ltxt += (data_template[a][1]).format(
                        txt * data_template[a][2]
                    ) + " \t"

                else:
                    ltxt += (data_template[a][1]).format(txt) + " \t"
            else:
                ltxt += ("{:>%ds}" % (data_template[a][0]) + "\t").format("NaN")
        ltxt = ltxt.replace("\n", " ").replace("\r", "")  # remove line breaks
        ltxt = htxt + ltxt
        if printnow:
            print(ltxt)

        if copytoclipboard:
            clipb = QAPP.clipboard()
            clipb.clear(mode=clipb.Clipboard)
            clipb.setText(ltxt, mode=clipb.Clipboard)

        return ltxt

    def dbStoreClicked(self):
        """
        Store data into the current database for further analysis
        """
        # self.updateAnalysis()
        if self.loaded is None:
            return
        self.dbIdentity = "IVCurve"  # type of data in the database
        db = self._host_.dm.currentDatabase()
        # print 'dir (db): ', dir(db)
        # print 'dir (db.db): ', dir(db.db)
        # print 'db.listTables: ', db.listTables()
        #
        table = self.dbIdentity

        columns = OrderedDict(
            [
                #            ('ProtocolDir', 'directory:Protocol'),
                ("AnalysisDate", "text"),
                ("ProtocolSequenceDir", "directory:ProtocolSequence"),
                ("Dir", "text"),
                ("Protocol", "text"),
                ("Genotype", "text"),
                ("Age", "text"),
                ("Sex", "text"),
                ("Temperature", "text"),
                ("Celltype", "text"),
                ("UseData", "int"),
                ("RMP", "real"),
                ("R_in", "real"),
                ("tau_m", "real"),
                ("iHold", "real"),
                ("PulseDuration", "real"),
                ("neg_cmd", "real"),
                ("neg_pk", "real"),
                ("neg_ss", "real"),
                ("h_tau", "real"),
                ("h_g", "real"),
                ("SpikeThreshold", "real"),
                ("AdaptRatio", "real"),
                ("FiringRate_1p5T", "real"),
                ("AP1_HalfWidth", "real"),
                ("AP1_Latency", "real"),
                ("AP2_HalfWidth", "real"),
                ("AP2_Latency", "real"),
                ("AHP_Depth", "real"),
                ("FI_Curve", "text"),
                ("IV_Curve_pk", "text"),
                ("IV_Curve_ss", "text"),
                ("FI_FZero", "real"),  #  ['Fzero', 'Ibreak', 'F1amp', 'F2amp', 'Irate']
                ("FI_Ibreak", "real"),
                ("FI_F1amp", "real"),
                ("FI_F2amp", "real"),
                ("FI_Irate", "real"),
            ]
        )

        if table not in db.tables:
            db.createTable(table, columns, owner=self.dbIdentity)
        try:
            z = self.tauh_neg_cmd
        except:
            self.tauh_neg_cmd = 0.0
            self.tauh_neg_pk = 0.0
            self.tauh_neg_ss = 0.0
            self.tauh_meantau = 0.0
            self.tau_Gh = 0.0

        if "Genotype" not in self.analysis_summary:
            self.analysis_summary["Genotype"] = "Unknown"
        #        print 'genytope: ', self.analysis_summary['Genotype']
        if (
            "Celltype" not in self.Script.analysis_parameters
            and self.analysis_summary["CellType"] == ""
        ):
            self.Script.analysis_parameters["Celltype"] = self.analysis_summary[
                "CellType"
            ]
        #        else:
        #            self.analysis_summary['CellType'] = self.Script.analysis_parameters['Celltype']

        data = {
            "AnalysisDate": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ProtocolSequenceDir": self.loaded,
            #            'ProtocolSequenceDir': self.dataModel.getParent(self.loaded, 'ProtocolSequence'),
            "Dir": self.loaded.parent().name(),
            "Protocol": self.loaded.name(),
            "Genotype": self.analysis_summary["Genotype"],
            "Age": self.analysis_summary["Age"],
            "Sex": self.analysis_summary["Sex"],
            "Temperature": self.analysis_summary["Temperature"],
            "Celltype": self.analysis_summary[
                "CellType"
            ],  # uses per cell info as available
            "UseData": 1,
            "RMP": self.RmTau.rmp / 1000.0,
            "R_in": self.r_in,
            "tau_m": self.RmTau.taum_taum,
            "iHold": self.analysis_summary["iHold"],
            "PulseDuration": self.analysis_summary["pulseDuration"],
            "AdaptRatio": self.adapt_ratio,
            "neg_cmd": self.RmTau.tauh_neg_cmd,
            "neg_pk": self.RmTau.tauh_neg_pk,
            "neg_ss": self.RmTau.tauh_neg_ss,
            "h_tau": self.analysis_summary["tauh"],
            "h_g": self.analysis_summary["Gh"],
            "SpikeThreshold": self.analysis_summary["SpikeThreshold"],
            "FiringRate": self.analysis_summary["FiringRate"],
            "FiringRate_1p5T": self.analysis_summary["FiringRate_1p5T"],
            "AP1_HalfWidth": self.analysis_summary["AP1_HalfWidth"],
            "AP1_Latency": self.analysis_summary["AP1_Latency"],
            "AP2_HalfWidth": self.analysis_summary["AP2_HalfWidth"],
            "AP2_Latency": self.analysis_summary["AP2_Latency"],
            "AHP_Depth": self.analysis_summary["AHP_Depth"],
            "FI_Curve": repr(
                self.analysis_summary["FI_Curve"].tolist()
            ),  # convert array to string for storage
            "IV_Curve_pk": repr(
                np.array(self.analysis_summary["IV_Curve_pk"]).tolist()
            ),
            "IV_Curve_ss": repr(
                np.array(self.analysis_summary["IV_Curve_ss"]).tolist()
            ),
            "FI_FZero": self.analysis_summary[
                "Fzero"
            ],  #',, 'Ibreak', 'F1amp', 'F2amp', 'Irate']
            "FI_Ibreak": self.analysis_summary["Ibreak"],
            "FI_F1amp": self.analysis_summary["F1amp"],
            "FI_F2amp": self.analysis_summary["F2amp"],
            "FI_Irate": self.analysis_summary["Irate"],
        }
        ## If only one record was given, make it into a list of one record
        if isinstance(data, dict):
            data = [data]
            ## Make sure target table exists and has correct columns, links to input file

        fields = db.describeData(data)
        ## override directory fields since describeData can't guess these for us
        #        fields['ProtocolDir'] = 'directory:Protocol'
        fields["ProtocolSequenceDir"] = "directory:ProtocolSequence"

        with db.transaction():
            db.checkTable(
                table,
                owner=self.dbIdentity,
                columns=fields,
                create=True,
                addUnknownColumns=True,
                indexes=[["ProtocolSequenceDir"],],
            )

            dirtable = db.dirTableName(
                self.loaded
            )  # set up the DirTable Protocol Sequence directory.
            if not db.hasTable(dirtable):
                db.createDirTable(self.loaded)

            # delete old
            for source in set([d["ProtocolSequenceDir"] for d in data]):
                db.delete(table, where={"ProtocolSequenceDir": source})

            # write new
            with pg.ProgressDialog("Storing IV Results..", 0, 100) as dlg:
                for n, nmax in db.iterInsert(table, data, chunkSize=30):
                    dlg.setMaximum(nmax)
                    dlg.setValue(n)
                    if dlg.wasCanceled():
                        raise HelpfulException(
                            "Scan store canceled by user.", msgType="status"
                        )
        # db.close()
        # db.open()
        print("Updated record for ", self.loaded.name())

    # ---- Helpers ----
    # Some of these would normally live in a pyqtgraph-related module, but are
    # just stuck here to get the job done.
    #
    @staticmethod
    def label_up(plot, xtext, ytext, title):
        """helper to label up the plot"""
        plot.setLabel("bottom", xtext)
        plot.setLabel("left", ytext)
        plot.setTitle(title)
