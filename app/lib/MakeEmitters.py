#Adapted 8/11/16

#Imports
    
from EPANETFunctions9 import * #get all functions from EPANETFunctions file (technically classes are already imported via functions file... oh well!
import epamodule as em
reload(em)        
import scipy.integrate as igt
import numpy as np
from matplotlib.dates import DateFormatter, datetime


#READ

#filename="BAK_CV.inp" #ACBulk has unscaled demand at all nodes including ACBulk Node
filename="GOY_CV_Pump.inp"
filename="N2_CV.inp"  
filename="MOD_CV.inp"  
filename="PES_CV.inp"  
filename="BAK_CV.inp"
filename="FOS_CV.inp"
filename="EXN_CV.inp"
filename="BIN.inp"
#filename="Richmond_standard.inp"
#filename="N4_CV.inp"
#filename="SingleNodeTest.inp"


targNRW=0.15



#"""
inpName=filename[:-4]
em.ENopen(inpName+'.inp',inpName+'.rpt')
#print(inpName)
demMult=em.ENgetoption(em.EN_DEMANDMULT)

### get avg pressure
nnodes=em.ENgetcount(em.EN_NODECOUNT)
junInds=[]
for index in range(1,nnodes+1):
    if em.ENgetnodetype(index)==em.EN_JUNCTION:
        junInds.append(index)
    
junPres=[[] for q in range(len(junInds))]

time=[]
## RUN SIM
em.ENopenH()
em.ENinitH(0)
while True :
    em.ENrunH()

    t=em.ENsimtime()
    time.append(datetime.timedelta.total_seconds(t)) #convert time delta to seconds
     
    # Retrieve hydraulic results for time t

#    #Tank heights
#    for  i in range(0,len(tankInds)):
#        p=em.ENgetnodevalue(tankInds[i], em.EN_PRESSURE )
#        tankLvls[i].append(p)
#        
    #Junction Pressure
    for  i in range(0,len(junInds)):
        p=em.ENgetnodevalue(junInds[i], em.EN_PRESSURE )
        junPres[i].append(p)
    
    #End if... 
    tstep=em.ENnextH()            
    if (tstep<=0): #end condition. 
        break
   
    #if (t>6000):#debugging
    #    print("early end for debugging")
    #    break 
    
em.ENcloseH()

#convert arrays to numpy
#tankLvlsM=np.transpose(np.array(tankLvls))
junPresM=np.transpose(np.array(junPres))
timeM=np.transpose(np.array(time))

#Calc inst pressure
instP=np.mean(junPresM,axis=1)

#Calc time-space average pressure
#intP=igt.cumtrapz(instP,timeM,initial=0.0) #time intergral of pressure
#cumT=np.copy(timeM) #Time is cumulative already!
#cumT[0]=1 # to avoid divide by 0; intP[0]=0, so no effect. 
#avgP=np.divide(intP,cumT) #time and space averaged pressure

intP=igt.trapz(instP,timeM)
avgP=np.divide(intP,timeM[-1])

if em.EN_LPS!=em.ENgetflowunits():
    print('STOP. Input file not in LPS')
#print(demMult)
    
## RUN SIM, get average pressure, the modify the network. ##
em.ENclose()
#"""



#ACTank has unscaled demand. e.g. J94 has 0.02 demand

data=ReadEPANET(filename)

#divide up data (of type dictionary) into its components
fullcontentList=data['FullContent']
junctions=data['Junctions']
tanks=data['Tanks']
pipes=data['Pipes']
coordinates=data['Coordinates']
demands=data['Demands']  
emitters=data['Emitters']
tags=data['Tags']
patterns=data['Patterns'] #NB Patterns are read only!!!
#print('Arrived')


#adjFrac = 1.0#0.4625 # from pattern average in EPANET b/c Suez reports peak demand as nodal demand


#print('last junction',junctions[-1])

#WRITE Parsed Original (for debugging)
#WriteEPANET(filename[:-4]+"_parsed.inp", junctions, tanks, pipes, coordinates, demands,emitters, fullcontentList)

## First scale all junction base demand by its pattern
## Then account for junctions with multiple demands
## Finally scale all demand by the demand multiplier

#COMBINE Demands into Junctions
#
jIndex=[]
for j in junctions:
    jIndex.append(j.ID)
pIndex=[]
for p in patterns:
    pIndex.append(p.ID)
#for every entry in the demands list, pop it, and =+ the demand of that junction

## Scale junction demand
#print(sum([j.Demand for j in junctions]))

for i, j in enumerate(junctions):
    #print('here')
    if len(j.Pattern)>0:
        pi=pIndex.index(j.Pattern)
        patAVG=patterns[pi].Avg
        #print(j.ID)
        #print(pi)
        #print(patAVG)
        junctions[i].Demand=j.Demand*patAVG
        junctions[i].Pattern='' #overwrite previous pattern 
    

