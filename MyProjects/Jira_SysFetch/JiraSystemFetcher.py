### This Code is written on Python- 2.7

import json
import pandas as pd
import win32com.client as win32



# Load Json Config file
with open('Configuration.json','r') as f:
    json_dict = json.load(f)


# Declaring Globals --
Input_FileName = json_dict["Input_FileName"]
Input_FieldSeperator = json_dict["Input_FieldSeperator"]
datafile_FilteringValues = json_dict["datafile_FilteringValues"]
datafile_RequiredColumns = json_dict["datafile_RequiredColumns"]
datafile_ColumnToBeFiltered = json_dict["datafile_ColumnToBeFiltered"]

mail_json_dict = json_dict["mailDetails"]
mail_To = mail_json_dict["mail_To"]
mail_CC =  mail_json_dict["mail_CC"]
mail_Subject = mail_json_dict["mail_Subject"]
mail_Body = mail_json_dict["mail_Subject"]


def preRequisites():
    ''' This Function is used to prefrom pre-reqisities operations like loading Input File'''
    
    # Load data into Memory with delimiter as variable-> Input_FieldSeperator
    datafile = pd.read_csv(Input_FileName, sep=Input_FieldSeperator)
    return datafile
    # Returns datafile which has all the data loaded in memory


def filterData(datafile, filter_Column, list_FilteringValues):
    ''' This Function is used to filter data acording to arguments '''
    ''' This function takes 3 Arguments. First one is the datafile variable. Second one is the Column on which filter should be applied. Third one is array of Filtering Constraints ["To Do", "Done"]) '''

    list_boolenVariable = datafile[filter_Column].isin(list_FilteringValues)
    return datafile[list_boolenVariable]
    # Returning an array of Filtered Rows

    

def getReqruiedColumns(datafile, list_ColumnsNeeded):
    ''' This Function returns only those colums that are provided in array Variable-> list_Columns_that_are_Needed and Convert DataFrame Object to Python List'''

    # Printing Final Data Frame before converting to python Array
    print("Final Data Frame is :- ")
    print(datafile[list_ColumnsNeeded])
    print("\n")

    return datafile[list_ColumnsNeeded].values.tolist()
    # Returning an arrya of only required Columns



def sendMail(Assignee, Status, IssueKey):
    ''' This Function is used to send Mail to required People '''
    # I dont know how to send mail so you have to complete this function Sweta
    
    print("Assignee is-> "+ Assignee)
    print("Status is-> "+ Status)
    print("Issue Key is-> "+ IssueKey)

    print("\n")
    print("For Each Value-- Mail Would be Send with following Details")
    print("To: "+ mail_To+"   CC: "+ mail_CC)
    print("Subject:- "+ mail_Subject)
    print("Mail Body:- "+ mail_Body)
    print("\n")

    try:
        print("Trying to Send mail but IDK HOW !")
    except Exception:
        print("Tere to Lagg gaye: "+Assignee)



def main():
    ''' This Function is main function. It acts as a wrapper function '''
    
    # Fetch Data into variable-> datafile
    datafile = preRequisites()

    # Apply Filter. Here variable-> datafile_FilteringValues contains filters as ["To Do", "Awaiting Deployment"]  from JSON Configuration
    # filterData(datafile, Column to be filtered, ["array of Filtering Values"]). This function returns an array of Filtered Rows
    df_filteredData = filterData(datafile, datafile_ColumnToBeFiltered, datafile_FilteringValues)

    
    # Get only Required Columns that is ["Assignee","Status","Issue key"] and Convert Data Frame Pandas Object to Python Array (list). So Now variable-> list_finalDatafile is a python list.
    # getReqruiedColumns(datafile, list of Columns that are needed)
    list_finalDatafile = getReqruiedColumns(df_filteredData, datafile_RequiredColumns)


    # Looping in array to send mail to each Assignee. Each SubArray is one row
    for subArray in list_finalDatafile:

        # Each SubArray is an array of -> [Assignee, Status, IssueKey]. Access Elements with thier Index subArray[2] is Issue Key
        sendMail(subArray[0], subArray[1], subArray[2])
        print("----- \n")

    # Program Ended !





# Start Point
if __name__ == "__main__":
    # Calling Main Function
    main()
