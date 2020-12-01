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
try:
    db = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        db=db_name
    )
except:
    print('mysql数据库连接失败.\n程序退出')
    exit()
cursor = db.cursor()
#初始化train_other_info
#cursor.execute('delete from train_other_info;')
cursor.execute('select device_id,service_ip,conf_ip from deviceinfo;')
id_lists = cursor.fetchall()
# ids = {}
# for train_id in id_lists:
#     ids[train_id[0]] = train_id[1]
#     #print(ids)
tun_ips={}
last_ping={}
sql = 'delete from simple_status'
db_insert_update_del(cursor, sql)
for message in id_lists:
    print(message)
    device_id=message[0]
    service_ip=message[1]
    conf_ip=message[2]
    service_ip=message[1].split('.')
    conf_ip=message[2].split('.')
    tun_ips[message[0]]='114.114.%s.114'%service_ip[2]#,service_ip[2])
    last_ping[message[0]]=0
    subnet_a="192.168.%s.1" %conf_ip[2]
    subnet_b="10.240.%s.1"%conf_ip[2]
    sql = "insert into simple_status values(0,'%s','%s','%s','0','%s','%s');" % (device_id,message[1],message[2],subnet_a,subnet_b)
    #print(sql)
    db_insert_update_del(cursor, sql)
    print(tun_ips)


while True:
    for device_id, tun_ip in tun_ips.items():
        ping_res = os.popen('ping -c 1 -w 1 %s' % tun_ip).read()
        ping = 0
        if '1 received' in ping_res:
            ping = 1
        if ping == 0:   # pingbutong
            if ping !=last_ping[device_id]:
                sql = "update simple_status set online_flag = 0 where device_id = '%s';" % device_id
                db_insert_update_del(cursor, sql)
                print(sql)
            # if ping != last_ping[train_id]:
            #     off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #     sql = "delete from train_connectivity where train_id='%s' and offline_time is null;" % train_id
            #     db_insert_update_del(cursor, sql)
            #     sql = "insert into train_connectivity(train_id, online_time, offline_time) values('%s', '%s', '%s');" % (train_id, online_time[train_id], off)
            #     db_insert_update_del(cursor, sql)
            # else:
            #     cursor = db.cursor()
            #     sql = "select * from train_connectivity where train_id='%s' and offline_time is null;" % train_id
            #     cursor.execute(sql)
            #     old_data = cursor.fetchall()
            #     if old_data:
            #         old_data1 = list(zip(*old_data))[2]
            #         online_time[train_id] = old_data1[0]
            #         off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #         sql = "delete from train_connectivity where train_id='%s' and offline_time is null;" % train_id
            #         db_insert_update_del(cursor, sql)
            #         sql = "insert into train_connectivity(train_id, online_time, offline_time) values('%s', '%s', '%s');" % (train_id, online_time[train_id], off)
            #         db_insert_update_del(cursor, sql)
        else:   # pingtong
            if ping !=last_ping[device_id]:
                sql = "update simple_status set online_flag = 1 where device_id = '%s';" % device_id
                db_insert_update_del(cursor, sql)
                print(sql)
            # if ping != last_ping[train_id]:
            #     cursor = db.cursor()
            #     sql = "select * from train_connectivity where train_id='%s' and offline_time is null;" % train_id
            #     cursor.execute(sql)
            #     old_data = cursor.fetchall()
            #     if old_data:
            #         old_data1 = list(zip(*old_data))[2]
            #         online_time[train_id] = old_data1[0]
            #     else:
            #         online_time[train_id] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #         sql = "insert into train_connectivity(train_id, online_time) values('%s', '%s');" % (train_id, online_time[train_id])
            #         db_insert_update_del(cursor, sql)
        last_ping[device_id] = ping
    time.sleep(ping_interval)
db.close()


