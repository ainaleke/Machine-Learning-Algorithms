import sys;

script, breast_cancer_data,training_labels=sys.argv;
from logging import DEBUG

prompt='>';
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
train_labels_dict={}
n=[]
for i in range(0,len(labelfile),1):
    with open(labelfile) as f:
        for line in f:
            a=line.split()


