import csv, os.path, requests, datetime
from config import *

def dateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def getDailyHistoricData(API_URL, file_type, file_location, start_date, end_date):
    for single_date in dateRange(start_date, end_date):
        # API URL for desired file
        fileURL = "{}{}.{}".format(API_URL, single_date.strftime("%Y%m%d"), file_type)
        myfile = requests.get(fileURL)
        # Relative file path to save requested document 
        fullFilePath = "{}{}.{}".format(file_location, single_date.strftime("%Y%m%d"), file_type)
        if myfile.status_code == 200:           # Skips requesting API URLs that do not exist
            if os.path.isfile(fullFilePath):    # Skips redownloading files
                print ("{} File exists".format(fullFilePath))
            else:
                open("{}{}.{}".format(file_location, single_date.strftime("%Y%m%d"), file_type), 'wb').write(myfile.content)
                print("SUCCESSFULLY DOWNLOADED {}{}.{}".format(file_location, single_date.strftime("%Y%m%d"), file_type))
        else:
            print("{} does not exist".format(fileURL))

def getAPIData(Base_URL, file_name, file_type, file_location):
    myfile = requests.get("{}/{}.{}".format(Base_URL, file_name, file_type))
    if myfile.status_code == 200:
        open("{}/{}.{}".format(file_location, file_name, file_type), "wb").write(myfile.content)
        print("{}/{}.{}".format(file_location, file_name, file_type))
    else:
        print ("{} does not exist".format(Base_URL))


# Request all US daily files
getDailyHistoricData(API_URL["usDaily"], FILE_TYPE, FILE_LOCATION["usDaily"], START_DATE, END_DATE)

# Cycle through all states
for state in STATES:
    URL = "{}{}/".format(API_URL["statesDaily"], state)
    file_path = "{}{}/".format(FILE_LOCATION["statesDaily"], state)
    getDailyHistoricData(URL, FILE_TYPE, file_path, START_DATE, END_DATE)

# Download singular race files
getAPIData(API_URL["raceSeparate"],RACE_FILES["separate"],FILE_TYPE, FILE_LOCATION["raceSeparate"] )
getAPIData(API_URL["raceCombined"],RACE_FILES["combined"],FILE_TYPE, FILE_LOCATION["raceCombined"] )