# Requires: airtable-python wrapper
# Currently parses a CSV file instead of directly pulling data from Airtable
# Send a log of any suspicious activity
from airtable import Airtable
import pandas as pd

# base_key = 'app801qX3wwQdSaoT'
# api_key = 'keyVrbI2sZnDNOp5E'
# table = Airtable(base_key, 'E-Week Attendance 2019', api_key)
# records = table.get_all()

# finds difference in 24hr time
# also needs to check if start and end times follow the official start and end times
# test event is 30 min
# real events are 1 or 2 hours
def checkTime(time, time2):
    t1 = time.split()
    t2 = time2.split()
    t1[1] = t1[1].replace(':','')
    t2[1] = t2[1].replace(':', '')
    # we assume that t1 is sign-in and t2 is sign-out
    # because that's the order entries should be entered
    # then, we blacklist these EIDs so we won't double count them
    if t1[0] == t2[0] == timeDict["event3Date"] and abs(int(t1[1]) - timeDict["event3Start"]) <= 5 \
            and abs(int(t2[1]) - timeDict["event3End"]) <= 5:
        print('yeet')
# problem: only checking for one event

# need to separate entries by events
# then we can blacklist EIDs for events

blacklist = []
timeDict = {
    "event3Date": "7/24/2019",
    "event3Start": 930,
    "event3End": 1000
}
df = pd.read_csv('attendance.csv')
# print(df)

# is there a better way than iteration?
# this current blacklist only works if we iterate through a specific event
# otherwise, an EID gets blacklisted for all other events
for index, row in df.iterrows():
    eid = row['EID']
    if eid in blacklist:
        continue
    print(eid)
    event = row['Event']
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

            checkTime(time, time2)
            blacklist.append(eid)












