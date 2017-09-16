# coding: UTF-8

import importlib
import os

import wx

from const import *
from controlpanel import ControlPanel
from matplotplanel import MatplotPanel



class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, parent=None, title=TITLE,
                      size=(WIDTH, HEIGHT),
                      style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                            wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION |
                            wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_SHAPED)
    self.SetBackgroundColour("black")
    self.SetMinClientSize((192, 108))
    self.Center()
    
    menu_bar = wx.MenuBar()
    menu_file = wx.Menu()
    file_open = wx.MenuItem(id=wx.ID_OPEN, text="&Open file\tCtrl+O",
                            help="Open a file with explorer",
                            kind=wx.ITEM_NORMAL)
    file_close = wx.MenuItem(id=wx.ID_EXIT, text="&Close\tCtrl+C",
                             help="Close the application", kind=wx.ITEM_NORMAL)
    menu_file.AppendItem(file_open)
    menu_file.AppendItem(file_close)
    menu_bar.Append(menu=menu_file, title="&File")
    self.SetMenuBar(menu_bar)
    
    self.Bind(wx.EVT_MENU, self.onQuit, file_close)
    self.Bind(wx.EVT_MENU, self.onOpenFile, file_open)
    
    self.dlg = wx.FileDialog(self, message="Choose a file",
                             defaultDir=os.getcwd(), defaultFile="",
                             wildcard=FILE_TYPES,
                             style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)
    
    self.main_panel = MainPanel(parent=self)
    self.main_box = wx.BoxSizer()
    self.main_box.Add(item=self.main_panel, proportion=1, flag=wx.EXPAND)
    self.SetSizer(self.main_box)
    
    self.status_bar = self.CreateStatusBar(style=wx.BORDER_SUNKEN)
    self.SetStatusText("Initialized")
  
  
  def onOpenFile(self, event):
    if self.dlg.ShowModal() == wx.ID_OK:
      self.file_path = self.dlg.GetPath()
      self.SetStatusText("You chose following file: " + self.file_path)
  
  
  def onQuit(self, event):
    self.dlg.Destroy()
    self.Close()



class MainPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
    self.SetBackgroundColour("white")
    
    self.init = True
    
    # control panel for user interaction
    self.control_panel = ControlPanel(self)
    
    self.file_path = u'E:\\GitHub\\pythogram\\[HQ] Toms Diner --- Susanne ' \
                     u'Vega.wav'
    
    # create sine signal and spectrum
    # self.signal = Sine(freq=7648.0, l=10.0, amp=1.0, srate=44100)
    # self.signal = File(self.file_path)
    # self.signal = WNoise()
    
    self.createMatplotPanels()
    
    # the main box sizer
    self.main_vbox = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.main_vbox)
    
    # top left box for control panel
    self.top_left_box = wx.BoxSizer()
    self.top_left_box.Add(item=self.control_panel, proportion=1, flag=wx.EXPAND)
    
    # top right box for signal and spectrum
    self.top_right_vbox = wx.BoxSizer(wx.VERTICAL)
    self.top_right_vbox.Add(item=self.matplot_panel1, proportion=1,
                            flag=wx.EXPAND)
    self.top_right_vbox.Add(item=self.matplot_panel2, proportion=1,
                            flag=wx.EXPAND)
    
    # top box containing control panel, signal and spectrum
    self.top_hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.top_hbox.Add(item=self.top_left_box, proportion=3, flag=wx.EXPAND)
    self.top_hbox.Add(item=self.top_right_vbox, proportion=2, flag=wx.EXPAND)
    
    # bottom box for spectrogram
    self.bottom_box = wx.BoxSizer()
    self.bottom_box.Add(item=self.matplot_panel3, proportion=1, flag=wx.EXPAND)
    
    # all together in main box
    self.main_vbox.Add(item=self.top_hbox, proportion=6, flag=wx.EXPAND)
    self.main_vbox.Add(item=self.bottom_box, proportion=5, flag=wx.EXPAND)
  
  
  def createMatplotPanels(self):
    # plot the signal
    self.matplot_panel1 = MatplotPanel(parent=self, xlim=(0.0, 1.0),
                                       # ylim=(-1.0, 1.0),
                                       title='Signal',
                                       xlabel='Time in seconds (s)',
                                       ylabel='Amplitude')
    # spectrum
    self.matplot_panel2 = MatplotPanel(parent=self, xlim=(20, 24000),
                                       # ylim=(0, 1e6),
                                       title='Spectrum',
                                       xlabel='Frequency in hertz (Hz)',
                                       ylabel='Amplitude in decibel '
                                              'relative\n to full scale (db '
                                              'FS)')
    # spectrogram
    self.matplot_panel3 = MatplotPanel(parent=self, title='Spectrogram',
                                       xlabel='Time in seconds (s)',
                                       ylabel='Frequency in hertz ('
                                              'Hz)')
  
  
  def plotSignal(self, signal=None):
    # plot the signal
    self.matplot_panel1 = self.matplot_panel1.plot(signal=signal)
    # spectrum
    self.matplot_panel2 = self.matplot_panel2.plotSpectrum(signal=signal)
    # spectrogram
    self.matplot_panel3 = self.matplot_panel3.plotSpectrogram(signal=signal)
  
  
  def changeSignal(self, signal, f=440.0, l=10.0, amp=1.0, fs=44100, path=None):
    if signal is None or path is None:
      return
    try:
      signals_module = importlib.import_module('.signals', 'pythogram')
      try:
        if signal in ["Sine", "Square", "Sawtooth", "Triangle"]:
          self.signal = getattr(signals_module, signal)(freq=f, l=l, amp=amp,
                                                        srate=fs)
        elif signal == "WNoise":
          self.signal = getattr(signals_module, signal)(l=l, amp=amp, srate=fs)
        
        elif signal == "File" and path is not None:
          self.signal = getattr(signals_module, signal)(path)
      except AttributeError:
        print("Class does not exist")
    except ImportError:
      print("Module does not exist")
    
    self.plotSignal(self.signal)
    self.setInformation(self.signal)
  
  
  def setInformation(self, signal):
    if self.control_panel is not None:
      self.control_panel.output_fs.SetValue(signal.sample_rate)
      self.control_panel.output_len.SetValue(signal.length)
