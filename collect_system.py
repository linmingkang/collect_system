# -*- coding: UTF-8 -*-
import os,time, pymysql, datetime


ping_interval = 3
db_user = 'root'
db_password = 'bjtungirc'

#读取配置文件参数
# try:
#     file_r = open('/home/chsr/cf.d/groundusr.conf', 'r')
#     file_r.readline()
#     file_r.readline()
#     db_user = file_r.readline()[len('mysqluser='):].strip()
#     db_password = file_r.readline()[len('mysqlpasswd='):].strip()
#     file_r.close()
# except:
#     print('配置文件groundusr.conf异常，该文件是否存在？该文件的内容格式是否符合规范？请相关人员检查。')
#     exit()

db_host = '127.0.0.1'
db_port = 3306
db_name = 'study'

#执行sql语句的方法
def db_insert_update_del(cursor, sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

#连接数据库
def db_connect():
    try:
        db = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name
        )
        return db
    except:
        print('mysql数据库连接失败.\n程序退出')
        exit()
db=db_connect()
cursor = db.cursor()
cursor.execute('select device_id,service_ip from deviceinfo;')
id_lists = cursor.fetchall()
db.commit()
ping_ips={}
last_ping={}
online_time={}
sql = 'delete from device_status'
db_insert_update_del(cursor, sql)
for message in id_lists:
    #print(message)
    ping_ips[message[0]]=message[1]
    last_ping[message[0]]=0
    online_time[message[0]]=''
    sql = "insert into device_status values(0,'%s','%s','0');" % (message[0],message[1])
    db_insert_update_del(cursor, sql)
    #print(ping_ips)


while True:
    for device_id, service_ip in ping_ips.items():
        ping_res = os.popen('ping -c 1 -w 1 %s' % service_ip).read()
        ping = 0
        if '1 received' in ping_res:
            ping = 1
        if ping == 0:   # pingbutong
                sql = "update device_status set service_ip='%s',online_flag = 0 where device_id = '%s';" % (service_ip,device_id)
                db_insert_update_del(cursor, sql)
                if ping != last_ping[device_id]:
                    off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #sql = "delete from mar_connectivity where device_id='%s' and offline_time is null;" % device_id
                    #db_insert_update_del(cursor, sql)
                    #sql = "insert into mar_connectivity(device_id, online_time, offline_time) values('%s', '%s', '%s');" % (device_id, online_time[device_id], off)
                    sql = "update mar_connectivity set offline_time='%s' where device_id = '%s' and online_time='%s';" % (off, device_id,online_time[device_id])
                    db_insert_update_del(cursor, sql)
                #print(sql)
                else:
                    cursor = db.cursor()
                    sql = "select * from mar_connectivity where device_id='%s' and offline_time is null;" % device_id
                    cursor.execute(sql)
                    old_data = cursor.fetchall()
                    if old_data:
                        old_data1 = list(zip(*old_data))[2]
                        online_time[device_id] = old_data1[0]
                        off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        sql = "delete from mar_connectivity where device_id='%s' and offline_time is null;" % device_id
                        db_insert_update_del(cursor, sql)
                        sql = "insert into mar_connectivity(device_id, online_time, offline_time) values('%s', '%s', '%s');" % (device_id, online_time[device_id], off)
                        db_insert_update_del(cursor, sql)
                        #sql = "update mar_connectivity set offline_time='%s' where device_id = '%s';" % (off, device_id)
                        #db_insert_update_del(cursor, sql)
        else:   # pingtong
                sql = "update device_status set service_ip='%s',online_flag = 1 where device_id = '%s';" % (service_ip,device_id)
                db_insert_update_del(cursor, sql)
                #print(sql)
                if ping != last_ping[device_id]:
                    cursor = db.cursor()
                    sql = "select * from mar_connectivity where device_id='%s' and offline_time is null;" % device_id
                    cursor.execute(sql)
                    old_data = cursor.fetchall()
                    if old_data:
                        old_data1 = list(zip(*old_data))[2]
                        online_time[device_id] = old_data1[0]
                    else:
                        online_time[device_id] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        sql = "insert into mar_connectivity(device_id, online_time) values('%s', '%s');" % (device_id, online_time[device_id])
                        db_insert_update_del(cursor, sql)
        last_ping[device_id] = ping
    db = db_connect()
    cursor = db.cursor()
    cursor.execute('select device_id,service_ip from deviceinfo;')
    aaa = cursor.fetchall()
    db.commit
    if(aaa):
        aaa1 = list(zip(*aaa))[0]
        #print(ping_ips)
        for b in list(ping_ips):
            if b not in aaa1:
                ping_ips.pop(b)
                last_ping.pop(b)
                online_time.pop(b)
                sql = "delete from device_status where device_id = '%s'" % b
                db_insert_update_del(cursor, sql)
        for a in aaa:
            if a[0] not in ping_ips:
                ping_ips[a[0]] = a[1]
                last_ping[a[0]] = 0
                online_time[a[0]] = ''
                sql = "insert into device_status values(0,'%s','%s','0');" % (a[0], a[1])
                db_insert_update_del(cursor, sql)
            ping_ips[a[0]]=a[1]
    time.sleep(ping_interval)
db.close()