import os
import sys
import json
import random
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn import linear_model

# Load Json config
with open('Configuration.json','r') as f:
    json_dict = json.load(f)


# Declaring Globals --
g_Input_FilePath = json_dict['Input_FilePath']
g_Input_FileName = json_dict['Input_FileName']
g_Input_FieldSeperator = json_dict["Input_FieldSeperator"]
g_CSV_SubjectsToBeDropped = json_dict["CSV_SubjectsToBeDropped"]
g_CSV_ColumnHeaders = json_dict["CSV_ColumnHeaders"]

# Input for Predction
json_precition_dict = json_dict["Input_PredictionDetails"]
g_PD_KeytoSelectRow = json_precition_dict["PD_KeytoSelectStudent"]
g_PF_PredictForAllStudents = json_precition_dict["PF_PredictForAllStudents"]
g_PD_Value_StudentsToMoniterCode = json_precition_dict["PD_Value_StudentsToMoniterCode"]
g_PD_SubjectCode_SubjetToBePredicted = json_precition_dict["PD_SubjectCode_SubjetToBePredicted"]
g_PD_PerformPredictionOnColumn = json_precition_dict["PD_PerformPredictionOnColumn"]
g_PD_MinPredictionArrayLength = json_precition_dict["PD_MinPredictionArrayLength"]
g_PD_MaxPredictionArrayLength = json_precition_dict["PD_MaxPredictionArrayLength"]

# Output of Prediction
json_out_dict = json_dict["Output_PredictionResult"]
g_OP_Key_NameOfStudent = json_out_dict["OP_Key_NameOfStudent"]

# Correlation Dictonary
json_correlation_dict = json_dict["CSV_Subjects_Correlation"]


# Some geneal validations
if g_PD_MinPredictionArrayLength >= g_PD_MaxPredictionArrayLength:
    print("Prediction Max Array Length Could not be '>=' Prediction Min Array length")
    sys.exit()

if len(json_correlation_dict[g_PD_SubjectCode_SubjetToBePredicted]["relation_RelatedSubject"]) == 0:
    print("There are no correlated subjects for Subject Code: ",g_PD_SubjectCode_SubjetToBePredicted)
    sys.exit()

if g_CSV_ColumnHeaders.index(g_PD_PerformPredictionOnColumn) == -1:
    print("Cannot find Column Named: ",g_PD_PerformPredictionOnColumn)
    sys.exit()



def Average(lst):
    ''' Calculates the Average of provided List'''
    return int(sum(lst) / len(lst))
    # Return an Inegrate Value which is average of the Input List


def convertListToInt(lst):
    l_list_tempIntList = list()
    
    for value in lst:
        try:
            l_list_tempIntList.append(int(value))
        except:
            print("Cannot Convert this list to Int. Continuing: ", value)
            l_list_tempIntList.append(value)
            continue
    return l_list_tempIntList


def loadDataIntoMemory():
    ''' This Function is used for loading Input File'''
    
    # Join path with File name
    l_path_InputDataset = os.path.join(g_Input_FilePath, g_Input_FileName)

    # Load data into Memory with delimiter as variable-> g_Input_FieldSeperator
    l_datafile = pd.read_csv(l_path_InputDataset, sep=g_Input_FieldSeperator)
    return l_datafile
    # Returns dataframe which has all the data loaded in memory


def cleanData(dataset):
    ''' This Function is used to perform operations like deleting non-usefull subjects.'''

    # For Each Subject in list-> g_CSV_SubjectsToBeDropped  that is to be dropped, Append "_*" in it to make a regex-> abc_*. 
    # This will drop all the columns related to that subject
    for eachSubject in g_CSV_SubjectsToBeDropped:
        l_str_temp_subjectSubstr = eachSubject + "_*"
        dataset.drop(dataset.filter(regex=l_str_temp_subjectSubstr).columns , axis=1, inplace=True)

    return dataset
    # Return dataframe which has the updated dataset without extra subjects


