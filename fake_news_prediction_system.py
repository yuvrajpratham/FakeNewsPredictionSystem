# -*- coding: utf-8 -*-




import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

# printing the stopwords in English
print(stopwords.words('english')) #remove all those text that does not add value to our data set

"""Data Pre-processing"""

# loading the dataset to a pandas DataFrame
#loads the data to a more structured table
news_dataset = pd.read_csv('/content/train.csv')#reads the file

news_dataset.shape #checks no of rows(news articles ),column(feature)

# print the first 5 rows of the dataframe
news_dataset.head()

# counting the number of missing values in the dataset
news_dataset.isnull().sum() #isnull function is used ..ye dhund lega jo "null" hai... and un sab ko sum ker lega using "sum function"

# replacing the null values with empty string
news_dataset = news_dataset.fillna('')

# merging the author name and news title
news_dataset['content'] = news_dataset['author']+' '+news_dataset['title']#combine

print(news_dataset['content'])

# separating the data & label
X = news_dataset.drop(columns='label', axis=1)#jis basis pe graph banega #removing column
#drop function
Y = news_dataset['label']

print(X)
print(Y) #verifying this

"""____________________________________________________________

**Stemming:**

Stemming is the process of reducing a word to its Root word

example: actor, actress, acting --> act

cuz baaki prefix and suffix are useless
"""

port_stem = PorterStemmer()

def stemming(content): #creating a function
    stemmed_content = re.sub('[^a-zA-Z]',' ',content) #substitutes surname values ---> "^" meanis exclusion
    stemmed_content = stemmed_content.lower() #convert all to lower case letters
    stemmed_content = stemmed_content.split()#spliting it to lists
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]#for loop
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

news_dataset['content'] = news_dataset['content'].apply(stemming)

print(news_dataset['content'])

#separating the data and label
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(X)

print(Y)

"""**CONVERTING textual data to numerical data**"""

# converting the textual data to numerical data
vectorizer = TfidfVectorizer()#FIND THE NUMBERS WHICH ARE REPEATING MULTIPLE TIMES AND THOSE ARE NOT THAT SIGNIFICANT
vectorizer.fit(X)

X = vectorizer.transform(X)#CONVERTING ALL VALUES TO RESPECTIVE FEATURE

print(X)

"""**Splitting the dataset to training & test data**"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify=Y, random_state=2) #20% OF TOTAL DATA TO TEST DATA
#stratify beacuse data should  be the same as the test data
#random_state =2 same manner spliting

"""**Training the Model: Logistic Regression**"""

model = LogisticRegression()

model.fit(X_train, Y_train)

"""**                                 Evaluation**

**accuracy score**
"""

# accuracy score on the training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of the training data : ', training_data_accuracy)

# accuracy score on the test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score of the test data : ', test_data_accuracy)

"""---------------------------------------------------------------

**Making a Predictive System**
"""

X_new = X_test[3]

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==0):
  print('The news is Real')
else:
  print('The news is Fake')

print(Y_test[3])

