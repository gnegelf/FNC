#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:07:30 2018

@author: fabiangnegel
"""
import numpy as np
import scipy
import cplex
from cplex.exceptions import CplexSolverError
seeds=range(1,6)
dupRanges={'small':[5,15],'medium':[15,25],'large':[20,50]}
#dupRanges={'small':[5,15],'large':[20,50]}
#bounds={'cat':[10,1,0],'mixed':[10,1,8]}
solDict={}
solTimes={}
#seeds=range(7,12)
#dupRanges={'medium':[15,25]}
bounds={'num':[0,0,8],'cat':[6,1,0],'mixed':[3,1,6]}
#bounds={'cat':[6,1,0]}
#bounds={'num':[0,0,8]}
#dupRanges={'large':[20,50]}
for ending in ['_friction_DA_I']:
    for key1,dupRange in dupRanges.iteritems():
        for key2,boundAmount in bounds.iteritems():
            times=[]
            seedList=[]
            gapList=[]
            seeds=range(1,6)
            #if key1=='small' and (key2=='cat' or key2 == 'mixed'):
            #    seeds=range(2,7)
            #if key1=='medium' and (key2=='cat' or key2 == 'mixed'):
            #    seeds=[1,3,8,9,10]
            #if key1=='large' and (key2=='cat' or key2 == 'mixed'):
            #    seeds=[1,2,3,4,7]
            for seed in seeds:
                model=cplex.Cplex()
                #filename=key1+"_"+key2+"_seed_%d" % seed+'_no_friction'
                filename=key1+"_"+key2+"_seed_%d" % seed+ending
                model.read("lpfiles/"+filename+".lp")
                model.set_results_stream('logs/'+filename+'.rlog')
                model.parameters.timelimit.set(3600.0)
                #model.parameters.threads(1)
                start=model.get_time()
                try:
                    model.solve()
                    end=model.get_time()
                    status=model.solution.get_status()
                    duration=end-start
                    fh = open('logs/'+filename+'.rlog','a')
                    fh.write("\n"+model.solution.get_status_string())
                    fh.close()
                    if (status == 101 or status== 102):
                        times.append(duration)
                        gapList.append(model.solution.MIP.get_mip_relative_gap())
                    else:
                        if duration < 3600:
                            times.append(-duration)
                            gapList.append(-1)
                        else:
                            times.append(duration)
                            gapList.append(model.solution.MIP.get_mip_relative_gap())
                    seedList.append(seed)
                except CplexSolverError, exc:
                    print "** Exception: ",exc
                #fh = open('logs/'+filename+'.rlog','a')
                #fh.write("\n"+str(model.solution.get_objective_value()))
                #fh.close()
            gapArray=np.transpose(np.array([gapList]))
            seedArray=np.transpose(np.array([seedList]))
            timeArray=np.transpose(np.array([times]))
            scipy.io.savemat('times/'+key1+'_'+key2+ending+'2',dict([('times2',timeArray),('seeds2',seedArray),('gaps2',gapArray)]))

#scipy.io.savemat('/Users/fabiangnegel/MIPDECO/Feuerprojekt/Results/contaStateFullxn%dtn%ds%d.mat' % (xn,tn,5), dict([('x_k',x),('duration',duration),('objective',model.solution.get_objective_value()),('gap',model.solution.MIP.get_mip_relative_gap())])) 