# #两对参数，分别用于公共更新和单独车辆更新
# oldFileNames="1"
# train_oldFileNames="1"
# newFileNames={}
# train_newFileNames={}
# train_filerecord={}
#
# cursor.execute('SELECT pending_ver, count( * ) AS count FROM train_other_info GROUP BY pending_ver ORDER BY count DESC LIMIT 1')
# public_lists = cursor.fetchall()
# train_oldFileNames=public_lists[0][0]
#
# cursor.execute('select train_id, pending_ver from train_other_info;')
# file_lists = cursor.fetchall()
# #print(file_lists)
# for train_id in file_lists:
#     train_filerecord[train_id[0]] = train_id[1]
#
#
# while True:
#     print('start')
#     try:
#         db = pymysql.connect(
#             host=db_host,
#             port=db_port,
#             user=db_user,
#             password=db_password,
#             db=db_name
#         )
#     except:
#         print('mysql数据库连接失败，请确保 /home/chsr/cf.d/trainuser.conf中数据库用户名、密码正确。\n程序退出')
#         exit()
#     cursor = db.cursor()
#
#     # 发现public文件夹下的更新包，并获取其版本,更新表所有项的更新状态和待更新版本内容
#     cursor.execute('select train_id, pending_ver from train_other_info;')
#     id_lists = cursor.fetchall()
#     ids = {}
#     for train_id in id_lists:
#         ids[train_id[0]] = train_id[1]
#     # print(ids)
#
#     updatefile_path = '/home/chsr/data.d/ground-to-train.d/public'
#     try:
#         newFileNamesyuan = os.listdir(updatefile_path)
#         #print(newFileNamesyuan)
#         if ".zip" in newFileNamesyuan[0]:
#             for train_id, pending_ver in ids.items():
#                 newFileNames[train_id] = newFileNamesyuan[0].split('.zip')[0]
#             #print(newFileNames)
#         else:
#             print("更新包文件名不符合要求")
#     except:
#         pass
#     for train_id, pending_ver in ids.items():
#         if (newFileNames):
#             if(newFileNames[train_id]==train_filerecord[train_id]):
#                 pass
#             else:
#                 train_newFileNames[train_id]=newFileNames[train_id]
#             #sql = "update train_other_info set update_status = 1,pending_ver='%s';" % (newFileNames)
#             #db_insert_update_del(cursor, sql)
#             #print(newFileNames)
#         else:
#         #print("noupdatefile")
#             pass
#
#     # 所有车辆指定文件夹下是否有更新包，有的话就更新相应条目
#
#     for train_id,pending_ver in ids.items():
#         try:
#             train_updatefile_path = '/home/chsr/data.d/ground-to-train.d/%s'%train_id
#             try:
#                 train_newFileNamesyuan = os.listdir(train_updatefile_path)
#                 #print(train_newFileNamesyuan)
#                 if ".zip" in train_newFileNamesyuan[0]:
#                     train_newFileNames[train_id] = train_newFileNamesyuan[0].split('.zip')[0]
#             except:
#                 #print('%s nofile'%train_id)
#                 pass
#             if (len(train_newFileNames[train_id]) > 0):
#                 if(train_filerecord[train_id]):
#                     if (train_newFileNames[train_id] == train_filerecord[train_id]):
#                         #print("666666")
#                         pass
#                     else:
#                         sql = "update train_other_info set update_status = 1,pending_ver='%s' where train_id='%s';" % (train_newFileNames[train_id], train_id)
#                         db_insert_update_del(cursor, sql)
#                         train_filerecord[train_id] = train_newFileNames[train_id]
#                         #print(train_newFileNames)
#                 else:
#                     sql = "update train_other_info set update_status = 1,pending_ver='%s' where train_id='%s';" % (train_newFileNames[train_id], train_id)
#                     db_insert_update_del(cursor, sql)
#                     train_filerecord[train_id] = train_newFileNames[train_id]
#                     #print(train_newFileNames)
#             else:
#                 #print("train_noupdatefile")
#                 pass
#         except:
#             pass
#
#     # 找到所有处于更新状态的条目，查找相应文件夹是否有标志文件，并做相应操作
#     cursor.execute('select train_id, pending_ver from train_other_info where update_status=1;')
#     train_id_lists = cursor.fetchall()
#     if len(train_id_lists) == 0:
#         print('无车辆正在更新')
#     else:
#         train_ids = {}
#         for train_id in train_id_lists:
#             train_ids[train_id[0]] = train_id[1]
#         #print(train_ids)
#         for train_id, pending_ver in train_ids.items():
#             try:
#                 #fileList = os.listdir('/home/chsr/data.d/train-to-ground.d/%s/updateinfo/'%train_id)
#                 #print(fileList[0])
#                 file_name='%s+%s'%(train_id,pending_ver)
#                 file_path='/home/chsr/data.d/train-to-ground.d/%s/updateinfo/%s'%(train_id,file_name)
#                 #print(file_path)
#                 file_r = open(file_path,'r')
#                 status = file_r.readline(1)
#                 #print(status)
#                 file_r.close()
#                 if status=='1':
#                     print('ok')
#                     update_time = datetime.datetime.now().strftime('%Y-%m-%d')
#                     #print(update_time)
#                     sql = "update train_other_info set update_status = 0,update_time='%s',curr_ver='%s' where train_id = '%s';" % (update_time,pending_ver,train_id)
#                     db_insert_update_del(cursor, sql)
#                     try:
#                         os.system("rm %s -rf" % file_path)
#                     except OSError as e:
#                         print("Error:  %s : %s" % (file_path, e.strerror))
#                 elif status=='0':
#                     print('fail')
#                     sql = "update train_other_info set update_status = 9 where train_id = '%s';" %(train_id)
#                     db_insert_update_del(cursor, sql)
#                     try:
#                         os.system("rm %s -rf" % file_path)
#                     except OSError as e:
#                         print("Error:  %s : %s" % (file_path, e.strerror))
#                 else:
#                     print('wenjianyichang')
#                 #sql = "update train_other_info set online_flag = %s where train_id = '%s';" % (train_id,status)
#                 #db_insert_update_del(cursor, sql)
#                 #try:
#                     #os.system("rm %s -rf" % file_path)
#                 #except OSError as e:
#                     #print("Error:  %s : %s" % (file_path, e.strerror))
#             except:
#                 pass
#     time.sleep(ping_interval)
# db.close()
