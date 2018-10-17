#!/usr/bin/env python
# coding: utf-8

import pretrained_model
from argparse import ArgumentParser
import database

__author__ = "Bo-Syun Cheng"
__email__ = "k12s35h813g@gmail.com"

parser = ArgumentParser()

if __name__ == '__main__':
    #parse argument
    parser = ArgumentParser()
    parser.add_argument("-e" , "--epoch" , help="number of training step" , default=10 , dest="epochs")
    parser.add_argument("-i" , "--init_size" , help="number of cut when grip search" , default=100 , dest="init_size")
    args = parser.parse_args()
    epochs = int(args.epochs)
    init_size = int(args.init_size)
    ###############################################################################################################
    db = database.Database()
    user_item_matrix = db.user_item_matrix()

    model = pretrained_model.Model(user_item_matrix)
    model.train(epochs = epochs , init_size = init_size)
    model.save()
    model.check()
