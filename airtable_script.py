#requires: airtable-python wrapper
from airtable import Airtable
import pandas as pd
import time

base_key = 'app801qX3wwQdSaoT'
api_key = 'keyVrbI2sZnDNOp5E'

at = Airtable(base_key, 'Imported table', api_key)
points = Airtable(base_key, 'Leaderboard', api_key)

def at_to_csv(df):
        df.to_csv('out.csv', index = False)
        
def clear_score(pts):
        for index, row in pts.iterrows():
                record = points.match('Name', row['Name'])
                fields = {'Sign-In Points': 0}
                points.update(record['id'], fields)
        
def update_score(df, prev):
        #cut out old sign ins
        df2 = df.iloc[len(prev.index):]
        
        for index, row in df2.iterrows():
                eid = row['UT EID']
                evnt = row['Event']
                so = row['Signing-In or Signing-Out']
                org = row['Organization']
                for index, row in df.iterrows():
                    if eid == row['UT EID'] and evnt == row['Event'] and org == row['Organization'] and so != row['Signing-In or Signing-Out']:
                        record = points.match('Name', row['Organization'])
                        fields = {'Sign-In Points': record['fields']['Sign-In Points'] + .5}
                        points.update(record['id'], fields)
                    
#start timing                        
start = time.time()

#get records from pts and sign in
records = at.get_all()
pts_records = points.get_all()

#create dataframes for pts, sign ins and previous sign ins
try:
    prev = pd.read_csv('out.csv')
except:
    prev = pd.DataFrame()
    pass
pts = pd.DataFrame.from_records((r['fields'] for r in pts_records))
df = pd.DataFrame.from_records((r['fields'] for r in records))

#clear and update scores
clear_score(pts)
update_score(df, prev)
at_to_csv(df)

#stop timing
end = time.time()

#calculate time
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


