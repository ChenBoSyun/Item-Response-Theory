
# coding: utf-8

# In[ ]:


import pymysql
class Database():
    def __init__(self):
        # 打开数据库连接
        self.__db = pymysql.connect("127.0.0.1","root","","adaptive_testing_db",charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.__cursor = self.__db.cursor()
        
        #初始化答案list
        self.__answer = []
        
        #初始化使用者答題結果
        self.__user_item_matrix = []
        
        ''''''
        #從資料庫取得answer
        try:
            self.__cursor.execute('SELECT answer FROM problem WHERE 1')
            self.__db.commit()
            result = self.__cursor.fetchall()
            for row in result:
                self.__answer.append(row[0])
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
        ''''''
        
        ''''''
        #從資料庫取得使用者答題結果
        try:
            self.__cursor.execute('SELECT * FROM user_data WHERE 1')
            self.__db.commit()
            result = self.__cursor.fetchall()
            for row in result:
                u = [1 if (self.__answer[i] == row[i+2]) else 0 for i in range(len(self.__answer))]
                self.__user_item_matrix.append(u)
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
        
        ''''''
    
    #get答案
    def answer(self):
        return self.__answer
    
    def user_item_matrix(self):
        return self.__user_item_matrix

