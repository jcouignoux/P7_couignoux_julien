#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from argparse import ArgumentParser
import time
import tracemalloc
# import numpy as np
import matplotlib.pyplot as plt
# from statsmodels.nonparametric.kernel_regression import KernelReg


##################################################
#################### SETUP #######################
##################################################
file = "./portefeuille.csv"
# file = './dataset1_Python+P7.csv'
# file = './dataset2_Python+P7.csv'
max = 500

parser = ArgumentParser()
parser.add_argument('-a', '--analyse', action='store_true',
                    help='an integer for the accumulator')
args = parser.parse_args()

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
    best_comb = list()
    total = 0
    roi = 0
    for action in sorted_p_dict:
        if total + action[1][0] <= max:
            total += action[1][0]
            total = round(total, 2)
            roi += action[1][2]
            roi = round(roi, 2)
            best_comb.append(action[0])

    return (tuple(best_comb), total, roi)


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def display_graph(list, y_label, title_label):
    print(list)
    x = range(1, len(list) + 1)
    y = list
    # kr = KernelReg(y, x, 'c')
    plt.plot(x, y)
    # plt.plot(x, smooth(y, 3))
    # plt.plot(x, smooth(y, 19))
    plt.xlabel('x - Nb of Actions')
    plt.ylabel('y - ' + y_label)
    plt.title('optimized ' + title_label + '\n' +
              file.split('_')[0].split('/')[-1])
    # plt.ylim(sorted(list)[0], sorted(list)[-1])
    # plt.xlim(0, len(list))
    plt.show()


##################################################
#################### MAIN FUNCTION ###############
##################################################


def main():
    p_dict = import_csv(file)
    if args.analyse:
        time_list = list()
        mem_list = list()
        for i in range(1, len(p_dict) + 1):
            p_dict_list = list(p_dict.keys())[0:i]
            p_dict_test = dict()
            for action in p_dict_list:
                p_dict_test[action] = p_dict[action]
            start = time.time()
            best_comb = get_comb(p_dict_test)
            # print(best_comb)
            end = time.time()
            elapsed = end - start
            # print(f'Temps d\'exécution : {elapsed:.6} s')
            time_list.append(elapsed)
            tracemalloc.start()
            best_comb = get_comb(p_dict)
            # print(tracemalloc.get_traced_memory())
            traced_mem = tracemalloc.get_traced_memory()
            used_mem = traced_mem[1] - traced_mem[0]
            mem_list.append(used_mem)
            tracemalloc.stop()
        display_graph(time_list, 'Execution time', 'Time Analyse')
        display_graph(mem_list, 'Used Memory', 'Memory Analyse')
    else:
        start = time.time()
        best_comb = get_comb(p_dict)
        print(best_comb)
        end = time.time()
        elapsed = end - start
        print(f'Temps d\'exécution : {elapsed:.2} s')
        # best_comb = sorted(comb_list, key=lambda x: (-x[2], -x[1]))[0]
        # print(best_comb)


if __name__ == '__main__':
    main()
