import matplotlib.pyplot as plt

def use_my_rcparam():
  # big plots: 1 plot per page
  plt.rcParams.update({
    'font.size'        : 8, 
    'figure.facecolor' : 'w',
    'figure.dpi'       : 2000,
    'figure.figsize'   : (6,3),
    # basic properties
    'axes.linewidth'   : 0.5,
    'xtick.top'        : True,
    'xtick.direction'  : 'in',
    'xtick.major.size' : '2',
    'xtick.major.width': '0.5',
    'ytick.right'      : True,
    'ytick.direction'  : 'in',
    'ytick.major.size' : '2',
    'ytick.major.width': '0.5', 
    'axes.grid'        : True,
    'grid.linewidth'   : '0.5',
    'legend.fancybox'  : False,
    'legend.framealpha': 1,
    'legend.edgecolor' : 'black',
    # case dependent
    'axes.autolimit_mode': 'round_numbers', # 'data' or 'round_numbers'
    'lines.linewidth'  : 1,
    'lines.markersize' : 3,
  })
  # small plots: 2 plot per page
  # plt.rcParams.update({
  #   'font.size'        : 9, 
  #   'font.weight'      : 'bold', 
  #   'figure.facecolor' : 'w',
  #   'figure.dpi'       : 400,
  #   'figure.figsize'   : (4,3),
  #   # basic properties
  #   'axes.linewidth'   : 1,
  #   'xtick.top'        : True,
  #   'xtick.direction'  : 'in',
  #   'xtick.major.size' : '3',
  #   'xtick.major.width': '1',
  #   'ytick.right'      : True,
  #   'ytick.direction'  : 'in',
  #   'ytick.major.size' : '3',
  #   'ytick.major.width': '1', 
  #   'axes.grid'        : True,
  #   'grid.linewidth'   : '1',
  #   'legend.fancybox'  : False,
  #   'legend.framealpha': 1,
  #   'legend.edgecolor' : 'black',
  #   # case dependent
  #   'axes.autolimit_mode': 'round_numbers', # 'data' or 'round_numbers'
  #   'lines.linewidth'  : 1,
  #   'lines.markersize' : 6,
  # })

class my_default_color_list:
  def __init__(self):
    self.colors = ['#1f77b4',
                  '#ff7f0e',
                  '#2ca02c',
                  '#d62728',
                  '#9467bd',
                  '#8c564b',
                  '#e377c2',
                  '#7f7f7f',
                  '#bcbd22',
                  '#17becf',
                  '#1a55FF']

  def __len__(self):
    return len(self.colors)

  def __getitem__(self, slice):
      return self.colors[slice]
