# Requires: airtable-python wrapper
# Currently parses a CSV file instead of directly pulling data from Airtable
# Currently catches multiple entries with same ut eid
# Ensures that entries are within submission time periods
# Send a log of any suspicious activity
# TODO: big concern is false UT EIDs; will need to have an automated way to confirm
# TODO: figure out how time-stamping parameters will work

from airtable import Airtable
import pandas as pd
import pdb

# TODO: directly pull data from Airtable instead of parsing csv
# constants is an gitignored file which holds Airtable API information
# from constants import BASE_KEY, API_KEY
# base_key = BASE_KEY
# api_key = API_KEY
# table = Airtable(base_key, 'E-Week Attendance 2019', api_key)
# records = table.get_all()
#
# df = pd.DataFrame.from_records((r['fields'] for r in records))
# for index, row in df.iterrows():
#     str = row['Timestamp'].replace('T',' ')
#     str2 = str[0:-8]
#     row['Timestamp'] = str2

# finds difference in 24hr time
# test event is 30 min
# real events are 1 or 2 hours
def checkTime(time, time2, event, eid):
    t1 = time.split()
    t2 = time2.split()
    t1[1] = t1[1].replace(':','')
    t2[1] = t2[1].replace(':','')
    # we assume that t1 is sign-in and t2 is sign-out
    # because that's the order entries should be entered
    # then, we blacklist these EIDs so we won't double count them

    # vars for timeDict keys
    start = event + " Start"
    end = event + " End"
    print(timeDict[event])
    print(abs(int(t1[1]) - timeDict[start]))
    print(abs(int(t2[1]) - timeDict[end]))
    # TODO: this conditional works, but can definitely use a better way to solve it
    if t1[0] == t2[0] == timeDict[event] and (abs(int(t1[1]) - timeDict[start]) <= 5
            or 41 <= abs(int(t1[1]) - timeDict[start]) <= 45) and (abs(int(t2[1]) - timeDict[end]) <= 5
            or 41 <= abs(int(t2[1]) - timeDict[end]) <= 45):
        print('Good')
        success.append(eid + " " + event)
        return True

    return False


# this blacklist stores "EID + Event"
# prevents someone from filling in multiple entries for an
# event with the same EID
blacklist = []
success = []
cheaters = []

# we need to know what times the forms are open to fill out
# Airtable has different date format
timeDict = {
    "Event 1": "7/22/2019",
    "Event 1 Start": 200,
    "Event 1 End": 230,
    "Event 2": "7/23/2019",
    "Event 2 Start": 1400,
    "Event 2 End": 1500,
    "Event 3": "7/24/2019",
    "Event 3 Start": 930,
    "Event 3 End": 1000
    # "Event 1": "2019-07-22",
    # "Event 1 Start": 200,
    # "Event 1 End": 230,
    # "Event 2": "2019-07-23",
    # "Event 2 Start": 1400,
    # "Event 2 End": 1500,
    # "Event 3": "2019-07-24",
    # "Event 3 Start": 930,
    # "Event 3 End": 1000
}

df = pd.read_csv('attendance.csv')
print(df)
# pdb.set_trace()

# this makes sure the entries we check are all in pairs of sign-in/out
for index, row in df.iterrows():
    eid = row['EID']
    event = row['Event']
    if eid + event in blacklist:
        print(eid + event)
        continue
    print(eid)
    status = row['Signing-In or Signing-Out']
    if status != "Signing-In":
        # print("100000000")
        continue
    time = row['Timestamp']
    print(time)
    for index2, row2 in df.iterrows():
        if eid == row2['EID'] and event == row2['Event'] and status != row2['Signing-In or Signing-Out']:
            time2 = row2['Timestamp']
            print(time2)

            # these parameters assume that time = sign-in and time2 = sign-out
            # we make sure this is the case in the script
            # need event parameter to find correct dictionary entry
            if checkTime(time, time2, event, eid) is False:
                cheaters.append(eid + " " + event)
            blacklist.append(eid + event)


print("Blacklist")
print(blacklist)
print("Correct Attendance Log")
print(success)
print("Suspicious Attendance Log")
print(cheaters)






