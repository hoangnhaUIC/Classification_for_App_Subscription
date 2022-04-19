# -*- coding: utf-8 -*-
"""IDS400_Final_Project_Group_B4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bR4gGdeFdcH-VbCRdW2aF01PPY681f5N
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline 
from sklearn.cluster import KMeans
from sklearn import datasets
import seaborn as sns
from sklearn.preprocessing import StandardScaler

appData=pd.read_csv("FineTech_appData.csv")
appData.head(10)

appData.isnull().sum()

appData.dtypes

appData['hour'] = appData.hour.str.slice(1,3).astype(int)

appData.dtypes

appData.describe()

appData

appVisual=appData[['user','dayofweek','hour','age','numscreens','minigame','used_premium_feature','enrolled','liked']]

# heatmap to find the corelation between the attributes w.r.t target variable

plt.figure(figsize=(12,10))
cor = appVisual.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

# we have found thet there is no strong corelation between any attributes.
# there is little corelation between numscreen and enrolled which mean those customer who enrolled for premimum app saw more screen
# and similarly between minigame and enrolled.
# there is slightly negative corelaton between age with enrolled and numscree which mean older customer do not enrolled for premium app and they don't see multiple screen

# Count for enrolled

sns.countplot(appData.enrolled)

print("OUT OF 50000")
print("No. of Not-Enrolled user :", (appData.enrolled<1).sum())
print("No. of Enrolled user :", (appData.enrolled==1).sum())

# plot histogram 
 
plt.figure(figsize = (16,9))
features = appVisual.columns 
for i,j in enumerate(features): 
    plt.subplot(3,3,i+1) 
    plt.title("Histogram of {}".format(j), fontsize = 15) 
     
    bins = len(appVisual[j].unique()) 
    plt.hist(appVisual[j], bins = bins, rwidth = 0.8, edgecolor = "y", linewidth = 2, ) 
     
plt.subplots_adjust(hspace=0.5)

# show corelation barplot 
 
sns.set() 
plt.figure(figsize = (14,5))
plt.title("Correlation all features with 'enrolled' ", fontsize = 20)
appVisual_1 = appVisual.drop(['enrolled'], axis = 1) 
ax =sns.barplot(appVisual_1.columns,appVisual_1.corrwith(appVisual.enrolled))  
ax.tick_params(labelsize=15, labelrotation = 20, color ="k")

from dateutil import parser

appData['first_open'] = pd.to_datetime(appData['first_open'])
appData['enrolled_date'] = pd.to_datetime(appData['enrolled_date'])

appData.dtypes

appData['totaltime']=(appData.enrolled_date - appData.first_open).astype('timedelta64[h]')

plt.hist(appData['totaltime'].dropna())

# distribution of time taken to enroll
plt.hist(appData['totaltime'].dropna(),range=(0,100))

# maximum customer enroll within 10 hours after the registration

"""# Feature Selection"""

appData.loc[appData.totaltime > 48, 'enrolled']=0

appData.drop(columns = ['totaltime', 'enrolled_date'], inplace=True)

dataS= pd.read_csv('top_screens.csv').top_screens.values
dataS

appData['screen_list'] = appData.screen_list.astype(str) + ','

for name in dataS:
    appData[name] = appData.screen_list.str.contains(name).astype(int)
    appData['screen_list'] = appData.screen_list.str.replace(name +",", "")

appData.shape

appData

appData.loc[0,'screen_list']

appData['remain_screen_list'] = appData.screen_list.str.count(",")

appData.drop(columns = ['screen_list'], inplace=True)

saving_screens = ['Saving1',
                  'Saving2',
                  'Saving2Amount',
                  'Saving4',
                  'Saving5',
                  'Saving6',
                  'Saving7',
                  'Saving8',
                  'Saving9',
                  'Saving10',
                 ]
appData['saving_screens_count'] = appData[saving_screens].sum(axis = 1)
appData.drop(columns = saving_screens, inplace = True)

credit_screens = ['Credit1',
                  'Credit2',
                  'Credit3',
                  'Credit3Container',
                  'Credit3Dashboard',
                 ]
