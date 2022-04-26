#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
# import pandas as pd
# import numpy as np
from itertools import combinations

##################################################
#################### SETUP #######################
##################################################
# file = "./portefeuille.csv"
file = './dataset2_Python+P7.csv'
max = 500

##################################################
#################### FUNCTIONS ###################
##################################################


def import_csv(file):
    p_dict = dict()
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            price = abs(float(row['price']))
            profit = abs(float(row['profit']))
            roi = round(abs(float(row['price']) *
                        float(row['profit']) / 100), 2)
            if price != 0 and profit != 0 and roi != 0:
                p_dict[row['name']] = [price, profit, roi]
    return p_dict


def get_comb(p_dict):
    sorted_p_dict = sorted(p_dict.items(), key=lambda x: (-x[1][1]))
    # print(sorted_p_dict)
    best_comb = list()
    total = 0
    roi = 0
    index = 0
    maxi = True
    for action in sorted_p_dict:
        if total + action[1][0] <= max:
            # print(total)
            total += action[1][0]
            total = round(total, 2)
            roi += action[1][2]
            roi = round(roi, 2)
            best_comb.append(action)
            # print(action)
    for action in best_comb:
        print(action)
    print(total)
    print(roi)

    return best_comb


##################################################
#################### MAIN FUNCTION ###############
##################################################


def main():
    p_dict = import_csv(file)
    comb_list = get_comb(p_dict)
    # print(comb_list)
    # best_comb = sorted(comb_list, key=lambda x: (-x[2], -x[1]))[0]
    # print(best_comb)


if __name__ == '__main__':
    main()
