# -*- coding: utf-8 -*-
'''
 Copyright (C) 2014 onwards University of Deusto

 All rights reserved.

 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.

 This software consists of contributions made by many individuals,
 listed below:

 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from argparse import ArgumentParser
from parser import parse_mWatt_data

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from chart_utils import ChartImprover


class DiagramGenerator:
    
    def __init__(self, title, data):
        
        # http://colorschemedesigner.com/previous/colorscheme2/index-es.html?tetrad;100;0;225;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0
        self.linesColors = ("#E6AC73", "#CFE673", "#507EA1", "#E67373", "#8A458A")
        # self.linesShapes = ('xk-','+k-.','Dk--') # avoiding spaghetti lines
        self.ci = ChartImprover( title = None, # title,
                                 xlabel = 'Key length (bits)',
                                 ylabel = {"label": 'Time (ms)', "x": -0.02, "y": 1.1},
                                 legend_from_to = (0.04, 1.0) )
        self.generate(data)
            
    def generate(self, data):
        fig = plt.figure( figsize=(10, 6) )
	ax = fig.add_subplot(111)
	
	colors = cycle(self.linesColors)
	
	ax.plot(data[0], data[1], 'k-',
		color = colors.next())
	handles, labels = ax.get_legend_handles_labels()
	#ax.legend(handles, labels, loc='best')
	#ax.set_xlim(0)
	#ax.set_ylim(0)
	
        self.ci.improve_following_guidelines(ax)
    
    def show(self):
        plt.show()
    
    def save(self, filename):
        plt.savefig(filename, bbox_inches='tight')


if __name__ == '__main__':
    argp = ArgumentParser()
    argp.add_argument('-rs','--results', default="../results", dest='results_path',
                    help='Specify the folder containing the result files to parse.')
    args = argp.parse_args()
    
    parsed_data = parse_mWatt_data( args.results_path + "/energy/allKeysSize_current.csv", from_t=10, to_t=15 )
    d = DiagramGenerator("Time needed", parsed_data)
    d.save('/tmp/current_kdfs.svg')