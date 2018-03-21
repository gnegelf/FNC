#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:22:58 2018

@author: fabiangnegel
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:24:42 2018

@author: fabiangnegel
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import random
import cplex
from cplex.exceptions import CplexSolverError
import re
class JCType(object):
    def __init__(self,supplyprob,taskprob):
        
        self.supplyprob=supplyprob
        self.taskprob=taskprob


class JC(object):
    def __init__(self,attributes,values):
        self.values=values
        #self.attributes=attributes
        
class Attribute(object):
    def __init__(self,attrType,valRange=None,values=None,fm=None,fs=None,intensity=None,fp=None):
        self.type=attrType
        self.values=values
        self.frictionMultiplier=fm
        self.frictionSteps=fs
        self.frictionPerc=fp
        self.range=valRange
        self.intensity=intensity
 

class SupDemCond(object):
    def __init__(self,attributesL,valuesL,attributesR,valuesR):
        self.valuesL=valuesL
        self.attributesR=attributesR
        self.valuesR=valuesR
        self.attributesL=attributesL

class CondBounds(object):
    def __init__(self,attributes,values):
        self.values=values
        self.attributes=attributes

class CatDivBound(object):
    def __init__(self,attribute,attributeId,bound,typ):
        self.bound=bound
        self.attribute=attribute
        self.attributeId=attributeId
        self.type=typ

class CatValBound(object):
    def __init__(self,attribute,attributeId,bound,typ,valueId):
        self.bound=bound
        self.attribute=attribute
        self.attributeId=attributeId
        self.valueId=valueId
        self.type=typ

class NumBound(object):
    def __init__(self,attribute,attributeId,bound,typ):
        self.bound=bound
        self.attribute=attribute
        self.attributeId=attributeId
        self.type=typ

class ForcedInclusion(object):
    def __init__(self,jc):
        self.jc=jc

class ObjectiveCoefficient(object):
    def __init__(self,typ,value):
        self.value=value
        self.type=typ

class Configuration(object):
    def __init__(self, name=None):
        self.name=name
    def read(self,path):
        print "reading: "+path
        file = open(path, "r")
        distances_data = file.read()
        file.close()
        
        entries = re.split("\n+", distances_data)
        
        
        for line in entries:
            if re.search(".*supplyAmount: [0-9]+",line):
                self.supplyAmount=int(re.split(" ",line)[1])
                self.demandAmount=self.supplyAmount
            if re.search(".*taskAmount: [0-9]+",line):
                self.taskAmount=int(re.split(" ",line)[1])
            if re.search(".*cateAmount: [0-9]+",line):
                self.cateAmount=int(re.split(" ",line)[1])
            if re.search(".*baseAmount: [0-9]+",line):
                self.baseAmount=int(re.split(" ",line)[1])
            if re.search(".*type1amount: [0-9]+",line):
                self.type1amount=int(re.split(" ",line)[1])
            if re.search(".*type2amount: [0-9]+",line):
                self.type2amount=int(re.split(" ",line)[1])
            if re.search(".*type3amount: [0-9]+",line):
                self.type3amount=int(re.split(" ",line)[1])
            if re.search(".*duplicateRange: [0-9]+ [0-9]+",line):
                self.duplicateRange=[int(re.split(" ",line)[1]),int(re.split(" ",line)[2])]
            if re.search(".*catDivAmount: [0-9]+",line):
                self.catDivAmount=int(re.split(" ",line)[1])
            if re.search(".*catValAmount: [0-9]+",line):
                self.catValAmount=int(re.split(" ",line)[1])
            if re.search(".*numAmount: [0-9]+",line):
                self.numAmount=int(re.split(" ",line)[1])
            if re.search(".*seed: [0-9]+",line):
                self.seed=int(re.split(" ",line)[1])

#_____________
#Read parameters
#_____________



seeds=range(1,6)
dupRanges={'small':[5,15],'medium':[15,25],'large':[20,50]}
#dupRanges={'small':[5,15],'large':[20,50]}

boundos={'num':[0,0,8],'cat':[6,1,0],'mixed':[3,1,6]}
#boundos={'cat':[6,1,0],'mixed':[3,1,6]}
#dupRanges={'medium':[15,25]}
#boundos={'num':[0,0,8]}
#dupRanges={'medium':[15,25]}
#boundos={'cat':[10,1,0],'mixed':[10,1,8]}


