import glob
import os
from os.path import join, dirname
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


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
        labels.append(1)

file_path = 'enron1/ham'
for filename in glob.glob(join(file_path, '*.txt')):
    with open(filename, 'r') as infile:
        emails.append((infile.read()))
        labels.append(0)

print len(emails)
print len(labels)

# Now we clean all the emails to remove
# Number and punctuation removal
# Human name removal(optional)
# Stop words removal
# Lemmatization

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

if __name__ == "__main__":
    # here we consider the 500 most frequent words and remove or eliminate all stop words like to, is etc.
    cv=CountVectorizer(stop_words="english", max_features=500)
    cleaned_email_list = clean_words(emails)
    print len(cleaned_email_list[0])
    transformed_emails = cv.fit_transform(cleaned_email_list)

    print transformed_emails[0]
