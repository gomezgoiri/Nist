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
    
    NB_CACHING_1C = 'caching_1'
    NB_CACHING_100C = 'caching_100'
    OURS_1C = 'ours_1'
    OURS_10C = 'ours_10'
    OURS_100C = 'ours_100'
    NB = 'nb'
    NUM_NODES = 'num_nodes'
    REQUESTS = 'requests'
    
    '''
      {
        'ours_1': { 'num_nodes': [1,10,50,100,200], 'requests': [[105,100,85],[140,120,130],[376,400,406],[338,320,355],[495,500,505]] },
        'ours_10': { 'num_nodes': [10,50,100,200], 'requests': [[223,220,221],[507,500,510],[430,420,420],[580,600,660]] },
        'ours_100': { 'num_nodes': [100,200], 'requests': [[480,500,520],[640,700,740]] },
        'nb': { 'num_nodes': [1,10,50,100,200], 'requests': [[320,300,340],[420,400,380],[540,600,630],[690,720,710],[880,900,912]] }
      }
    '''
    def __init__(self, title, data):
        
        # http://colorschemedesigner.com/previous/colorscheme2/index-es.html?tetrad;100;0;225;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0.3;-0.8;0.3;0.5;0.1;0.9;0.5;0.75;0
        self.linesColors = ("#E6AC73", "#CFE673", "#507EA1", "#E67373", "#8A458A")
        # self.linesShapes = ('xk-','+k-.','Dk--') # avoiding spaghetti lines
        self.ci = ChartImprover( title = None, # title,
                                 xlabel = 'Key length (bits)',
                                 ylabel = {"label": 'Time (ms)', "x": -0.02, "y": 1.1},
                                 legend_from_to = (0.04, 1.0) )
        # from worst to best
        # desired_order = ( DiagramGenerator.NB,
        #                   DiagramGenerator.NB_CACHING_100C,
        #                   DiagramGenerator.OURS_100C,
        #                   DiagramGenerator.OURS_10C,
        #                   DiagramGenerator.OURS_1C,
        #                   DiagramGenerator.NB_CACHING_1C )
        self.generate(data)
    
    def get_line_data(self, data, key_length_order):
	names = []
	means = []
        std_devs = []
        #for key_length in data:
        for key_length in key_length_order:
	  names.append( key_length )
	  for algo in data[key_length]: # just one
	    repetitions = data[key_length][algo]
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

def mainTest():
    json_txt = '''
      {
        'ours_1': { 'num_nodes': [1,10,50,100,200], 'requests': [[105,100,85],[140,120,130],[376,400,406],[338,320,355],[495,500,505]] },
        'ours_10': { 'num_nodes': [10,50,100,200], 'requests': [[223,220,221],[507,500,510],[430,420,420],[580,600,660]] },
        'ours_100': { 'num_nodes': [100,200], 'requests': [[480,500,520],[640,700,740]] },
        'nb': { 'num_nodes': [1,10,50,100,200], 'requests': [[320,300,340],[420,400,380],[540,600,630],[690,720,710],[880,900,912]] }
      }
        '''
    json_txt = json_txt.replace(' ','')
    json_txt = json_txt.replace('\n','')
    json_txt = json_txt.replace('\t','')
    
    d = DiagramGenerator("Network usage by strategies", eval(json_txt))
    d.save('/tmp/test_diagram.pdf')

def main():    
    f = open('/tmp/requests_by_strategies.json', 'r')
    json_txt = f.read()
    f.close()
    
    d = DiagramGenerator("Network usage by strategies", eval(json_txt))
    d.save('/tmp/requests_by_strategies.svg')


if __name__ == '__main__':
    argp = ArgumentParser()
    argp.add_argument('-rs','--results', default="../results", dest='results_path',
                    help='Specify the folder containing the result files to parse.')
    args = argp.parse_args()
    
    merged_data = {}

    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_128_timing.txt" )
    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_256_timing.txt", parsed_data )
    parsed_data = parse_file( args.results_path + "/duemilanove/binary_100loops_512_timing.txt", parsed_data )
    merged_data["duemilanove"] = parsed_data["time"]
    
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_128_timing.txt" )
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_256_timing.txt", parsed_data )
    parsed_data = parse_file( args.results_path + "/mega_adk/binary_100loops_512_timing.txt", parsed_data )
    merged_data["mega"] = parsed_data["time"]
    
    d = DiagramGenerator("Time needed", merged_data)
    d.save('/tmp/time_kdfs.pdf')