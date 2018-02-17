__author__ = 'chenlei'
# -*- coding: UTF-8 -*-

import pytz
import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from simple_salesforce import Salesforce
import time

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_mail(casenumber,createddate,priority,timeleft):
    #from_addr = 'cdc_sh@tom.com'
    #from_addr = 'sh_cdc_monitor@126.com'
    from_addr = ''
    #password = '$cdcsh123'
    password = ''
    to_addr = ['']
    #to_addr = ",".join(to_list)
    #print to_addr
    smtp_server = 'smtp.sina.com'

    msg_subject = 'Case:' + casenumber
    msg_body = 'CaseNumber:' + casenumber + '\r\nPriority:' + priority + '\r\nCreatedTime(Shanghai):' + createddate + '\r\nTime_left:' + str(timeleft) + ' minutes'
    print unicode(str(msg_body))


    msg = MIMEText(unicode(str(msg_body)), 'plain', 'utf-8')

    msg['From'] = _format_addr(u'KPI_Notification <%s>' % from_addr)
    msg['To'] = _format_addr(u'China_CDC <%s>' % to_addr)
    msg['Subject'] = Header(msg_subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


def cal_time(createddate):
    print createddate
    time_now = datetime.datetime.now(pytz.UTC)
    created_time = datetime.datetime.strptime(createddate, '%Y-%m-%dT%H:%M:%S.000+0000')

    case_created_time = pytz.UTC.localize(created_time)
    tz = pytz.timezone('Asia/Shanghai')
    case_created_time_SH = pytz.utc.localize(created_time, is_dst=None).astimezone(tz)
    print type(case_created_time_SH)
    minutes_delta = (time_now - case_created_time).total_seconds()/60
    if int(minutes_delta) > 0:
        return_time = case_created_time_SH.strftime('%Y-%m-%d %H:%M:%S')
        print case_created_time,case_created_time_SH
        return int(minutes_delta),return_time
    else:
        return False,False





def case_list(response):
    for key,value in response.items():
        if key == 'ids':
            case_list = value
            return case_list



def main(sf,dmin):

    end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this
    try:
        response_cases = sf.Case.updated(end - datetime.timedelta(minutes=dmin), end)
    except:
        return False

    #print 'response_cases is OK'

    new_cases = case_list(response_cases)
    fields = 'CaseNumber,CreatedDate,Priority,Status'

    for new_case in new_cases:

        case_attr = sf.Case.get(new_case+'/?fields='+ fields)
        if case_attr['Status'] == 'New':
            TimeUsed,SH_Time = cal_time(case_attr['CreatedDate'])
            print TimeUsed, SH_Time
            if TimeUsed:
                send_mail(case_attr['CaseNumber'],SH_Time,case_attr['Priority'],int(30-TimeUsed))
    return True


if __name__ == '__main__':
    s_id = ''
    sf = Salesforce(instance_url='',session_id=s_id)
    #print sf
    while main(sf,300):
        print '%s: working' % datetime.datetime.now()
        time.sleep(298)

    send_mail('Notification System Failure','None','None','None')
