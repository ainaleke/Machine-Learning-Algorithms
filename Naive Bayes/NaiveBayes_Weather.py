import sys
import collections
import re
from collections import defaultdict,Counter

#filename outlook temp humidity windy
"""
filename=sys.argv[0]
outlook=sys.argv[1]
temp=sys.argv[2]
humidity=sys.argv[3]
windy=sys.argv[4]
"""
labels=Counter()
likelihoodOutlook=collections.defaultdict(Counter)
likelihoodTemp=collections.defaultdict(Counter)
likelihoodHumid=collections.defaultdict(Counter)
likelihoodWindy=collections.defaultdict(Counter)
datafile='weather_expansive.data'
def read_training_data(datafile):
    with open(datafile) as f:
        for line in f:
            #print(line)
            a=line.split()
            #print a[0]
            labels[a[4]]+=1
            #print(a[0],a[4])
            likelihoodOutlook[a[0]][a[4]]+=1
            likelihoodTemp[a[1]][a[4]]+=1
            likelihoodHumid[a[2]][a[4]]+=1
            likelihoodWindy[a[3]][a[4]]+=1


read_training_data(datafile)
print(likelihoodOutlook)
print(likelihoodTemp)
print(likelihoodHumid)
print(likelihoodWindy)
#print test

