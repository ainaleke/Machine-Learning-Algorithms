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
meandiastolicBloodPress=collections.Counter()
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

#####probability/outcome of each feature with a tested_positive and tested_negative label
prob_numOfPreg=collections.Counter()
prob_bodyMassIndex=collections.Counter()
prob_diabetesPdgreeFxn=collections.Counter()
prob_diastolicBloodPress=collections.Counter()
prob_plasmaGlucoseConc=collections.Counter()
prob_age=collections.Counter()
prob_twoHourSerum=collections.Counter()
prob_tricepSkinFold=collections.Counter()

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

            meandiastolicBloodPress[a[8]]+=float(a[2])
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
    calc_mean_of_features(meandiastolicBloodPress, sum_by_class_of_diastolic)
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
            std_dev_diastolicBloodPress[a[8]]+= ((float(a[2]) - meandiastolicBloodPress[a[8]]) ** 2) / (sum_by_class_of_diastolic[a[8]] - 1)
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

def calc_prob_values(test_value, mean_of_feature, std_dev_of_feature, tested_label):
    first_part=1/(math.sqrt((2*math.pi))* float(std_dev_of_feature[tested_label]))
    second_part=0.5 *((float(test_value)-mean_of_feature[tested_label])/std_dev_of_feature[tested_label])**2
    result=first_part * math.exp(-1 * second_part)
    return result

def get_likelihood(eachline, tested_label):
    result=0
    ###tested_label is either tested_positive or tested_negative
    prob_numOfPreg=calc_prob_values(eachline[0], meanNumOfPreg, std_dev_numOfPreg, tested_label)
    prob_plasmaGlucoseConc=calc_prob_values(eachline[1], meanplasmaGlucoseConc, std_dev_plasmaGlucoseConc, tested_label)
    prob_diastolicBloodPress=calc_prob_values(eachline[2], meandiastolicBloodPress, std_dev_diastolicBloodPress, tested_label)
    prob_tricepSkinFold=calc_prob_values(eachline[3], meantricepSkinFold, std_dev_tricepSkinFold,tested_label)
    prob_twoHourSerum=calc_prob_values(eachline[4], meantwoHourSerum, std_dev_twoHourSerum, tested_label)
    prob_bodyMassIndex=calc_prob_values(eachline[5], meanbodyMassIndex, std_dev_bodyMassIndex, tested_label)
    prob_diabetesPdgreeFxn=calc_prob_values(eachline[6], meandiabetesPdgreeFxn, std_dev_diabetesPdgreeFxn, tested_label)
    prob_age=calc_prob_values(eachline[7], meanage, std_dev_age, tested_label)
    result= prob_numOfPreg * prob_plasmaGlucoseConc * prob_diastolicBloodPress * prob_tricepSkinFold * prob_twoHourSerum \
           * prob_bodyMassIndex * prob_diabetesPdgreeFxn * prob_age * class_probability[tested_label]
    return result

test_datafile='diabetes_testdata.data'
def predict_result(test_datafile):
    with open(test_datafile) as f:
        for line in f:
            a=line.rstrip('\n').split(',')
            likelihood_its_positive=get_likelihood(a, 'tested_positive')
            likelihood_its_negative=get_likelihood(a, 'tested_negative')
            if(likelihood_its_negative > likelihood_its_positive):
                print 'Result: Tested Negative => ',a
            else:
                print 'Result: Tested Positive => ',a

read_training_data(datafile)
calculateMeanFeatures(datafile)
predict_result(test_datafile)
#print num_of_entries

#print 'Class', class_probability

print math.exp(-1)




