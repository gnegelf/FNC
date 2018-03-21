#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:55 2018

@author: fabiangnegel
"""
seeds=range(1,12)
dupRanges={'small':[5,15],'medium':[15,25],'large':[20,50]}
#dupRanges={'medium':[15,25]}
#bounds={'cat':[6,1,0],'mixed':[3,1,6]}
bounds={'num':[0,0,8],'cat':[8,1,0],'mixed':[3,1,6]}

for seed in seeds:
    for key1,dupRange in dupRanges.iteritems():
        for key2,boundAmount in bounds.iteritems():
            fh= open("parameter_configurations/"+key1+"_"+key2+"_seed_%d" % seed,"w")
            lines_of_text=[]
            lines_of_text.append("supplyAmount: %d\n" % 6)
            lines_of_text.append("taskAmount: %d\n" % 50)
            lines_of_text.append("cateAmount: %d\n" % 7)
            lines_of_text.append("baseAmount: %d\n" % 8)
            lines_of_text.append("type1amount: %d\n" % 40)
            lines_of_text.append("type2amount: %d\n" % 6)
            lines_of_text.append("type3amount: %d\n" % 7)
            lines_of_text.append("duplicateRange: %d %d\n" % (dupRange[0],dupRange[1]))
            lines_of_text.append("catValAmount: %d\n" % boundAmount[0])
            lines_of_text.append("catDivAmount: %d\n" % boundAmount[1])
            lines_of_text.append("numAmount: %d\n" % boundAmount[2])
            lines_of_text.append("seed: %d\n" % seed)
            fh.writelines(lines_of_text)
            fh.close()
            
