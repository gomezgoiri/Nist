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

import re
import csv
from argparse import ArgumentParser


def parse_file(filename, parsed_data={}, calculate_time_lapses=True):
    with open(filename, 'r') as f:
        prog = re.compile("^(\d),(\d),(\d),(\d+),(\d+)$", re.MULTILINE) #"^(\d),(\d),(\d),(\d+),(\d+)$"
        executions = prog.findall( f.read() )

        before_t = 0
        i = 0
        for execution in executions:
            eval_type =  "time" if execution[0] == "0" else "memory"
            when =  "after" if execution[1] == "0" else "before"
            prf_function = "HMAC_SHA1" if execution[2] == "0" else "HMAC_SHA256"
            num_bits_derived_key = execution[3]
            result_eval = execution[4] # free ram (MB) for "memory" and "millisecs" for "time".

            if eval_type not in parsed_data:
                parsed_data[eval_type] = {}

            if num_bits_derived_key not in parsed_data[eval_type]:
                parsed_data[eval_type][num_bits_derived_key] = {}

            if prf_function not in parsed_data[eval_type][num_bits_derived_key]:
                parsed_data[eval_type][num_bits_derived_key][prf_function] = {}

            if calculate_time_lapses and eval_type=="time":
                if when=="before":
                    before_t = int(result_eval)
                else: # "after"
                    if not parsed_data[eval_type][num_bits_derived_key][prf_function]:
                        parsed_data[eval_type][num_bits_derived_key][prf_function] = []
                    parsed_data[eval_type][num_bits_derived_key][prf_function].append( int(result_eval) - before_t )
                    if prf_function=="HMAC_SHA1" and (i==17 or i==18):
		      print before_t, int(result_eval)
            else:
                if when not in parsed_data[eval_type][num_bits_derived_key][prf_function]:
                    parsed_data[eval_type][num_bits_derived_key][prf_function][when] = []
                parsed_data[eval_type][num_bits_derived_key][prf_function][when].append( int(result_eval) )
            i+=1
    return parsed_data


def parse_mWatt_data(csvpath, from_t=0, to_t=-1, watts_row = 1):
    reader = csv.reader(open(csvpath, 'rb'), delimiter=',')
    x = []
    y = []
    line = 0
    for row in reader:
	if line<3:
	    line += 1
	else:
	    #print row
	    t = float(row[0])
	    if t>=from_t:
		if to_t>=0 and t>to_t: # to_t<0 => a way to say: till the end!
		    break # exit
		# else
		x.append(t)
		y.append(row[watts_row])
	   
    return x,y


if __name__ == '__main__':
    argp = ArgumentParser()
    argp.add_argument('-rs','--results', default="../results", dest='results_path',
                    help='Specify the folder containing the result files to parse.')
    argp.add_argument('-f','--file', default="/duemilanove/binary_100loops_128_timing.txt", dest='analysis_file',
                    help='Specify the specific file to analyse.')
    args = argp.parse_args()

    parsed_data = parse_file( args.results_path + args.analysis_file )

    print parsed_data
