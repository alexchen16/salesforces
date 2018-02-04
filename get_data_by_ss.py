__author__ = 'chenlei'

import pytz
import datetime
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




sf = Salesforce(instance_url='https://seclink.my.salesforce.com/', session_id='00Db0000000IowA!AR0AQKrd0qY98dw7cba1KuSbqDngmVRnuhKnSPishf8UNgnJ8I9Rud5loHxLosSUq9IfWGBB_Afd2TX2Osgr_nh6wyz2vvWF')

end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this

response_cases = sf.Case.updated(end - datetime.timedelta(minutes=20), end)
#print type(response_json)

new_cases = case_list(response_cases)

fields = 'CDC_Milestone_1__c,CDC_Milestone_2__c,CDC_Milestone_1_min__c,CDC_Milestone_2_h__c'
for new_case in new_cases:
    #print 'new_case',new_case
    print 'ALL',sf.Case.get(new_case)
    #print 'CDC',sf.Case.get(new_case+'/?fields='+ fields)


#response_python = json.loads(response_json)

#print response_python



#query = 'SELECT id FROM Case'

#print sf.bulk.Case.query(query)