import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup


# Load Json Config file
try:
    with open('ScrappingConfig.json', 'r') as f:
        json_dict = json.load(f)
except Exception:
    print("Web-Scrapper | There is a problem in Config")



# Define Globals
cwd = os.getcwd()
g_str_urlToHit = json_dict["input_URL"]
g_int_TableNumber = json_dict["input_Table_Number"]
g_csv_OutputName = json_dict["output_CSV_Name"]

# Column Count
g_Count_Column = int()
# Row Count
g_Count_Row = int()



def getValidUrl(l_str_urlToBeChecked):
    ''' This Function Checks if the Input URL is valid or not'''
    print("Web-Scrapper | Checking is URL is Valid. This step might take time depending upon internet speed...")
    l_str_website = requests.get(l_str_urlToBeChecked)
    
    if str(l_str_website.status_code) == '200':
        print("Web-Scrapper | Valid Website: Response Code ["+(str(l_str_website.status_code))+"] \n")
        return l_str_website
    else:
        print("Web-Scrapper | Please Enter a Valid Website \n")
        return False


def convertListToDataframe(l_list_headers, l_list_data):
    ''' This function is used to convert the supplied List into Dataframe. Format(Headers, Data)'''
    return pd.DataFrame(l_list_data, columns = l_list_headers )


def extractHeaders(l_soup_table):
    ''' This function extract Headers from the provided table '''

    print("Web-Scrapper | Fetching Headers... \n")
    l_list_TableHeaders = list()
    
    l_soup_tableHeaders = l_soup_table.find_all('th')

    for data in l_soup_tableHeaders:
        l_list_TableHeaders.append(data.contents)

    if len(l_list_TableHeaders) == 0:
        print("Web-Scrapper | No Headers Found")
        print("Web-Scrapper | Assigning Column Names like 1,2,3... \n")
        l_list_TableHeaders = list(range(1,g_Count_Column+1))
    
    return l_list_TableHeaders


def extractData(l_soup_table):
    ''' This function extract Data from the provided table '''

    print("Web-Scrapper | Fetching Data...")
    global g_Count_Column, g_Count_Row
    l_list_TableData = list()

    # get a list of table rows
    l_soup_tableRows = l_soup_table.find_all('tr')
    
    for rows in l_soup_tableRows:
        l_list_tempTableRow = list()
        for data in rows.find_all('td'):
            l_list_tempTableRow.append(data.contents)

        l_list_TableData.append(l_list_tempTableRow)
    
    #print(convertListToDataframe(l_list_TableData))
    g_Count_Column = len(rows.find_all('td'))
    g_Count_Row = len(l_soup_tableRows)

    return l_list_TableData
    





def main():
    ''' Main function. used to call subfunctions and act like a wrapper'''
    # check if URL is Valid or Not
    print("Web-Scrapper | URL: "+g_str_urlToHit)
    
    # Variable that holds HTML Content
    l_webpage = getValidUrl(g_str_urlToHit)

    # Convert it to Beautiful Soup format
    l_soup_webpage = BeautifulSoup(l_webpage.content, 'html.parser')
    
    # find Table and filter it...
    l_soup_tables = l_soup_webpage.find_all('table')
    l_soup_tables = l_soup_tables[g_int_TableNumber]
       
    # Get Table Data.
    l_list_tableData = extractData(l_soup_tables)
    # Get Table Headers.
    l_list_tableHeaders = extractHeaders(l_soup_tables)
    print("Web-Scrapper | Number of Columns found: "+str(g_Count_Column))
    print("Web-Scrapper | Number of Rows found: "+str(g_Count_Row))
    print("")
    
    # Convert list to Data Frame to use Pandas for Exporting
    l_dataframe_CSV = convertListToDataframe(l_list_tableHeaders, l_list_tableData)

    # Export to CSV
    print("Web-Scrapper | Exporting data to CSV.")
    l_dataframe_CSV.to_csv(cwd+'\\'+g_csv_OutputName, header=True, index = None)
    print("Web-Scrapper | Export done. \n")
    print("Web-Scrapper | CSV Exported to path->   "+cwd+"\\")


    



    
    





if __name__ == "__main__":
    # Call Main Function
    main()