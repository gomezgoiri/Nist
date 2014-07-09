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
        self.linesColors = ("#E6AC73", "#CFE673", "#507EA1", "#E67373", "#8A458A")
        # self.linesShapes = ('xk-','+k-.','Dk--') # avoiding spaghetti lines
        self.ci = ChartImprover( title = None, # title,
                                 xlabel = 'Key length (bits)',
                                 ylabel = {"label": 'Memory used (KB)', "x": -0.02, "y": 1.1},
                                 legend_from_to = (0.04, 1.0) )
        self.generate(data)
    
    def get_line_data(self, data, key_length_order):
	names = []
	means = []
        std_devs = []
        #for key_length in data:
        for key_length in key_length_order:
	  names.append( key_length )
	  for algo in data[key_length]: # just one
	    repetitions = data[key_length][algo]["after"]
	    means.append( np.average(repetitions) )
            std_devs.append( np.std(repetitions) )
        return names, means, std_devs
            
    def generate(self, data):
	fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(1,1,1)
        
        devices_names = data.keys()
        groups_names = ["128", "256", "512"]
        ind = range(1, len(groups_names)+1) # the x locations for the groups
        width = 0.3 # the width of the bars
        colors = cycle(self.linesColors)
        
        _, avg, dev = self.get_line_data( data[devices_names[0]], groups_names )        
        ax.bar( ind, avg, width,
                yerr = dev,
                color = colors.next(),
                #ecolor='black',
                edgecolor = 'none',
                label = "duemilanove"
        )
        
        _, avg, dev = self.get_line_data( data[devices_names[1]], groups_names )
        ax.bar( [i + width for i in ind], avg, width,
                yerr = dev,
                color = colors.next(),
                #ecolor='black',
                edgecolor = 'none',
                label = "mega"
        )
        
        plt.xticks( [i+width for i in ind], groups_names)
        
        ax.set_xlim(0.5, len(groups_names)+1)
        ax.set_ylim(0)
        
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
    
    merged_data = {}

    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_128_memory.txt" )
    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_256_memory.txt", parsed_data )
    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_512_memory.txt", parsed_data )
    merged_data["duemilanove"] = parsed_data["memory"]
    
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_128_memory.txt" )
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_256_memory.txt", parsed_data )
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_512_memory.txt", parsed_data )
    merged_data["mega"] = parsed_data["memory"]
    
    d = DiagramGenerator("Time needed", merged_data)
    d.save('/tmp/memory_kdfs.pdf')