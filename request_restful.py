# -*- coding: UTF-8 -*-
__author__ = 'chenlei'

import requests

#res = requests.get('https://stackoverflow.com')

#print res.text

token ='00Db0000000IowA!AR0AQKrd0qY98dw7cba1KuSbqDngmVRnuhKnSPishf8UNgnJ8I9Rud5loHxLosSUq9IfWGBB_Afd2TX2Osgr_nh6wyz2vvWF'
url = 'https://seclink.my.salesforce.com/services/data/v20.0/sobjects/Case/5000X00001NMhR3QAL'
data = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
    'X-PrettyPrint': '1'
}

response = requests.post(url, data=data)

print 'response',response.text
