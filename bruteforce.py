#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from itertools import combinations
from argparse import ArgumentParser
import time
import tracemalloc
import matplotlib.pyplot as plt


##################################################
#################### SETUP #######################
##################################################
file = "./portefeuille.csv"
# file = '../dataset1_Python+P7.csv'
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


def display_graph(list, y_label, title_label):
    print(list)
    x = range(1, len(list) + 1)
    y = list
    plt.plot(x, y)
    plt.xlabel('x - Nb of Actions')
    plt.ylabel('y - ' + y_label)
    plt.title('bruteforce ' + title_label)
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
            comb_list = get_comb(p_dict_test)
            best_comb = sorted(comb_list, key=lambda x: (-x[2], -x[1]))[0]
            print(best_comb)
            end = time.time()
            elapsed = end - start
            print(f'Temps d\'exécution : {elapsed:.2} s')
            time_list.append(elapsed)
            tracemalloc.start()
            comb_list = get_comb(p_dict_test)
            print(tracemalloc.get_traced_memory())
            traced_mem = tracemalloc.get_traced_memory()
            used_mem = traced_mem[1] - traced_mem[0]
            mem_list.append(used_mem)
            tracemalloc.stop()
        display_graph(time_list, 'Execution time', 'Time Analyse')
        display_graph(mem_list, 'Used Memory', 'Memory Analyse')
    else:
        start = time.time()
        comb_list = get_comb(p_dict)
        best_comb = sorted(comb_list, key=lambda x: (-x[2], -x[1]))[0]
        print(best_comb)
        end = time.time()
        elapsed = end - start
        print(f'Temps d\'exécution : {elapsed:.2} s')


if __name__ == '__main__':
    main()