def concatSubject_Column(subject, columnName):
    ''' This Function Concatinates Subjcets to Column with '_' '''
    return subject + "_" + columnName


def preRequisite(dataset):
    ''' This Function filters the input dataset (both rows and columns) and returns the desired list of Scores needed for prediction'''
    l_list_tempColumnName = list()

    # Get Correlated subjects for the Subject to be Predicted.
    l_list_CorrelatedSubjects = json_correlation_dict[g_PD_SubjectCode_SubjetToBePredicted]["relation_RelatedSubject"]
    
    # Filter Rows using Student's Unique Key (Required for Prediction)
    if g_PF_PredictForAllStudents:
        print("Flag PF_PredictForAllStudents is set to true. Thus performing Prediction for all Students")
    else:
        dataset = dataset[dataset[g_PD_KeytoSelectRow].isin(g_PD_Value_StudentsToMoniterCode)]
    
    # Prepare filter list of Columns using Column list (Required for Prediction)
    for subject in l_list_CorrelatedSubjects:
        l_list_tempColumnName.append( concatSubject_Column(subject,g_PD_PerformPredictionOnColumn))
    
    return dataset[g_PD_KeytoSelectRow].values.tolist(), dataset[l_list_tempColumnName].values.tolist()
    # Return list with filtered columns and Rows. (List is returned insteed of dataframe). Each Subarray here represent a student that is one row


def calcInverseDifference(list_dataset):
    ''' This Function is used to Calculate difference of all the elments of the provided list. '''
    l_list_tempDifferenceArray = list()
    
    for subArray in list_dataset:
        l_int_diff = int()
        for i in range (len(subArray)-1):
            l_int_diff = l_int_diff + (subArray[i+1] - subArray[i])
        l_list_tempDifferenceArray.append([abs(l_int_diff)]) # Get the Mod Value 

    return l_list_tempDifferenceArray
    # Returning a 2D list where each subArray includes Mod(difference of all elements of array).


def addDummyValues(list_dataset, list_inverseDifference):
    ''' This Function adds dummy values till variable-> g_PD_MinPredictionArrayLength to increase the training set'''
    l_list_ConvertedToIntDataset = list()

    for subArray in list_dataset:
        for differenceValue in list_inverseDifference:
            for i in range(1, g_PD_MaxPredictionArrayLength):
                if len(subArray) >= g_PD_MinPredictionArrayLength:
                    break
                subArray.append(Average(subArray) + random.randint(-1 * abs(differenceValue[0]), abs(differenceValue[0])))

    # Convert Each element of SubArray into Int
    for subArray in list_dataset:
        l_list_ConvertedToIntDataset.append(convertListToInt(subArray))

    return l_list_ConvertedToIntDataset
    # Returns a 2D list with dummy values, each of which is in Int format


def linearRegressionModel(l_2dArray_of_Students,l_list_inverseDifference):
    ''' This Function fits the lineral regression model with Training set and Retuns an array of Prediction along with slope and inverse Difference'''
    #print("LRM | Starting with Prediction. Model:- Linear Regression...")
    l_list_localPredictionValues = list()
    l_int_indexCounter = 0

    for subArray in l_2dArray_of_Students:
        # Preparing Input for Training
        # Convert Input into required format to fit the linear regression model and rehape it with -1,1
        l_list_yAxis = np.asarray(subArray).reshape(-1,1)
        l_list_xAxis = np.asarray(range(1,len(l_list_yAxis)+1)).reshape(-1,1)

        # Preparing Input for test set. Here it will be the next intermediate value of l_list_xAxis
        l_int_xTestValue = g_PD_MinPredictionArrayLength + 1
        # Convert Input to numpy array and reshape it
        l_npArray_xtestVaue = np.asanyarray(l_int_xTestValue).reshape(-1,1)

        # Initialize the Linearal Regress Model
        model = linear_model.LinearRegression()
        # Fit the Model with Input Data
        model.fit(l_list_xAxis,l_list_yAxis)

        # For returning the Coefficient of Determination      
        model.score(l_list_xAxis, l_list_yAxis)
        
        # Perform Peridiction by identifying the Slope of line and predicting the intermediate next Value
        predicted = model.predict(l_npArray_xtestVaue)
        
        # Append Subarray with format: [predicted Value, inverse Difference, Slope of Line]
        l_list_localPredictionValues.append([int(predicted), int(l_list_inverseDifference[l_int_indexCounter][0]) ,float("{0:.4f}".format(float(model.coef_)))])
        l_int_indexCounter += 1
        #print("LRM | Performed Prediction for Student: "+ str(l_int_indexCounter))
    
    print("LRM | Process Completed. Total Students Processed: "+ str(l_int_indexCounter))
    print("\n")
    return l_list_localPredictionValues
    # Returning List of Predictions along with Slope of line


