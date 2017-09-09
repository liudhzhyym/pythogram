import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab
# import matplotlib as mpl
import wx
from matplotlib.backends.backend_wxagg import (
  FigureCanvasWxAgg as FigureCanvas,
  NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure



class MatplotPanel(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER, grid=True, ylim=None,
               title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style)
    
    # figure
    self.figure = Figure(tight_layout=True)
    self.axes = self.figure.add_subplot(111)
    # just a recommended style
    plt.style.use('ggplot')
    
    # our custom color map for spectrogram
    self.cmap = LinearSegmentedColormap(name='Custom',
                                        segmentdata={'red'  : [(0.0, 0.0, 0.0),
                                                               (0.7, 1.0, 1.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'green': [(0.0, 0.0, 0.0),
                                                               (0.7, 0.0, 0.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'blue' : [(0.0, 0.0, 0.0),
                                                               (0.7, 0.0, 0.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'alpha': [(0.0, 0.0, 0.0),
                                                               (0.5, 0.0, 1.0),
                                                               (1.0, 1.0, 1.0)]
                                                     })
    
    # grid?
    if grid:
      self.axes.grid(True)
    else:
      self.axes.grid(False)
    # limits on y?
    if ylim:
      self.axes.set_ylim(ylim)
    # title?
    if title:
      self.axes.set_title(title)
    # label on x?
    if xlabel:
      self.axes.set_xlabel(xlabel)
    # label on y?
    if ylabel:
      self.axes.set_ylabel(ylabel)
    
    # canvas for integration in wxPython
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    # vertical box with toolbar and figure canvas
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.v_box)
    self.v_box.Add(item=self.toolbar, proportion=1, flag=wx.EXPAND)
    # self.v_box.AddSpacer(4)
    self.v_box.Add(item=self.canvas, proportion=1,
                   flag=wx.GROW)
  
  
  def plot(self, x, y):
    self.axes.plot(x, y)
    return self
  
  
  def semilogx(self, x, y):
    self.axes.semilogx(x, y)
    return self
  
  
  def spectrogram(self, x, fs):
    pxx, freq, t, im = self.axes.specgram(x=x, Fs=fs, cmap='plasma')
    # pxx, freq, t = mlab.specgram(x=x, Fs=fs, NFFT=512)
    # self.axes.pcolormesh(t, freq, pxx, cmap=mpl.cm.hot)
    self.axes.set_yscale('symlog')
    # self.axes.imshow(x)
    self.figure.colorbar(im).set_label('Intensity [dB]')
    return self
