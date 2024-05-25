#创建表
import pymysql
#创建连接
con=pymysql.connect(host='localhost',user='root',password='whuwhuwhu',database='test',port=3306)
#创建游标
cur=con.cursor()
##### 编写创建表的sql
 sql="""
 create table user(
     sequence int primary key auto_increment,
     userid varchar(36) not null,
     username varchar(20) not null,
     password varchar(32) not null,
     jurisdiction int DEFAULT '0'
     )
 """

# sql="""
# create table filepass(
#     userid int not null,
#     fileid varchar(20) not null,
#     in_template varchar(20) not null,
#     out_template varchar(20) not null,
#     format varchar(5) not null,
#     dir varchar(30) not null,
#     time varchar(20) not null
#     )
# """

# sql="""
# create table InTemplate(
#     in_template varchar(20) not null,
#     data_file varchar(20) not null,
#     clock_file varchar(20) not null,
#     box1 varchar(20) not null,
#     box2 varchar(20) null,
#     box3 varchar(20) null,
#     box4 varchar(20) null,
#     box5 varchar(20) null,
#     box6 varchar(20) null,
#     box7 varchar(20) null,
#     box8 varchar(20) null,
#     box9 varchar(20) null,
#     box10 varchar(20) null,
#     box11 varchar(20) null,
#     morphological varchar(20) not null,
#     space_relation varchar(20) not null,
#     gradient varchar(20) not null
#     )
# """

# sql="""
# create table OutTemplate(
#     out_template varchar(20) not null,
#     keyword1 varchar(20) not null,
#     keyword2 varchar(20) null,
#     keyword3 varchar(20) null,
#     keyword4 varchar(20) null,
#     keyword5 varchar(20) null,
#     keyword6 varchar(20) null,
#     keyword7 varchar(20) null,
#     keyword8 varchar(20) null,
#     keyword9 varchar(20) null,
#     keyword10 varchar(20) null,
#     keyword11 varchar(20) null
#     )
# """

# sql="""
# create table Identification(
#     userid int not null,
#     fileid varchar(20) not null,
#     in_template varchar(20) not null,
#     out_template varchar(20) not null,
#     data_file varchar(20) not null,
#     clock_file varchar(20) not null,
#     d_name_1 varchar(20) not null,
#     d_spf_1 varchar(20) not null,
#     d_unit_1 varchar(20) not null,
#     d_price_1 varchar(20) not null,
#     d_num_1 varchar(20) not null,
#     d_batch_1 varchar(20) not null,
#     d_name_2 varchar(20) null,
#     d_spf_2 varchar(20) null,
#     d_unit_2 varchar(20) null,
#     d_price_2 varchar(20) null,
#     d_num_2 varchar(20) null,
#     d_batch_2 varchar(20) null,
#     d_name_3 varchar(20) null,
#     d_spf_3 varchar(20) null,
#     d_unit_3 varchar(20) null,
#     d_price_3 varchar(20) null,
#     d_num_3 varchar(20) null,
#     d_batch_3 varchar(20) null,
#     d_name_4 varchar(20) null,
#     d_spf_4 varchar(20) null,
#     d_unit_4 varchar(20) null,
#     d_price_4 varchar(20) null,
#     d_num_4 varchar(20) null,
#     d_batch_4 varchar(20) null,
#     d_name_5 varchar(20) null,
#     d_spf_5 varchar(20) null,
#     d_unit_5 varchar(20) null,
#     d_price_5 varchar(20) null,
#     d_num_5 varchar(20) null,
#     d_batch_5 varchar(20) null
#     )
# """

#sql="""
#create table jsontest(
#    json varchar(200) not null
#    )
#"""


#int primary key auto_increment 自增长的不需要插入
try:
    #执行创建表的sql
    cur.execute(sql)
    print('创建成功')
except Exception as e:
    print(e)
    print('创建失败')
finally:
    #关闭连接
    con.close()
