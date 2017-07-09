import glob
import os
from os.path import join, dirname
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

def letters_only(astr):
    return astr.isalpha()

emails, labels = [], []
# Then to load the spam email files:
all_names = set(names.words())
lemmatizer = WordNetLemmatizer()


file_path = 'enron1/spam'
for filename in glob.glob(join(file_path, '*.txt')):
    with open(filename, 'r') as infile:
        emails.append(infile.read())
        labels.append(1) #Label 1 represents a spam email

file_path = 'enron1/ham'
for filename in glob.glob(join(file_path, '*.txt')):
    with open(filename, 'r') as infile:
        emails.append((infile.read()))
        labels.append(0) #Label 0 represents a legitimate email


"""
Calculate Prior/ probability of the classes i.e. P(Spam) and P(Not Spam) and place results in
dictionary
"""

def get_class_prob(labels):
    """
    :param labels: grouped sample indicies by class -> 0 or 1

    Get each label which is either 0 or 1 and generate a dictionary with their indices from labels
    :return: label_index = {0:[1500, 1501, 1502, 1503, 1504, 1505...], 1:[1,2,3,4,5,6...]},
    """
    label_index = defaultdict(list)

    for index, label in enumerate(labels):
        label_index[label].append(index)

    prior = {}
    for class_, index in label_index.iteritems():
        print len(index)
        #prior[class_] = len(index)

    #Get total count of all labels in the list
    #total_label_count = sum(label_index.values())

get_class_prob(labels)


"""
 Now we clean all the emails to remove
 Number and punctuation removal
 Human name removal(optional)
 Stop words removal
 Lemmatization

"""
def clean_words(email_list):
    cleaned_emails = []
    temp = []
    for email in email_list:
        str = ""
        for word in email.split():
            if letters_only(word) and word not in all_names:
                str += ' ' + lemmatizer.lemmatize((word.lower()))
        cleaned_emails.append(str)
    return cleaned_emails


'''
def clean_words(email_list):
    cleaned_emails = []
    for email in email_list:
        #cleaned_emails.append(
        str = ' '.join([lemmatizer.lemmatize(word.lower())
        for word in email.split()
        if letters_only(word) and word not in all_names])
        print str
        cleaned_emails.append(str)
    return cleaned_emails
'''



if __name__ == "__main__":
    # here we consider the 500 most frequent words and remove or elimin
    cv=CountVectorizer(stop_words="english", max_features=500)
    cleaned_email_list = clean_words(emails)
    print len(cleaned_email_list[0])
    transformed_emails = cv.fit_transform(cleaned_email_list)

    #print transformed_emails[0]

    feature_names = cv.get_feature_names()
    #print lemmatizer.lemmatize(feature_names[125])
