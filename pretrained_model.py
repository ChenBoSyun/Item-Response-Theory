
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats import truncnorm
import math
import scipy as sp
import database


# In[2]:


class Model():
    def __init__(self):
        """initialize the model's parameter and load training data from database
        trainging data : the users answered result. 0 means error , 1 means correct , like:[0,0,1,0,1,0]
        user_ability : the value between -4~4 , the higher the better

        """
        db = database.Database() 
        self.__user_item_matrix = np.asarray(db.user_item_matrix()) #get training data
        n_user , n_item = self.__user_item_matrix.shape 
        self.__user_ability = truncnorm.rvs( a=-4 , b=4 ,loc=0 ,scale=2 , size=n_user) 
        self.__item_parameter = [{'a': truncnorm.rvs(0, 2), 'b': truncnorm.rvs(-4, 4), 'c': truncnorm.rvs(0, 1)} for i in range(n_item)]
        
        self.__a_lb = 0
        self.__a_ub = 2

        self.__b_lb = -4
        self.__b_ub = 4

        self.__c_lb = 0
        self.__c_ub = 1

        self.__theta_lb = -4
        self.__theta_ub = 4
    
    def Equation_3PL(self , a , b , c , theta):
        p = c + (1.0 - c) * (1.0 / (1.0 + math.exp(-1.7*a*(theta-b)) )) 
        return p 
    
    def prob_user_response(self , response , theta):
        norm = sp.stats.norm(0, 1)
        p = 1
        for r , item in zip(response , self.__item_parameter):
            if r == 1:
                p = p * self.Equation_3PL(item['a'] , item['b'] , item['c'] , theta)
            elif r == 0:
                p = p * (1 - self.Equation_3PL(item['a'] , item['b'] , item['c'] , theta))
        return p
    
    def prob_item_response(self , s_type , response , a , b , c):
        norm = sp.stats.norm(0, 1)
        p = 1
        '''
        if s_type == 'a':
            p = norm.pdf(a)
        elif s_type == 'b':
            p = norm.pdf(b)
        elif s_type == 'c':
            p = norm.pdf(c)
        '''
        for r , abi in zip(response , self.__user_ability):
            if r == 1:
                p = p * self.Equation_3PL(a , b , c , abi)
            else:
                p = p * (1 - self.Equation_3PL(a , b , c , abi))
        return p
    
    def grid_search(self , s_type ,  response , index=None  , init_size=7 ):
        max_prob = 0

        if s_type == 'a':
            lb = self.__a_lb
            ub = self.__a_ub
            search_list = np.linspace(lb, ub, init_size)
            b = self.__item_parameter[index]['b']
            c = self.__item_parameter[index]['c']
            for a in search_list:
                temp_prob = self.prob_item_response(s_type , response , a , b , c )
                if temp_prob > max_prob:
                    max_prob = temp_prob
                    max_a = a
            return max_a

        elif s_type == 'b':
            lb = self.__b_lb
            ub = self.__b_ub
            search_list = np.linspace(lb, ub, init_size)
            a = self.__item_parameter[index]['a']
            c = self.__item_parameter[index]['c']
            for b in search_list:
                temp_prob = self.prob_item_response(s_type , response , a , b , c )
                if temp_prob > max_prob:
                    max_prob = temp_prob
                    max_b = b
            return max_b

        elif s_type == 'c':
            lb = self.__c_lb
            ub = self.__c_ub
            search_list = np.linspace(lb, ub, init_size)
            a = self.__item_parameter[index]['a']
            b = self.__item_parameter[index]['b']
            for c in search_list:
                temp_prob = self.prob_item_response(s_type , response , a , b , c )
                if temp_prob > max_prob:
                    max_prob = temp_prob
                    max_c = c
            return max_c 

        elif s_type == 'theta':
            lb = self.__theta_lb
            ub = self.__theta_ub
            search_list = np.linspace(lb, ub, init_size)
            for theta in search_list:
                temp_prob = self.prob_user_response(response , theta )
                if temp_prob > max_prob:
                    max_prob = temp_prob
                    max_theta = theta
            return max_theta , max_prob

        else:
            raise typeerror('type error')
    def train(self , epochs = 20 , init_size = 7):
        for i in range(epochs):
            tmp = 0.0
            for index,user in enumerate(self.__user_item_matrix):
                self.__user_ability[index] , prob = self.grid_search(s_type='theta' , response=user , init_size=init_size)
                tmp += math.log(prob)
            print("%d epoch - probabilty:%.4f"%((i+1),tmp))
            
            for index,item in enumerate(self.__user_item_matrix.transpose()):
                new_a = self.grid_search(s_type='a' ,  response=item , index=index  , init_size=init_size )
                new_b = self.grid_search(s_type='b' ,  response=item , index=index  , init_size=init_size )
                new_c = self.grid_search(s_type='c' ,  response=item , index=index  , init_size=init_size )
                self.__item_parameter[index]['a'] = new_a
                self.__item_parameter[index]['b'] = new_b
                self.__item_parameter[index]['c'] = new_c
    def save(self):
        import pickle
        with open('Weights.pickle', 'wb') as file:
            pickle.dump(self.__item_parameter, file, protocol=pickle.HIGHEST_PROTOCOL)
        print("save model weights completed")
    
    def check(self):
        import pandas as pd
        df = pd.DataFrame(self.__item_parameter)
        print (df)

