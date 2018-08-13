
# coding: utf-8

# In[10]:


import pretrained_model
from argparse import ArgumentParser


# In[11]:


parser = ArgumentParser()


# In[13]:


if __name__ == '__main__':

    #parse argument
    parser = ArgumentParser()
    parser.add_argument("-e" , "--epoch" , help="number of training step" , default=20 , dest="epochs")
    parser.add_argument("-i" , "--init_size" , help="number of cut when grip search" , default=7 , dest="init_size")
    args = parser.parse_args()
    epochs = int(args.epochs)
    init_size = int(args.init_size)
    ###############################################################################################################
    model = pretrained_model.Model()
    model.train(epochs = epochs , init_size = init_size)
    model.save()
    model.check()
    

