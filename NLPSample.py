import nltk
import matplotlib.pyplot as plt
from nltk.corpus import names
from sklearn.datasets import fetch_20newsgroups
from nltk.stem.porter import PorterStemmer
import numpy as np
import seaborn as sns

porter_stemmer = PorterStemmer()

print (porter_stemmer.stem('learning'))


words = names.words()[:11]

print(words)
#print(len(words))

groups = fetch_20newsgroups()
print groups.keys()

print np.unique(groups.target)

print groups.data[1]


sns.distplot(groups.target)
plt.show()

'''
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
'''

