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
from parser import parse_file

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from chart_utils import ChartImprover


class DiagramGenerator:
  
    def __init__(self, title, data):
        
        # http://colorschemedesigner.com/previous/colorscheme2/index-es.html?tetrad;100;0;225;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0
        self.linesColors = ("#2E8199", "#73CCE6", "#996735", "#E6AC73")
        # self.linesShapes = ('xk-','+k-.','Dk--') # avoiding spaghetti lines
        self.ci = ChartImprover( title = None, # title,
                                 xlabel = 'Key length (bits)',
                                 ylabel = {"label": '# of information sets', "x": -0.02, "y": 1.1},
                                 legend_from_to = (0.04, 1.0) )
	
	fig = plt.figure(figsize=(18,6))
        ax1 = fig.add_subplot(1,2,1)
        ax2 = fig.add_subplot(1,2,2)
        
        self.generate(ax1, data["uno"])
        self.generate(ax2, data["mega"])
            
    def generate(self, ax, data):
	#fig = plt.figure(figsize=(10, 6))
        #ax = fig.add_subplot(1,1,1)
        
        devices_names = data.keys()
        groups_names = ["128", "256", "512"]
        ind = range(1, len(groups_names)+1) # the x locations for the groups
        width = 0.3 # the width of the bars
        colors = cycle(self.linesColors)
        
        simples_avg = data["simple"]["sram"]    
        ax.bar( ind, simples_avg, width,
                color = colors.next(),
                edgecolor = 'none',
                label = "ssram"
        )
	        
        simplee_avg = data["simple"]["eeprom"]     
        ax.bar( ind, simplee_avg, width,
                color = colors.next(),
                edgecolor = 'none',
                label = "seeprom",
                bottom = simples_avg
        )
        
        caches_avg = data["cachingKeys"]["sram"]
        ax.bar( [i + width for i in ind], caches_avg, width,
                color = colors.next(),
                edgecolor = 'none',
                label = "csram"
        )
	
	cachee_avg = data["cachingKeys"]["eeprom"]
        ax.bar( [i + width for i in ind], cachee_avg, width,
                color = colors.next(),
                edgecolor = 'none',
                label = "ceeprom",
                bottom = caches_avg
        )
        
        plt.sca( ax )
        plt.xticks( [i+width for i in ind], groups_names)
        
        ax.set_xlim(0.5, len(groups_names)+1)
        ax.set_ylim(0)
        
        self.ci.improve_following_guidelines(ax)
        plt.ylim((0,480))
    
    def show(self):
        plt.show()
    
    def save(self, filename):
        plt.savefig(filename, bbox_inches='tight')


if __name__ == '__main__':
    argp = ArgumentParser()
    argp.add_argument('-rs','--results', default="../results", dest='results_path',
                    help='Specify the folder containing the result files to parse.')
    args = argp.parse_args()
    
    data = {"uno": {"simple" : {}, "cachingKeys": {}}, "mega": {"simple" : {}, "cachingKeys": {}}}
    
    # Arduino Uno
    data["uno"]["simple"]["sram"] = (26, 24, 20)
    data["uno"]["simple"]["eeprom"] = (64, 64, 64)
    data["uno"]["cachingKeys"]["sram"] = (13, 8, 5)
    data["uno"]["cachingKeys"]["eeprom"] = (20, 12, 7)
    
    # Arduino Mega
    data["mega"]["simple"]["sram"] = (191, 189, 186)
    data["mega"]["simple"]["eeprom"] = (256, 256, 256)
    data["mega"]["cachingKeys"]["sram"] = (92, 63, 38)
    data["mega"]["cachingKeys"]["eeprom"] = (81, 49, 28)
    
    d = DiagramGenerator("Memory needed", data)
    d.save('/tmp/memory-eval.svg')