#print(sum([j.Demand for j in junctions])) 


## FIX THIS! 
#account for patterns... 
#first demand entry repeats "base demand" in junction summary. 
#first make a list of all junctions with demands
demList=[d.ID for d in demands]
demList=list(set(demList)) #unique list

for dL in demList:
    thisDem=0
    for d in demands:
        if d.ID==dL:
            pi=pIndex.index(d.Pattern)
            patAVG=patterns[pi].Avg
            #print(patAVG)
            thisDem+=d.Demand*patAVG
    ji=jIndex.index(dL)
    junctions[ji].Demand=thisDem
#print(sum([j.Demand for j in junctions])) 
demands=[] #overwrite demand list!

#print('dem mult doesnt work in epamodule')
#demMult=1.0
for j in junctions:
    j.Demand=j.Demand*demMult
#print(sum([j.Demand for j in junctions])) 

#WriteEPANET(filename[:-4]+"_parsed.inp", junctions, tanks, pipes, coordinates, demands,emitters, tags, fullcontentList)


##First scale for NRW accounting for wierd peak demand reporting convention

#Make leak coefficients Q=C pressure^exponent
pressure=avgP
power=1.0
NRW=0.15
if targNRW==0.15:
    NRW_Multiplier=1.0#5.6666#1.0 # #5.6666 is 50% (NOT 50% of current!) and 32.111 is 85% 
else:
    if targNRW==0.5:
        NRW_Multiplier=5.6666
    else:
        NRW_Multiplier=1.0
        print('ERROR: wrong target NRW specified')

## Planned NRW is 15% therefore planned customer demand is 85% of nodal demand
# However to model higher leakage rates, keep ccustomer demand at 85%, but increase emitter coefficient... 
#NRW_Multiplier is responsible for this addiitonal scaling

colonYN=0
for j in junctions:
    if j.Demand>0:
        emitters.append(Emitter(j.ID,j.Demand*NRW*NRW_Multiplier/pressure**power,colonYN)) #NRW COMPENSATING FOR multiplier
    j.Demand=j.Demand*(1-NRW)

    

    
#now scale demands to expected total demand under 24/7
totDem=0
for j in junctions:
    totDem+= j.Demand
    
totDem = totDem*3600.0*24.0/10.0**6.0
print('Unadjusdted Demand with emitters (sent to CWS inp file) = ')
print(totDem)

#ilenameFIX, junctionsFIX, tanksFIX, pipesFIX, coordinatesFIX, demandsFIX,emittersFIX,tagsFIX, fullcontentListFIX
WriteEPANET(filename[:-4]+"_emitters15_15.inp", junctions, tanks, pipes, coordinates, demands,emitters,tags, fullcontentList)

#now scale demands to expected total demand under 24/7

for j in junctions:
    j.Demand=j.Demand

    
#now scale demands to expected total demand under 24/7
totDem=0
for j in junctions:
    totDem+= j.Demand
    
totDem = totDem*3600.0*24.0/10.0**6.0
print('Adjusted Demand eith emitters (Sent to Tank program) = ')
print(totDem)



#WRITE simple demand version
#WriteEPANET(filename[:-4]+"_demand.inp", junctions, tanks, pipes, coordinates, demands, fullcontentList)

#ROUND KEY VALUES
[junctions,tanks,pipes]=RoundKeyValues(junctions,tanks,pipes)

#ID zones to give BPs
KList=[]
LList=[]

for j in junctions:
    if 1: #j.ID[:3]=="JKB":
        KList.append(j.ID) 
    else:
        LList.append(j.ID) #else LList
            
KLheight=0
LLheight=0
HHdailyDemand=1000 #Round number for paper
#873 #mean billing data from Saket Jan/Feb        

#INSERT SUMPS
    #for constants see MakeSumps Function
coordOff=100.0
[junctionsR,tanksR,pipesR,coordinatesR]=MakeSpecifiedSumps(junctions,tanks,pipes,coordinates,coordOff,HHdailyDemand,KLheight,LLheight,KList,LList)

# junctions,tanks,pipes,coordinates, HHDaily, sDepth, bpDepth,sList,bpList):
#[junctionsR2,tanksR2,pipesR2,coordinatesR2]=MakeSpecifiedSumps(800,-4,junctionsR,tanksR,pipesR,coordinatesR,bpList)

#WRITE sumped version demand version
WriteEPANET(filename[:-4]+"_Tanks_CV_15_%.0f_Padj.inp" %(100*targNRW), junctionsR, tanksR, pipesR, coordinatesR, demands, emitters,tags, fullcontentList)
#'%.3f' %twoR2L
#WriteEPANET(filename[:-4]+"_SomeBPs.inp", junctionsR2, tanksR2, pipesR2, coordinatesR2, demands, fullcontentList)
print('DONE EXECUTION')
#"""