for key1,dupRange in dupRanges.iteritems():
    for key2,boundAmount in boundos.iteritems():
        for seed in seeds:
            param=Configuration(key1+"_"+key2+"_seed_%d" % seed)
            param.read("parameter_configurations/"+key1+"_"+key2+"_seed_%d" % seed)
  
            
            supplyAmount=param.supplyAmount
            taskAmount=param.taskAmount
            cateAmount=param.cateAmount
            demandAmount=param.demandAmount
            baseAmount=param.baseAmount
            bigM=100000
            JCTypes={"1" : JCType(0.0,0.3),"2" : JCType(0.0,0.15),"3" : JCType(0.9,0.0)}
            type1amount=param.type1amount
            type2amount=param.type2amount
            type3amount=param.type3amount
            duplicateRange=param.duplicateRange
            catDivAmount=param.catDivAmount
            catValAmount=param.catValAmount
            numAmount=param.numAmount
            random.seed(param.seed)
            directory="lpfiles/"
            
            """              
            supplyAmount=4
            taskAmount=40
            cateAmount=7
            demandAmount=supplyAmount
            baseAmount=4
            bigM=100000
            JCTypes={"1" : JCType(0.0,0.1),"2" : JCType(0.0,0.05),"3" : JCType(0.9,0.0)}
            type1amount=40
            type2amount=6
            type3amount=6
            duplicateRange=[20,30]
            catDivAmount=0
            catValAmount=0
            numAmount=22
            """
            
                    
            
            
            
            
            
            #_____________
            #Data Generation
            #_____________
            
            
            attributes={}
            supplyIds=[]
            demandIds=[]
            taskIds=[]
            baseIds=[]
            categoricIds=[]
            for i in range(supplyAmount):
                supplyIds.append(i)
                attributes[i]=Attribute('supply',valRange=[0,90],fs=[-1000,1000],intensity=0,fp=[1.0])
            
            for i in range(supplyIds[-1]+1,supplyIds[-1]+demandAmount+1):
                demandIds.append(i)
                attributes[i]=Attribute('demand',valRange=[0,20],fs=[-1000,1000])
            
            for i in range(demandIds[-1]+1,demandIds[-1]+taskAmount+1):
                taskIds.append(i)
                attributes[i]=Attribute('task',valRange=[0,20],fs=[-1000 ,1,4,1000],intensity=i < taskAmount/2,fp=[1.0,0.9,0.7])
            
            k=0
            for i in range(taskIds[-1]+1,taskIds[-1]+cateAmount+1):
                categoricIds.append(i)
                if k==0:
                    valAmount=random.randint(8,12)
                    fm=1.0
                if k==1:
                    if key1 != 'small':
                        if key1 == 'large':
                            valAmount=taskAmount
                            fm=0.0
                        else:
                            valAmount=12
                            fm=0.0
                    else:
                        valAmount=8
                        fm=0.0
                if k>1:
                    valAmount=2
                    fm=0.1
                values={}
                for j in range(valAmount):
                    values[j] =  j
                attributes[i]=Attribute('categoric',values=values,fm=fm)
                k+=1
            
            
               
            for i in range(categoricIds[-1]+1,categoricIds[-1]+baseAmount+1):
                baseIds.append(i)
                attributes[i]=Attribute('base',valRange=[0,20],fs=[-1000,1000]) 
            
            
            jcs={}
            j=0
            while (j<type1amount):
                values={}
                valset=0
                for i,attr in attributes.iteritems():
                    if attr.type == 'task':
                        if random.uniform(0,1)<JCTypes["1"].taskprob:
                            values[i] = random.randint(attr.range[0]+5,attr.range[1]-8)
                            valset=1
                        else:
                            values[i]=0.0
                    if attr.type == 'supply':
                        if random.uniform(0,1)<JCTypes["1"].supplyprob:
                            values[i] = random.randint(attr.range[0]+30,attr.range[1])
                            valset=1
                        else:
                            values[i]=0.0
                    if attr.type == 'demand':
                        val1=random.randint(0,6)
                        values[i] = [val1,val1+2]
                    if attr.type == 'base':
                        if i == baseIds[0]:
                            #values[i] = 1
                            values[i] = random.randint(attr.range[0]+10,attr.range[1])
                        else:
                            values[i] = random.randint(attr.range[0]+10,attr.range[1])
                    if attr.type == 'categoric':
                        values[i] = attr.values[random.randint(0,len(attr.values)-1)]
                        
                if (valset == 1):
                    jcs[j] = JC(attributes,values)
                    j+=1
            
            j=type1amount
            while (j<type2amount+type1amount):
                values={}
                valset=0
                for i,attr in attributes.iteritems():
                    if attr.type == 'task' and random.uniform(0,1)<JCTypes["2"].taskprob:
                        values[i] = random.randint(attr.range[0]+5,attr.range[1]-8)
                        valset=1
                    else:
                        values[i]=0.0
                    if attr.type == 'supply'  and random.uniform(0,1)<JCTypes["2"].supplyprob:
                        values[i] = random.randint(attr.range[0]+10,attr.range[1])
                        valset=1
                    else:
                        values[i]=0.0
                    if attr.type == 'demand':
                        val1=random.randint(0,4)
                        values[i] = [val1,random.randint(val1,val1+2)]
                    if attr.type == 'base':
                        if i == baseIds[0]:
                            values[i] = random.randint(1,2)
                        else:
                            values[i] = random.randint(attr.range[0]+10,attr.range[1])
                        
                    if attr.type == 'categoric':
                        values[i] = attr.values[random.randint(0,len(attr.values)-1)]
                        
                if  (valset == 1):
                    jcs[j] = JC(attributes,values)
                    j+=1
            j=type2amount+type1amount
            while (j<type3amount+type2amount+type1amount):
                values={}
                valset=0
                for i,attr in attributes.iteritems():
                    if attr.type == 'task' and random.uniform(0,1)<JCTypes["3"].taskprob:
                        values[i] = random.randint(attr.range[0]+5,attr.range[1])
                        valset=1
                    else:
                        values[i]=0.0
                    if attr.type == 'supply'  and random.uniform(0,1)<JCTypes["3"].supplyprob:
                        values[i] = random.randint(attr.range[0]+10,attr.range[1])
                        valset=1
                    else:
                        values[i]=0.0
                    if attr.type == 'demand':
                        val1=random.randint(0,1)
                        values[i] = [val1,random.randint(val1,val1+1)]
                    if attr.type == 'base':
                        if i == baseIds[0]:
                            values[i] = random.randint(1,2)
                        else:
                            values[i] = random.randint(attr.range[0]+10,attr.range[1])
                    if attr.type == 'categoric':
                        values[i] = attr.values[random.randint(0,len(attr.values)-1)]
                        
                if (valset == 1):
                    jcs[j] = JC(attributes,values)
                    j+=1
            if key1 == 'small':
                mutprob=0.35
            else:
                mutprob=0.35
            
            for jc in jcs.copy():
                newVals=jcs[jc].values.copy()
                for i in range(random.randint(duplicateRange[0],duplicateRange[1])):
                    #newAttrs=jcs[jc].attributes.copy()
                    if random.uniform(0,1) < mutprob:
                        aId=random.randint(0,len(taskIds)-1)
                        while jcs[jc].values[taskIds[aId]] < 0.1 and aId>-(len(taskIds)-1):
                            aId=aId-1
                        if jcs[jc].values[taskIds[aId]] > 0.1:
                            newVals[taskIds[aId]]+=random.randint(-2,2)
                    if random.uniform(0,1) < mutprob:
                        aId=categoricIds[random.randint(0,len(categoricIds)-1)]
                        newVals[aId]=random.randint(0,len(attributes[aId].values)-1)
                    jcs[len(jcs)]=JC([],newVals.copy())
            
            
            catDivBounds={}
            catValBounds={}
            numBounds={}
            
            for i in xrange(catDivAmount):
                attributeId=categoricIds[random.randint(0,len(categoricIds)-1)]
                catDivBounds[i]=CatDivBound(attributes[attributeId],attributeId,random.randint(1,len(attributes[attributeId].values)-1),'L')
            
            
            for i in xrange(catValAmount):
                #attributeId=categoricIds[random.randint(0,len(categoricIds)-1)]
                
                boundType='G'
                if random.randint(0,10)<5:
                    attributeId=categoricIds[1]
                valueId=random.randint(0,len(attributes[attributeId].values)-1)
                if key1 == 'small':
                    boundV=random.randint(30,35)
                else:
                    if key1 == 'medium':
                        boundV=random.randint(40,45)
                    else:
                        boundV=random.randint(90,95)
                catValBounds[i]=CatValBound(attributes[attributeId],attributeId,boundV,boundType,valueId)
            
            numericIds=taskIds+supplyIds+baseIds
            taskPool=[]
            for i in taskIds:
                taskPool.append(i)
            
            if numAmount>len(taskIds):
                numAmount=len(taskIds)
            for i in xrange(numAmount):
                attributeId=taskPool.pop(random.randint(0,len(taskPool)-1))
                if random.randint(0,10)<11:
                    boundType='G'
                else:
                    boundType='L'
                numBounds[i]=NumBound(attributes[attributeId],attributeId,random.randint(3000,3600),boundType)
            
            
            
            model=cplex.Cplex()
            for i,attr in attributes.iteritems():
                if attr.type == 'task':
                    model.variables.add(names=["t#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                    model.variables.add(names=["p#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                if attr.type == 'supply':
                    model.variables.add(names=["t#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                    model.variables.add(names=["p#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                #if attr.type == 'categoric':
                #    model.variables.add(names=["a#%d" % i],lb=[0],ub=[10000],types=['C'])
                if attr.type == 'demand':
                    model.variables.add(names=["n#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                if attr.type == 'base':
                    if i == baseIds[0]:
                        obj=1.0
                    else:
                        obj=0.0
                    model.variables.add(names=["s#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                                               
            for jc in jcs:
                model.variables.add(names=["x#%d" % jc],lb=[0],ub=[1],types=['B'])
                for i,attr in attributes.iteritems():
                    if attr.type == 'task' or attr.type == 'supply' :
                        model.variables.add(names=["c#%d_%d" % (jc,i)],lb=[0],ub=[1],types=['B'])
            
            
            for i,attr in attributes.iteritems():
                if attr.type == 'categoric':
                    for j in attr.values:
                        model.variables.add(names=["e#%d_%d" % (i,j)],lb=[0],ub=[1],types=['B'])
                        model.variables.add(names=["a#%d_%d" % (i,j)],lb=[0],ub=[10000],types=['I'])
                        for t,attr2 in attributes.iteritems():
                            if attr2.type == 'task' or attr2.type == 'supply':
                                model.variables.add(names=["g#%d_%d_%d" % (t,i,j)],lb=[0],ub=[1],types=['B'])
                                                           
            for i,attr in attributes.iteritems():
                if attr.type == 'task' or attr.type == 'supply' :
                    for j,bound in enumerate(attr.frictionSteps):
                        if j < len(attr.frictionSteps)-1:
                            model.variables.add(names=["f#%d_%d" % (i,j)],lb=[0],ub=[1],types=['B'])
            
            
            name2idx = { n : j for j, n in enumerate(model.variables.get_names()) }
            totalMultipliers=0
            for i,a in attributes.iteritems():
                if a.type == 'categoric':
                    totalMultipliers+=a.frictionMultiplier
            
            for jc in jcs:
                thevars=[name2idx["x#%d" % jc]]+[name2idx["c#%d_%d" % (jc,t)] for t,attr in attributes.iteritems() if attr.type == 'task' or attr.type == 'supply']
                thecoefs = [-1.0]+[1.0]*(len(thevars)-1)
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                
            for k,attr in attributes.iteritems():
                if attr.type == 'categoric':
                    for v in attr.values: 
                        for jc in jcs:
                            if jcs[jc].values[k] == v:
                                thevars=[name2idx["x#%d" % jc]]+[name2idx["e#%d_%d" % (k,v)]]
                                thecoefs = [1,-1]
                                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                                for t,attr2 in attributes.iteritems():
                                    if attr2.type == 'task' or attr2.type == 'supply':
                                        thevars=[name2idx["c#%d_%d" % (jc,t)]]+[name2idx["g#%d_%d_%d" % (t,k,v)]]
                                        thecoefs = [1,-1]
                                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                        thevars=[name2idx["x#%d" % jc] for jc in jcs if jcs[jc].values[k] == v]+[name2idx["e#%d_%d" % (k,v)]]
                        thecoefs = [1 for jc in jcs if jcs[jc].values[k] == v]+[-1]
                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [0.0])
                        thevars=[name2idx["x#%d" % jc] for jc in jcs if jcs[jc].values[k] == v]+[name2idx["a#%d_%d" % (k,v)]]
                        thecoefs = [1 for jc in jcs if jcs[jc].values[k] == v]+[-1]
                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                        for t,attr2 in attributes.iteritems():
                            if attr2.type == 'task' or attr2.type == 'supply':
                                thevars=[name2idx["c#%d_%d" % (jc,t)] for jc in jcs if jcs[jc].values[k] == v ]+[name2idx["g#%d_%d_%d" % (t,k,v)]]
                                thecoefs = [1.0 for jc in jcs if jcs[jc].values[k] == v ]+[-1]
                                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [0.0])
                if attr.type == 'base':
                    thevars = [name2idx["x#%d" % jc]  for jc in jcs]+[name2idx["s#%d" % k]]
                    thecoefs = [jcs[jc].values[k] for jc in jcs]+[-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                if attr.type == 'demand':
                    thevars= [name2idx["c#%d_%d" % (jc,t)] for jc in jcs for t,attr2 in attributes.iteritems() if attr2.type == 'task'] + [name2idx["n#%d" % k]]
                    thecoefs = [jcs[jc].values[k][0]*(int(not attr2.intensity))+jcs[jc].values[k][1]*(int(attr2.intensity))
                                for jc in jcs for t,attr2 in attributes.iteritems() if attr2.type == 'task'] + [-1.0]
                    
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                    thevars= [name2idx["n#%d" % k],name2idx["t#%d" % (k-demandAmount)]]
                    thecoefs = [1.0,-1.0] 
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                if attr.type == 'task' or attr.type == 'supply':
                    thevars= [name2idx["g#%d_%d_%d" % (k,k2,v)] for k2,attr2 in attributes.iteritems() if attr2.type == 'categoric' for v in attr2.values] + [name2idx["p#%d" % k]]
                    thecoefs = [attr2.frictionMultiplier for k2,attr2 in attributes.iteritems() if attr2.type == 'categoric' for v in attr2.values] + [-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [totalMultipliers])
                    """
                    #testing constraints:
                    thevars = [name2idx["c#%d_%d" % (jc,k)]  for jc in jcs]+[name2idx["t#%d" % k]]
                    thecoefs = [jcs[jc].values[k] for jc in jcs]+[-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                    """
                    for j,b in enumerate(attr.frictionSteps):
                        if j < len(attr.frictionSteps)-1:
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["p#%d" % k]]
                            thecoefs = [bigM, -1.0]
                            rhs= bigM-b
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["p#%d" % k]]
                            thecoefs = [-bigM, -1.0]
                            rhs= -bigM-attr.frictionSteps[j+1]
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["t#%d" % k]]+[name2idx["c#%d_%d" % (jc,k)] for jc in jcs]
                            thecoefs = [bigM, -1.0]+[jcs[jc].values[k]*attr.frictionPerc[j] for jc in jcs]
                            rhs=bigM
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["t#%d" % k]]+[name2idx["c#%d_%d" % (jc,k)] for jc in jcs]
                            thecoefs = [-bigM, -1.0]+[jcs[jc].values[k]*attr.frictionPerc[j] for jc in jcs]
                            rhs=-bigM
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [rhs])
                    
                    thevars = [name2idx["f#%d_%d" % (k,j)] for j,b in enumerate(attr.frictionSteps) if j < len(attr.frictionSteps)-1]
                    thecoefs = [1.0]*len(thevars)
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [1.0]) 
            
            for i,cond in catValBounds.iteritems():
                model.variables.add(names=["cvb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(["a#%d_%d" % (cond.attributeId,cond.valueId),"cvb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
            
            
                                                                    
            for i,cond in catDivBounds.iteritems():
                model.variables.add(names=["cdb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(["e#%d_%d" % (cond.attributeId,valueId) for valueId in attributes[cond.attributeId].values]+["cdb#%d" % i],
                                                                           [1.0 for valueId in attributes[cond.attributeId].values]+[-1.0*(cond.type == 'L')+1.0*(cond.type == 'G')])], senses = [cond.type], rhs = [cond.bound])                      
            
            
            for i,cond in numBounds.iteritems():
                model.variables.add(names=["nb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                if cond.attribute.type == 'task':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["t#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'supply':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["t#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'base':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["s#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'demand':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["n#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["n#%d" % cond.attributeId],[1.0])], senses = [cond.type], rhs = [cond.bound])
            
            model.write(directory+param.name+"_friction_DA_I.lp")
            
            
            model=cplex.Cplex()
            for i,attr in attributes.iteritems():
                if attr.type == 'task':
                    model.variables.add(names=["t#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                    model.variables.add(names=["p#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                if attr.type == 'supply':
                    model.variables.add(names=["t#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                    model.variables.add(names=["p#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                #if attr.type == 'categoric':
                #    model.variables.add(names=["a#%d" % i],lb=[0],ub=[10000],types=['C'])
                if attr.type == 'demand':
                    model.variables.add(names=["n#%d" % i],lb=[-10000],ub=[10000],types=['C'])
                if attr.type == 'base':
                    if i == baseIds[0]:
                        obj=1.0
                    else:
                        obj=0.0
                    model.variables.add(names=["s#%d" % i],lb=[-10000],ub=[10000],types=['C'],obj=[0.0])
                                               
            for jc in jcs:
                model.variables.add(names=["x#%d" % jc],lb=[0],ub=[1],types=['B'])
                for i,attr in attributes.iteritems():
                    if attr.type == 'task' or attr.type == 'supply' :
                        model.variables.add(names=["c#%d_%d" % (jc,i)],lb=[0],ub=[1],types=['B'])
            
            
            for i,attr in attributes.iteritems():
                if attr.type == 'categoric':
                    for j in attr.values:
                        model.variables.add(names=["e#%d_%d" % (i,j)],lb=[0],ub=[1],types=['B'])
                        model.variables.add(names=["a#%d_%d" % (i,j)],lb=[0],ub=[10000],types=['I'])
                        for t,attr2 in attributes.iteritems():
                            if attr2.type == 'task' or attr2.type == 'supply':
                                model.variables.add(names=["g#%d_%d_%d" % (t,i,j)],lb=[0],ub=[1],types=['B'])
                                                           
            for i,attr in attributes.iteritems():
                if attr.type == 'task' or attr.type == 'supply' :
                    for j,bound in enumerate(attr.frictionSteps):
                        if j < len(attr.frictionSteps)-1:
                            model.variables.add(names=["f#%d_%d" % (i,j)],lb=[0],ub=[1],types=['B'])
            
            
            name2idx = { n : j for j, n in enumerate(model.variables.get_names()) }
            totalMultipliers=0
            for i,a in attributes.iteritems():
                if a.type == 'categoric':
                    totalMultipliers+=a.frictionMultiplier
            
            for jc in jcs:
                thevars=[name2idx["x#%d" % jc]]+[name2idx["c#%d_%d" % (jc,t)] for t,attr in attributes.iteritems() if attr.type == 'task' or attr.type == 'supply']
                thecoefs = [-1.0]+[1.0]*(len(thevars)-1)
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                
            for k,attr in attributes.iteritems():
                if attr.type == 'categoric':
                    for v in attr.values: 
                        for jc in jcs:
                            if jcs[jc].values[k] == v:
                                thevars=[name2idx["x#%d" % jc]]+[name2idx["e#%d_%d" % (k,v)]]
                                thecoefs = [1,-1]
                                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                                for t,attr2 in attributes.iteritems():
                                    if attr2.type == 'task' or attr2.type == 'supply':
                                        thevars=[name2idx["c#%d_%d" % (jc,t)]]+[name2idx["g#%d_%d_%d" % (t,k,v)]]
                                        thecoefs = [1,-1]
                                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                        thevars=[name2idx["x#%d" % jc] for jc in jcs if jcs[jc].values[k] == v]+[name2idx["e#%d_%d" % (k,v)]]
                        thecoefs = [1 for jc in jcs if jcs[jc].values[k] == v]+[-1]
                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [0.0])
                        thevars=[name2idx["x#%d" % jc] for jc in jcs if jcs[jc].values[k] == v]+[name2idx["a#%d_%d" % (k,v)]]
                        thecoefs = [1 for jc in jcs if jcs[jc].values[k] == v]+[-1]
                        model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                        for t,attr2 in attributes.iteritems():
                            if attr2.type == 'task' or attr2.type == 'supply':
                                thevars=[name2idx["c#%d_%d" % (jc,t)] for jc in jcs if jcs[jc].values[k] == v ]+[name2idx["g#%d_%d_%d" % (t,k,v)]]
                                thecoefs = [1.0 for jc in jcs if jcs[jc].values[k] == v ]+[-1]
                                model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [0.0])
                if attr.type == 'base':
                    thevars = [name2idx["x#%d" % jc]  for jc in jcs]+[name2idx["s#%d" % k]]
                    thecoefs = [jcs[jc].values[k] for jc in jcs]+[-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                if attr.type == 'demand':
                    thevars= [name2idx["c#%d_%d" % (jc,t)] for jc in jcs for t,attr2 in attributes.iteritems() if attr2.type == 'task'] + [name2idx["n#%d" % k]]
                    thecoefs = [jcs[jc].values[k][0]*(int(not attr2.intensity))+jcs[jc].values[k][1]*(int(attr2.intensity))
                                for jc in jcs for t,attr2 in attributes.iteritems() if attr2.type == 'task'] + [-1.0]
                    
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                    thevars= [name2idx["n#%d" % k],name2idx["t#%d" % (k-demandAmount)]]
                    thecoefs = [1.0,-1.0] 
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [0.0])
                if attr.type == 'task' or attr.type == 'supply':
                    thevars= [name2idx["g#%d_%d_%d" % (k,k2,v)] for k2,attr2 in attributes.iteritems() if attr2.type == 'categoric' for v in attr2.values] + [name2idx["p#%d" % k]]
                    thecoefs = [attr2.frictionMultiplier for k2,attr2 in attributes.iteritems() if attr2.type == 'categoric' for v in attr2.values] + [-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [totalMultipliers])
                    """
                    #testing constraints:
                    thevars = [name2idx["c#%d_%d" % (jc,k)]  for jc in jcs]+[name2idx["t#%d" % k]]
                    thecoefs = [jcs[jc].values[k] for jc in jcs]+[-1.0]
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [0.0])
                    """
                    for j,b in enumerate(attr.frictionSteps):
                        if j < len(attr.frictionSteps)-1:
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["p#%d" % k]]
                            thecoefs = [bigM, -1.0]
                            rhs= bigM-b
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["p#%d" % k]]
                            thecoefs = [-bigM, -1.0]
                            rhs= -bigM-attr.frictionSteps[j+1]
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["t#%d" % k]]+[name2idx["c#%d_%d" % (jc,k)] for jc in jcs]
                            thecoefs = [bigM, -1.0]+[jcs[jc].values[k]*attr.frictionPerc[j] for jc in jcs]
                            rhs=bigM
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["L"], rhs = [rhs]) 
                            thevars = [name2idx["f#%d_%d" % (k,j)],name2idx["t#%d" % k]]+[name2idx["c#%d_%d" % (jc,k)] for jc in jcs]
                            thecoefs = [-bigM, -1.0]+[jcs[jc].values[k]*attr.frictionPerc[j] for jc in jcs]
                            rhs=-bigM
                            model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["G"], rhs = [rhs])
                    
                    thevars = [name2idx["f#%d_%d" % (k,j)] for j,b in enumerate(attr.frictionSteps) if j < len(attr.frictionSteps)-1]
                    thecoefs = [1.0]*len(thevars)
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(thevars,thecoefs)], senses = ["E"], rhs = [1.0]) 
            
            for i,cond in catValBounds.iteritems():
                model.variables.add(names=["cvb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(["a#%d_%d" % (cond.attributeId,cond.valueId),"cvb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
            
            
                                                                    
            for i,cond in catDivBounds.iteritems():
                model.variables.add(names=["cdb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                model.linear_constraints.add(lin_expr = [cplex.SparsePair(["e#%d_%d" % (cond.attributeId,valueId) for valueId in attributes[cond.attributeId].values]+["cdb#%d" % i],
                                                                           [1.0 for valueId in attributes[cond.attributeId].values]+[-1.0*(cond.type == 'L')+1.0*(cond.type == 'G')])], senses = [cond.type], rhs = [cond.bound])                      
            
            
            for i,cond in numBounds.iteritems():
                model.variables.add(names=["nb#%d" % i],lb=[0],ub=[10000],types=['C'],obj=[1.0])
                if cond.attribute.type == 'task':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["t#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'supply':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["t#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'base':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["s#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                if cond.attribute.type == 'demand':
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["n#%d" % cond.attributeId,"nb#%d" % i],[1.0]+[-1.0*(cond.type == 'L')+1.0*(cond.type== 'G')])], senses = [cond.type], rhs = [cond.bound])
                    model.linear_constraints.add(lin_expr = [cplex.SparsePair(["n#%d" % cond.attributeId],[1.0])], senses = [cond.type], rhs = [cond.bound])
            
            model.write(directory+param.name+"_no_friction_DA_I.lp")