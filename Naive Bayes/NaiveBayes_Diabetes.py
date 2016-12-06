import sys
import collections
import re
import math
from collections import defaultdict,Counter
list=[]
num_of_entries=0
class_probability=collections.Counter()
datafile='training_data.labels'

###Mean entries to be calculated
meanNumOfPreg=collections.Counter()
meanplasmaGlucoseConc=collections.Counter()
meandiastolicBlooddPress=collections.Counter()
meantricepSkinFold=collections.Counter()
meantwoHourSerum=collections.Counter()
meanbodyMassIndex=collections.Counter()
meandiabetesPdgreeFxn=collections.Counter()
meanage=collections.Counter()

###Sum of each label by feature
sum_by_class_of_pregnant=collections.Counter()
sum_by_class_of_plasma_glucose=collections.Counter()
sum_by_class_of_diastolic=collections.Counter()
sum_by_class_of_tricepskinfold=collections.Counter()
sum_by_class_of_twohourserum=collections.Counter()
sum_by_class_of_bodymassindex=collections.Counter()
sum_by_class_of_diabetes_pedigree=collections.Counter()
sum_by_class_of_age=collections.Counter()

####Standard Deviation counters
std_dev_numOfPreg=collections.Counter()
std_dev_bodyMassIndex=collections.Counter()
std_dev_diabetesPdgreeFxn=collections.Counter()
std_dev_diastolicBloodPress=collections.Counter()
std_dev_plasmaGlucoseConc=collections.Counter()
std_dev_age=collections.Counter()
std_dev_twoHourSerum=collections.Counter()
std_dev_tricepSkinFold=collections.Counter()

########Read training data set and get the sum total and the number of occurrences
def read_training_data(datafile):
    with open(datafile) as f:
        num=0
        for line in f:
            num+=1
            a=line.rstrip('\n').split(',')
            ##get the conditional probailities ie. tested_negative and tested_positive
            class_probability[a[8]]+=float(1)
            meanNumOfPreg[a[8]]+=float(a[0])
            sum_by_class_of_pregnant[a[8]]+=1

            meanplasmaGlucoseConc[a[8]]+=float(a[1])
            sum_by_class_of_plasma_glucose[a[8]]+=1

            meandiastolicBlooddPress[a[8]]+=float(a[2])
            sum_by_class_of_diastolic[a[8]]+=1

            meantricepSkinFold[a[8]]+=float(a[3])
            sum_by_class_of_tricepskinfold[a[8]]+=1

            meantwoHourSerum[a[8]]+=float(a[4])
            sum_by_class_of_twohourserum[a[8]]+=1

            meanbodyMassIndex[a[8]]+=float(a[5])
            sum_by_class_of_bodymassindex[a[8]]+=1

            meandiabetesPdgreeFxn[a[8]]+=float(a[6])
            sum_by_class_of_diabetes_pedigree[a[8]]+=1

            meanage[a[8]]+=float(a[7])
            sum_by_class_of_age[a[8]]+=1

    global num_of_entries
    num_of_entries=num

    ##Calculate the conditional Probability for both labels tested_positive and tested_negative
    for x in class_probability:
        class_probability[x] /= num_of_entries


#function to calculate mean for each feature
def calc_mean_of_features(sumTotalCounter,numberOfOccurences):
    for x in sumTotalCounter:
        sumTotalCounter[x] /= numberOfOccurences[x]


###Calculate the mean for each feature
def calculateMeanFeatures(datafile):
    ###Cycle through each feature and compute the mean
    calc_mean_of_features(meanNumOfPreg,sum_by_class_of_pregnant)
    calc_mean_of_features(meanbodyMassIndex,sum_by_class_of_bodymassindex)
    calc_mean_of_features(meandiabetesPdgreeFxn,sum_by_class_of_diabetes_pedigree)
    calc_mean_of_features(meandiastolicBlooddPress,sum_by_class_of_diastolic)
    calc_mean_of_features(meanplasmaGlucoseConc,sum_by_class_of_plasma_glucose)
    calc_mean_of_features(meanage,sum_by_class_of_age)
    calc_mean_of_features(meantwoHourSerum,sum_by_class_of_twohourserum)
    calc_mean_of_features(meantricepSkinFold,sum_by_class_of_tricepskinfold)

    ###Calculate standard deviation for each feature
    calculateStdDeviation(datafile)

def calculateStdDeviation(datafile):
    result=collections.Counter()
    with open(datafile) as f:
        for line in f:
            a=line.rstrip('\n').split(',')
            ##Calculate the variance of each of the Features with respect to tested_positive or tested_negative
            std_dev_numOfPreg[a[8]]+=((float(a[0])-meanNumOfPreg[a[8]])**2)/(sum_by_class_of_pregnant[a[8]]-1)
            std_dev_plasmaGlucoseConc[a[8]]+=((float(a[1])-meanplasmaGlucoseConc[a[8]])**2)/(sum_by_class_of_plasma_glucose[a[8]]-1)
            std_dev_diastolicBloodPress[a[8]]+=((float(a[2])-meandiastolicBlooddPress[a[8]])**2)/(sum_by_class_of_diastolic[a[8]]-1)
            std_dev_tricepSkinFold[a[8]]+=((float(a[3])-meantricepSkinFold[a[8]])**2)/(sum_by_class_of_tricepskinfold[a[8]]-1)
            std_dev_twoHourSerum[a[8]]+=((float(a[4])-meantwoHourSerum[a[8]])**2)/(sum_by_class_of_twohourserum[a[8]]-1)
            std_dev_bodyMassIndex[a[8]]+=((float(a[5])-meanbodyMassIndex[a[8]])**2)/(sum_by_class_of_bodymassindex[a[8]]-1)
            std_dev_diabetesPdgreeFxn[a[8]]+=((float(a[6])-meandiabetesPdgreeFxn[a[8]])**2)/(sum_by_class_of_diabetes_pedigree[a[8]]-1)
            std_dev_age[a[8]]+=((float(a[7])-meanage[a[8]])**2)/(sum_by_class_of_age[a[8]]-1)

    get_sqrt_of_features(std_dev_numOfPreg)
    get_sqrt_of_features(std_dev_plasmaGlucoseConc)
    get_sqrt_of_features(std_dev_diastolicBloodPress)
    get_sqrt_of_features(std_dev_tricepSkinFold)
    get_sqrt_of_features(std_dev_bodyMassIndex)
    get_sqrt_of_features(std_dev_diabetesPdgreeFxn)
    get_sqrt_of_features(std_dev_age)
    get_sqrt_of_features(std_dev_twoHourSerum)
    print 'Std Dev Age',std_dev_age
    print 'Std Dev Num preg',std_dev_numOfPreg

##Calculate the sqrt of features
def get_sqrt_of_features(std_dev_feature):
    for x in std_dev_feature:
        std_dev_feature[x] = math.sqrt(std_dev_feature[x])

read_training_data(datafile)
print meanNumOfPreg
calculateMeanFeatures(datafile)
print num_of_entries

print 'Class', class_probability
#def predictOutcome():
