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


def notify_flag(indicator,case_number,notify_time):
    flag = indicator + '_flag_' + str(notify_time)
    db.insert("INSERT INTO cases notify_flag VALUES \'%s\' WHERE casenumber=\'%s\'"% (flag,case_number))


def KPI():
    #print 'Enter the KPI'
    KPI_query = "SELECT casenumber,priority,createddate FROM `cases` WHERE CDC_Milestone_1__c=0 and notify_flag = 'None'"
    results = db.query(KPI_query)
    #print type(results)
    time_now = datetime.datetime.now(pytz.UTC)
    print time_now
    #fmt = '%Y-%m-%d %H:%M:%S'
    #print datetime.datetime.strptime(time_now, fmt)

    for result in results:
        #print type(result['createddate'])
        #print type(time_now)
        case_created_time = pytz.UTC.localize(result['createddate'])
        #print 'case_created_time',case_created_time
        minutes_delta = (time_now - case_created_time).total_seconds()/60
        if minutes_delta > 15:
            print 'Will Alert'
            notify_flag('KPI',result['casenumber'],15)

            #print minutes_delta
            #print result['casenumber']







db = Database.Database()


sf = Salesforce(instance_url='https://seclink.my.salesforce.com/',session_id='00Db0000000IowA!AR0AQFNQ5PZdGThHSTARpFApkTscYtIhlQCFNMZHmaxgR7WNE5OVIxA9.PgihuLhKQyhUp5ih09vjltsNGA3DpLtycqnhmBq')

end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this

response_cases = sf.Case.updated(end - datetime.timedelta(minutes=300), end)
#print type(response_json)


new_cases = case_list(response_cases)
fields = 'CaseNumber,RecordTypeId,Reason,'\
         'Origin,Subject,Priority,Description,' \
         'CreatedDate,CDC_Milestone_1__c,CDC_Milestone_2__c,' \
         'CDC_Milestone_1_min__c,CDC_Milestone_2_h__c'
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

    insert_query = "INSERT INTO cases " \
                   "(CaseNumber,RecordTypeId,Reason,Origin,Subject,Priority,Description,CreatedDate,CDC_Milestone_1__c,CDC_Milestone_2__c,CDC_Milestone_1_min__c,CDC_Milestone_2_h__c,notify_flag)" \
                   " VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % \
                   (case_attr['CaseNumber'],case_attr['RecordTypeId'],case_attr['Reason'],case_attr['Origin'],case_attr['Subject'],case_attr['Priority'],case_attr['Description'],case_attr['CreatedDate'],case_attr['CDC_Milestone_1__c'],case_attr['CDC_Milestone_2__c'],case_attr['CDC_Milestone_1_min__c'],case_attr['CDC_Milestone_2_h__c'],'None')
    #insert_query = "INSERT INTO cases (casenumber,recordtypeid,reason) VALUES (" + case_attr['CaseNumber'] + "," + case_attr['RecordTypeId'] + "," + case_attr['Reason'] + ")"
    #print type(insert_query)
    db.insert(insert_query)

KPI()
#print datetime.datetime.now(pytz.UTC)









#response_python = json.loads(response_json)

#print response_python



#query = 'SELECT id FROM Case'

#print sf.bulk.Case.query(query)