#-----------------------------------------Program Info--------------------------------------------#
# Author: Julian Linkhauer
# Created: 02/08/2019
# Last Modified: 02/11/2019
# Purpose: Generate a classified scatter plot based on random input data using KNN
#-------------------------------------------------------------------------------------------------#

#Import statements
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv('rand_data.csv') #Get data from file

df.columns = ['X1', 'X2', 'Y'] #Label columns of data

#Prepare visuals
sns.set_context('notebook', font_scale=1.1) 
sns.set_style('ticks')

#Plot graph
sns.lmplot('X1','X2',scatter = True, fit_reg=False, data=df, hue = 'Y')
plt.ylabel('X2')
plt.xlabel('X1')

#Pick k value; choose colums for X and Y
neighbors = KNeighborsClassifier(n_neighbors=5)
X = df.values[:,0:2]
Y = df.values[:,2]

#Split data for training and testing (test_size = % of data to be used for testing)
trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.3)

#Train Model with training data
neighbors.fit(trainX, trainY)

#Test model with testing data
print('Accuracy: ', neighbors.score(testX,testY))

#Show the plot
plt.show()