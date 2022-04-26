#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from itertools import combinations

##################################################
#################### SETUP #######################
##################################################
file = "./portefeuille.csv"
# file = '../dataset1_Python+P7.csv'
max = 500

##################################################
#################### FUNCTIONS ###################
##################################################


def import_csv(file):
    p_dict = dict()
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            p_dict[row['name']] = [float(row['price']), float(
                row['price']) * float(row['profit']) / 100]
    return p_dict


def get_comb(p_dict):
    comb_list = list()
    for i in range(1, len(p_dict) + 1):
        a = list(combinations(p_dict, i))
        for comb in a:
            costs = list()
            rois = list()
            [costs.append(p_dict[i][0]) for i in comb]
            total = sum(costs)
            if total <= max:
                [rois.append(p_dict[i][1]) for i in comb]
                roi = sum(rois)
                comb_total = (comb, total, roi)
                comb_list.append(comb_total)
    return comb_list


##################################################
#################### MAIN FUNCTION ###############
##################################################


def main():
    p_dict = import_csv(file)
    comb_list = get_comb(p_dict)
    best_comb = sorted(comb_list, key=lambda x: (-x[2], -x[1]))[0]
    print(best_comb)


if __name__ == '__main__':
    main()
