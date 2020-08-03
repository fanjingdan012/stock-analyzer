# coding:utf-8
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
import datetime
start = datetime.datetime.now().strftime('%Y-%m-%d')
end = (datetime.datetime.now()+datetime.timedelta(days=100)).strftime('%Y-%m-%d')
# 新建pandas中的DataFrame, 只有id,num两列
df = pd.DataFrame(data=np.random.randint(-100,100,(100,100)),index=pd.date_range('2018-1-1',periods=100, freq='D'),columns=None,dtype=int)
print(df.shape)
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df.to_sql('data', engine, if_exists='append',index= True)

def write_sql(name,data=pd.DataFrame()):
    global engine
    data.to_sql(name,engine,if_exists='fail',index=True)