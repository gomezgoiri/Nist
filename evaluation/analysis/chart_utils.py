# -*- coding: utf-8 -*-
'''
 Copyright (C) 2012 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

import matplotlib.pyplot as plt
import matplotlib

class ChartImprover(object):
    
    def __init__( self,
                  title = None,
                  xlabel = None,
                  ylabel = {'label': None, 'x':0, 'y': 0 },
                  line_width = 3,
                  legend_from_to = (0.12, 0.78),
                  font_size = 18.0 ):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self._configure_matplotlib(line_width, font_size)
        self.legend_from = legend_from_to[0]
        self.legend_to = legend_from_to[1]
    
    # should be called before making the chart
    def _configure_matplotlib(self, line_width, font_size):
        # http://matplotlib.org/users/customizing.html
        
        # It is important that in order this fonts to be suitable, the height should be 6
        # the default figure.figsize: 8, 6
        
        # change font sizes
        matplotlib.rcParams.update({'font.size': font_size})
        # Relative to the font size:
        # 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', 'larger', or 'smaller'        
        matplotlib.rcParams.update({'axes.titlesize': 'large'})   # fontsize of the axes title
        matplotlib.rcParams.update({'axes.labelsize': 'large'})  # fontsize of the x any y labels
        
        matplotlib.rcParams.update({'xtick.labelsize': 'medium'})
        matplotlib.rcParams.update({'ytick.labelsize': 'medium'})
        
        matplotlib.rcParams.update({'legend.fontsize': 'medium'})
        matplotlib.rcParams.update({'legend.handletextpad': 0.25})        
        
        # change paddings for ticks
        matplotlib.rcParams['xtick.major.pad']='12'
        matplotlib.rcParams['ytick.major.pad']='12'
        
        # Line thickness
        matplotlib.rcParams['lines.linewidth'] = line_width

    def improve_following_guidelines(self, ax): # from the Wall Street Journal "Guide to Information Graphics"
        #ax.legend(handles, labels, loc="upper right")
        # using strings with loc (e.g. loc = "upper left") is also valid
        _, labels = ax.get_legend_handles_labels()
        leg = ax.legend( bbox_to_anchor = (self.legend_from, 1.1, self.legend_to, .102), loc=3, ncol=len(labels), mode="expand", borderaxespad=0)
        if leg is not None: # we got labels to create a legend
            leg.get_frame().set_alpha(0)
        
        # add some labels to the chart
        if self.title is not None: plt.title( self.title )
        if self.xlabel is not None: plt.xlabel( self.xlabel, labelpad=20 )
        if self.ylabel is not None and self.ylabel['label'] is not None:
            plt.ylabel( self.ylabel['label'], rotation='horizontal' )# verticalalignment="top")
            ax.yaxis.set_label_coords( self.ylabel['x'], self.ylabel['y'] )
        #plt.xlabel(self.xlabel, labelpad=20)
        
        # Just horizontal grid line and in the foreground
        #ax.grid(True)
        ax.yaxis.grid( True )
        ax.xaxis.grid( False )
        ax.set_axisbelow( True )
        
        # from: http://stackoverflow.com/questions/9126838/how-to-simultaneously-remove-top-and-right-axes-and-plot-ticks-facing-outwards
        
        #do not display top and right axes
        #comment to deal with ticks
        ax.spines["left"].set_visible( False )
        ax.spines["right"].set_visible( False )
        ax.spines["top"].set_visible( False )
        
        # omit ticks
        # the OP way (better):
        ax.tick_params( axis='both', direction='out' )
        ax.get_xaxis().tick_bottom() # remove unneeded ticks 
        ax.get_yaxis().tick_left()