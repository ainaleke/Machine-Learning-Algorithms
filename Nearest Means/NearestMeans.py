import sys;
import numpy as np;


script, breast_cancer_data,training_labels=sys.argv;
from logging import DEBUG

prompt='>';
#pip install numpy pandas
#python NearestMeans.py   breast_cancer.data   breast_cancer.labels
#breast cancer data set
datafile=sys.argv[1]
data=[]
with open(datafile) as f:
    for line in f:
        #print(line)
        a=line.split()
        l2=[]
        for j in range(0,len(a),1):
            l2.append(float (a[j]))

        data.append(l2)

#print(data)
rows=len(data)
cols=len(data[0])
#end of parsing and converting data into a two dimensional mmatrix/array
if(DEBUG):
    for i in range(0,len(data),1):
        print(data[i])

###READ BREAST_CANCER LABELS
labelfile=sys.argv[2]
training_labels={}
n=[0,0]
#for i in range(0,len(labelfile),1):
with open(labelfile) as f:
    for line in f:
        a=line.split()
        training_labels[int (a[1])]=int (a[0])
        #n=[0 , 1]
        print(int(a[0]))
        n[int (a[0])]+=1

if(DEBUG):
    for i in range(0,len(n),1):
        print(n[i])
    for x in training_labels:
        #for y in training_labels[x]:
            print(training_labels[x])

##Calculate Means for each label indentifier either 0 or 1
mean0=[]
mean1=[]

for i in range(0,cols,1):
    mean0.append(0.0)
    mean1.append(0.0)

for i in range(0,rows,1):
    if(training_labels[i]!=None and training_labels[i]==0):
        for j in range(0,cols,1):
            mean0[j]+=data[i][j]
    elif(training_labels[i]!=None and training_labels[i]==1):
        for k in range(0,cols,1):
            mean1[k]+=data[i][k]

for p in range(0,cols,1):
    mean0[p]/=n[0]
    mean1[p]/n[1]
print("Mean values with 0 as labels")
print(mean0)

print("Mean values with 1 as labels")
print(mean1)

#Calculate the distance of mean to each test point
for i in range(0,rows,1):
    d0=0
    d1=0
    if(training_labels[i]!=None):
        for j in range(0,cols,1):
            #get the distances from the gradient descent
            d0+=(mean0[j]-data[i][j])**2
            d1+=(mean1[j]-data[i][j])**2
            if(d0<d1):
                print("0",i)
            else:
                print("1",j)