def printResults(dataset, l_list_StudentSeatNumber, l_list_predictionList):
    ''' This Function Outputs everything on Terminal'''
    for student, subarray in zip(l_list_StudentSeatNumber,l_list_predictionList):
        print('Student Seat Number: ',student)
        print('Student Name: ',dataset[dataset[g_PD_KeytoSelectRow] == student][g_OP_Key_NameOfStudent].values.tolist())
        print('Subject to be Predicted: ', json_correlation_dict[g_PD_SubjectCode_SubjetToBePredicted]["relation_SubjectName"])
        print('Correlated Subjects: ', json_correlation_dict[g_PD_SubjectCode_SubjetToBePredicted]["relation_RelatedSubject"])
        print('Current Score: ',dataset[dataset[g_PD_KeytoSelectRow] == student][concatSubject_Column(g_PD_SubjectCode_SubjetToBePredicted,g_PD_PerformPredictionOnColumn)].values.tolist()[0])
        print('Predict Score: ',subarray[0])
        print('Prediction Score can vary in range +/-',subarray[1])
        print('Slop of line for this prediction :',subarray[2])
        print('This means for each exam that this Student gives, his performance in this subject will Increase/Decrease by: '+str(float("{0:.2f}".format(subarray[2])))+' %')
        print("-- -- -- -- \n")



def main():
    ''' This Function is main function. It acts as a wrapper Script '''
    
    # Call loadDataIntoMemory() function which loads and returns dataset into the memory.
    dataset = loadDataIntoMemory()

    # Make a Deep Copy
    OG_dataset = dataset

    # Call cleanData to remove extra columns and reuse the variable-> dataset to prevent memory leaks. 
    # Function cleanData takes 1 parameter that is dataset and Returns the updated data set by droping columns in configuration
    dataset = cleanData(dataset)

    # Call preRequisite to filter the dataframe for Students for which Scores should be predicted,
    # Subjetcs for which Prediction should be done and Category(InSem, Theory) for which prediction process is require
    # Reuse the variable-> dataset to prevent memory leaks. 
    list_studentsSeatNumber, dataset = preRequisite(dataset)

    # Call calcInverseDifference() that gets the differene of all the elements of list and then mod it.
    l_list_inverseDifference = calcInverseDifference(dataset)

    # Call addDummyValues() to increase the size of training dataset by adding Random numbers between range +/- Inverse Difference
    l_2dlist_yAxis = addDummyValues(dataset, l_list_inverseDifference)
    
    # Call the linear regression model which performs prediction and returns a set of 2d Array.
    l_list_PredictionList = linearRegressionModel(l_2dlist_yAxis, l_list_inverseDifference)

    # Print the Final Output
    printResults(OG_dataset, list_studentsSeatNumber, l_list_PredictionList)
    


if __name__ == "__main__":
    # Initialize the Start Variable
    startTime = datetime.now()

    # Call Master Function
    main()

    # Total Time Taken for Script
    print("-- --")
    print("Total time taken for the Script (HH:MM:SS:MS): ", datetime.now() - startTime)