appData['credit_screens_count'] = appData[credit_screens].sum(axis = 1)
appData.drop(columns = credit_screens, axis = 1, inplace = True)

cc_screens = ['CC1',
              'CC1Category',
              'CC3',
             ]
appData['cc_screens_count'] = appData[cc_screens].sum(axis = 1)
appData.drop(columns = cc_screens, inplace = True)

loan_screens = ['Loan',
                'Loan2',
                'Loan3',
                'Loan4',
               ]
appData['loan_screens_count'] = appData[loan_screens].sum(axis = 1)
appData.drop(columns = loan_screens, inplace = True)

appData.shape

plt.figure(figsize = (25,16)) 
sns.heatmap(appData.corr(), annot = True, linewidth =4)

appData["first_open"] = pd.to_datetime(appData["first_open"])

appData['first_month'] = appData["first_open"].dt.month

"""# Data Preprocessing"""

df_dummies = pd.get_dummies(appData, prefix='dayofweek', prefix_sep='.',columns=['dayofweek'])
df_dummies = pd.get_dummies(df_dummies, prefix='first_month', prefix_sep='.',columns=['first_month'])
#df_dummies = pd.get_dummies(df_dummies, prefix='hour', prefix_sep='.',columns=['hour'])
df_dummies=df_dummies.drop(["first_open"],1)
df_dummies.head()

appDataDP = df_dummies
target = df_dummies['enrolled']
df_dummies.drop(columns = 'enrolled', inplace = True)

from sklearn.model_selection import train_test_split
appDataDP=appDataDP.loc[:, (appDataDP != 0).any(axis=0)]
seed = 7
X_train, X_test, y_train, y_test = train_test_split(appDataDP, target, test_size = 0.3, random_state=seed)

train_userID = X_train['user']
X_train.drop(columns= 'user', inplace =True)
test_userID = X_test['user']
X_test.drop(columns= 'user', inplace =True)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)
X_test_sc = sc.transform(X_test)

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

"""## Logistic Regression"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

logit_model = LogisticRegression(random_state = seed, penalty = 'l2')
logit_model.fit(X_train, y_train)
y_pred = logit_model.predict(X_test)
print(accuracy_score(y_test, y_pred))
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logit_model.score(X_test, y_test)))

# train with Standard Scaling dataset
logit_model = LogisticRegression(random_state = seed, penalty = 'l2')
logit_model.fit(X_train_sc, y_train)
y_pred = logit_model.predict(X_test_sc)
print(accuracy_score(y_test, y_pred))print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logit_model.score(X_test, y_test)))

import statsmodels.api as sm
sm_model = sm.Logit(target, sm.add_constant(appDataDP)).fit(disp=0)
print(sm_model.pvalues)
sm_model.summary()

logit_model=sm.Logit(target,appDataDP)
result=logit_model.fit()
print(result.summary2())

"""## SVM"""

# train with Standard Scaling dataset

svc_model2 = SVC()
svc_model2.fit(X_train_sc, y_train)
y_pred_svc_sc = svc_model2.predict(X_test_sc)
 
accuracy_score(y_test, y_pred_svc_sc)

cm_SVM = confusion_matrix(y_test, y_pred_svc_sc)
sns.heatmap(cm_SVM, annot = True, fmt = 'g')
plt.title("Confussion Matrix", fontsize = 20)

"""## Random Forest"""

# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
 
accuracy_score(y_test, y_pred_rf)

# train with Standert Scaling dataset
rf_model2 = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
rf_model2.fit(X_train_sc, y_train)
y_pred_rf_sc = rf_model2.predict(X_test_sc)
 
accuracy_score(y_test, y_pred_rf_sc)

cm_RF = confusion_matrix(y_test, y_pred_rf_sc )
sns.heatmap(cm_RF, annot = True, fmt = 'g')
plt.title("Confussion Matrix", fontsize = 15)

"""# Additional experiment: Multiple Model"""

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
scoring = 'accuracy'
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold= model_selection.KFold(n_splits=10)
    cv_results= model_selection.cross_val_score(model, X_train_sc, y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg= "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)