__author__ = 'chenlei'

import pytz
import datetime
import Database
import json
from simple_salesforce import Salesforce

#return the cases list
def case_list(response):
    for key,value in response.items():
        if key == 'ids':
            #print 'key',key
            case_list = value
            #print 'case_list',case_list
            return case_list

db = Database.Database()


sf = Salesforce(instance_url='https://seclink.my.salesforce.com/', session_id='00Db0000000IowA!AR0AQFHyDESDn0s0pdFihaJ9OVbm3Xco5kTVy3zbY5bRjXYcY8Q3nqbwckDJMk0h4s2Gs0IZcLg63hwIQgj.dUyGkWuztRvi')

end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this

response_cases = sf.Case.updated(end - datetime.timedelta(minutes=50), end)
#print type(response_json)

new_cases = case_list(response_cases)

fields = 'CaseNumber,RecordTypeId,Reason'
        # 'Origin,Subject,Priority,Description,' \
        # 'CreatedDate,CDC_Milestone_1__c,CDC_Milestone_2__c,' \
        # 'CDC_Milestone_1_min__c,CDC_Milestone_2_h__c'
for new_case in new_cases:
    #print 'new_case',new_case
    #print 'ALL',sf.Case.get(new_case)
    case_attr = sf.Case.get(new_case+'/?fields='+ fields)
    print case_attr['CaseNumber']
    '''
    for key,value in case_attributes.items():
        if key == ''
        print 'key',key
        print 'value',value
    '''

    insert_query = "INSERT INTO cases (casenumber,reason) VALUES (%s,%s)" % (case_attr['CaseNumber'],'hello')
    #insert_query = "INSERT INTO cases (casenumber,recordtypeid,reason) VALUES (" + case_attr['CaseNumber'] + "," + case_attr['RecordTypeId'] + "," + case_attr['Reason'] + ")"
    #print type(insert_query)
    db.insert_many(insert_query)





#response_python = json.loads(response_json)

#print response_python



#query = 'SELECT id FROM Case'

#print sf.bulk.Case.query(query)