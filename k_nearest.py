# -----------------------------------------Program Info--------------------------------------------#
# Author: Julian Linkhauer
# Created: 02/08/2019
# Last Modified: 04/08/2019
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

# Function: make_advice
# Purpose:
#   Generate simple advice for someone sitting in the chair based on sensor data
#   with all directions taken from the viewpoint of a person sitting in the chair
#   normally
# Input:
#   br_left     = backrest left sensor value
#   br_bottom   = backrest bottom sensor value
#   br_right    = backrest right sensor value
#   s_left      = seat left sensor value
#   s_left      = seat back sensor value
#   s_left      = seat right sensor value
# Output:
#   advice_string = String of statements to output based on sensor values in relation
#                   to each other
def make_advice(br_left,br_bottom,br_right,s_left,s_back,s_right):
    advice_string = "\n"
    if(br_left == 0 and br_right == 0 and br_bottom == 0 and s_left == 0 and s_right == 0 and s_back == 0):
        advice_string = advice_string + "No one is sitting in the chair\n"
    else:
        if((br_left == 0 and br_right == 0) or (br_bottom > br_left and br_bottom > br_right)):
            advice_string = advice_string + "You are leaning too far forward\n"
        elif(br_bottom == 0 or (br_left > br_bottom and br_right > br_bottom)):
            advice_string = advice_string + "You are leaning too far back\n"
        if(br_left > br_right):
            advice_string = advice_string + "You are leaning too far to your left\n"
        elif(br_right > br_left):
            advice_string = advice_string + "You are leaning too far to your right\n"
        if(s_back == 0 or (s_left > s_back and s_right > s_back)):
            advice_string = advice_string + "You are sitting too far forward\n"
        elif((s_left == 0 and s_right == 0) or (s_back > s_left and s_back > s_right)):
            advice_string = advice_string + "You are not resting your legs on the chair\n"
        if(s_left > s_right):
            advice_string = advice_string + "You are sitting too far to the left\n"
        elif(s_right > s_left):
            advice_string = advice_string + "You are sitting too far to the right\n"
    return advice_string


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
        score = score + abs(x - sum(sensor_values)/len(sensor_values))
    return score


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


# Function: make_prediction
# Purpose:
#   Use the model to make a class prediction based on the two scores
def make_prediction(model,back_score,seat_score):
    return model.predict([[back_score,seat_score]])

def main():
    model_data = get_data()                                       # Get data for model training and testing
    knn, data_table, test_in, test_out = make_model(model_data)  # Train model using input data
    #sns.set_context('notebook',font_scale=1.1)
    #sns.set_style('ticks')
    #sns.lmplot('Seat Score','Backrest Score', scatter=True,fit_reg=False,data=data_table,hue='Class')
    #plt.show()
    print('Accuracy: ', knn.score(test_in,test_out))               # Calculate model accuracy
    print('Confusion Matrix: ')
    print(confusion_matrix(test_out,knn.predict(test_in)))         # Display confusion matrix of test data
    new_data = [int(x) for x in input("Enter 6 Integer Values: ").split()] # Get new input from user
    back_score = generate_score(new_data[0:3])                     # Generate backrest score
    seat_score = generate_score(new_data[4:6])                     # Generate seat score
    print('Backrest Score: ', back_score)
    print('Seat Score: ', seat_score)
    print('Predicted Class: ', make_prediction(knn,back_score,seat_score)[0])
    print('Advice: ', make_advice(new_data[0],new_data[1],new_data[2],new_data[3],new_data[4],new_data[5]))

if __name__ == '__main__':
    main()
