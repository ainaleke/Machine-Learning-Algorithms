from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_20newsgroups
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer

def letters_only(str):
    return str.isalpha()

cv=CountVectorizer(stop_words="english", max_features=500)
groups=fetch_20newsgroups()
cleaned = []
all_names = set(names.words())
lemmatizer = WordNetLemmatizer()

#print(lemmatizer.lemmatize('machines'))
for post in groups.data:
    for word in post.split():
        if letters_only(word):
            cleaned.append(''.join(lemmatizer.lemmatize(word.lower())))
transformed=cv.fit_transform(cleaned)
list_of_names=cv.get_feature_names()


print(list_of_names)
sns.distplot(np.log(transformed.toarray().sum(axis=0)))
plt.title('Distribution Plot of 500 Word counts')
plt.xlabel('Log Count')
plt.ylabel('Frequency')
plt.show()