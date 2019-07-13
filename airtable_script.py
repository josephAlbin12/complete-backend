#requires: airtable-python wrapper

from airtable import Airtable
import pandas as pd

base_key = 'app801qX3wwQdSaoT'
api_key = 'keyVrbI2sZnDNOp5E'


at = Airtable(base_key, 'E-Week Attendance 2019', api_key)
points = Airtable(base_key, 'Leaderboard', api_key)

orgs_list = ['AICHE', 'ASCE', 'ASME', 'BMESF', 'IEEE', 'SNaP', 'SWEEP',
             'PGE', 'Longhorn Racing', 'AEI', 'EChO', 'ESW', 'HKN', 'KTE',
             'SASE', 'SFE', 'TBP', 'TxTPEG', 'WIALD']

def at_to_csv(df):
        df.to_csv('out.csv', index = False)
        
def clear_score(df):
        for index, row in df.iterrows():
            if row['Organization'] in orgs_list:
                record = points.match('Name', row['Organization'])
                fields = {'Sign-In Points': 0}
                points.update(record['id'], fields)
        
def update_score(df):        
        clear_score(df)
                
        for index, row in df.iterrows():
            eid = row['EID']
            evnt = row['Event']
            so = row['Signing-In or Signing-Out']
            org = row['Organization']
            for index, row in df.iterrows():
                if eid == row['EID'] and evnt == row['Event'] and org == row['Organization'] and so != row['Signing-In or Signing-Out']:
                    if row['Organization'] in orgs_list:
                        record = points.match('Name', row['Organization'])
                        fields = {'Sign-In Points': record['fields']['Sign-In Points'] + .5}
                        points.update(record['id'], fields)

records = at.get_all()
df = pd.DataFrame.from_records((r['fields'] for r in records))
update_score(df)