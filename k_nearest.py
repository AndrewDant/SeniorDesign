# -----------------------------------------Program Info--------------------------------------------#
# Author: Julian Linkhauer
# Created: 02/08/2019
# Last Modified: 03/04/2019
# Purpose: Generate a classified scatter plot based on random input data using KNN
# -------------------------------------------------------------------------------------------------#

# Import statements
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


# Function: get_data
# Purpose:
#   Get data to be used for training and testing of the model from a .csv file
# Output:
#   data = data to be used for training and testing of the model
def get_data():
    data = pd.read_csv('rand_data.csv')  # Read Data from File
    data.columns = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'Y']  # Label columns of data
    return data


# Function: make_model
# Purpose:
#   Build and train a KNN model to be used for classifying posture as either 'Good' or 'Bad'
# Inputs:
#   data = data to be used to train and test model
#   num_neighbors = number of neighbors to use with knn algorithm
# Outputs:
#   knn = classification model being used
#   data_scores = scores generated based on input data
#   test_in = inputs from sample data to be used for testing
#   test_out = outputs from sample data to be used for testing
def make_model(data, num_neighbors=5):
    knn = KNeighborsClassifier(n_neighbors=num_neighbors)
    data_in = data.values[:, 0:6]
    data_out = data.values[:, 6]
    data_scores = [[0, 0] for x in range(np.size(data_in, 0))]
    for x in range(np.size(data_in, 0)):
        data_scores[x][0] = generate_score(data_in[x][0:3])
        data_scores[x][1] = generate_score(data_in[x][3:6])
    data_table = pd.DataFrame(data_scores)
    data_table.columns = ['Backrest Score', 'Seat Score']
    data_table['Class'] = data_out
    train_in, test_in, train_out, test_out = train_test_split(data_scores, data_out, test_size=0.3)
    knn.fit(train_in, train_out)
    return knn, data_table, test_in, test_out


# Function: generate_score
# Purpose:
#   Generate a numerical score for a set of data retrieved from sensors based on the sum 
#   of absolute errors of each sensor value. Scores should be generated based on 3 values
#   at a time for 2 scores in total (1 score representing the backrest and 1 for the seat).
# Input:
#   sensor_values = array of values to generate a score on
# Output:
#   score = numeric score generated by summing absolute errors
def generate_score(sensor_values):
    score = 0
    for x in sensor_values:
        score = score + abs(x - sum(sensor_values) / len(sensor_values))
    return score


# Function: make_prediction
# Purpose:
#   Use the model to make a class prediction based on the two scores
def make_prediction(model, back_score, seat_score):
    return model.predict([[back_score, seat_score]])


def main():
    model_data = get_data()  # Get data for model training and testing
    knn, data_table, test_in, test_out = make_model(model_data)  # Train model using input data
    return knn


if __name__ == '__main__':
    main()
