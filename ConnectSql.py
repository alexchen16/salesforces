__author__ = 'chenlei'
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb as mdb
class ConSql:
        def __init__(self,dbip,user,password,dbname):
            self.dbip = dbip
            self.user = user
            self.password = password
            self.dbname = dbname

        def get_data(self,ipaddr):
            con = None
            try:
                con = mdb.connect(self.dbip,self.user,self.password,self.dbname)
                cur = con.cursor()
                cur_result = cur.execute("select device_sysname,device_vendor from cmb_device where device_ip =%s", (ipaddr,))
                #cur_result = cur.execute("select device_sysname,device_vendor from cmb_device where device_ip ='10.50.255.3'")

                if cur_result:
                    print 'Getting data. Have found the existed node'
                    result = cur.fetchone()
                    sysname =  str(result[0])
                    vendor =  str(result[1])
                    print 'sysname and vendor is', (sysname,vendor)
                    cur.close()
                else:
                    print 'The node is not in the device list,please add the node into the device list at first'
                    return False

                if(vendor):
                    return sysname , vendor
                else:
                    return False

            finally:
                if con:
                    con.close()



        def put_data(self,ipaddr,configurl,savetime,content):
            con = None
            try:
                con = mdb.connect(self.dbip,self.user,self.password,self.dbname)
                cur = con.cursor()
            except:


                if cur.execute("select id from cmb_device where device_ip = %s",(ipaddr,)):
                    print 'Have found the existed node'
                    device_id =  str(cur.fetchone()[0])
                    print 'device id is',device_id
                    cur.executemany("insert into cmb_configbak (config_url,device_id,config_time,config_content) values (%s,%s,%s,%s)", [(configurl,device_id,savetime,content),])
                    #print 'method is',method
                    con.commit()
                    print 'Have inserted the config into database'
                    cur.close()
                else:
                    print 'The node is not in the device list,please add the node into the device list at first'

            finally:
                if con:
                    con.close()