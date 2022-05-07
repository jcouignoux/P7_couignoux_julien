#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from argparse import ArgumentParser
from re import M
import time
import tracemalloc
import matplotlib.pyplot as plt


##################################################
#################### SETUP #######################
##################################################
# file = "./portefeuille.csv"
# file = './dataset1_Python+P7.csv'
file = './dataset2_Python+P7.csv'
maxi = 500

parser = ArgumentParser()
parser.add_argument('-a', '--analyse', action='store_true',
                    help='an integer for the accumulator')
args = parser.parse_args()


##################################################
#################### FUNCTIONS ###################
##################################################


def import_csv(file):
    p_list = list()
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            name = row['name']
            price = abs(float(row['price']))
            profit = abs(float(row['profit']))
            roi = round(abs(float(row['price']) *
                        float(row['profit']) / 100), 2)
            if price != 0 and profit != 0 and roi != 0:
                p = (name, price, roi)
                p_list.append(p)

    return p_list


def get_comb(maxi, p_list):
    matrice = [[0 for x in range(maxi + 1)] for x in range(len(p_list) + 1)]

    for i in range(1, len(p_list) + 1):
        for w in range(1, maxi + 1):
            if p_list[i-1][1] <= w:
                index = int(w-p_list[i-1][1])
                matrice[i][w] = max(
                    p_list[i-1][2] + matrice[i-1][index], matrice[i-1][w])
            else:
                matrice[i][w] = matrice[i-1][w]

    w = maxi
    n = len(p_list)
    total = 0
    p_sel = []

    while w >= 0 and n >= 0:
        p = p_list[n - 1]
        index = int(w-p[1])
        if matrice[n][int(w)] == matrice[n-1][index] + p[2]:
            p_sel.append(p)
            total += p[1]
            w -= p[1]
        n -= 1

    return total, matrice[-1][-1], p_sel


def display_graph(list, y_label, title_label):
    print(list)
    x = range(1, len(list) + 1)
    y = list
    plt.plot(x, y)
    plt.xlabel('x - Nb of Actions')
    plt.ylabel('y - ' + y_label)
    plt.title('optimized ' + title_label + '\n' +
              file.split('_')[0].split('/')[-1])
    plt.show()

    ##################################################
    #################### MAIN FUNCTION ###############
    ##################################################


def main():
    p_list = import_csv(file)
    if args.analyse:
        time_list = list()
        mem_list = list()
        for i in range(1, len(p_list) + 1, int(len(p_list) / 20)):
            p_dict_list = p_list[0:i]
            start = time.time()
            best_comb = get_comb(maxi, p_dict_list)
            end = time.time()
            elapsed = end - start
            time_list.append(elapsed)
            tracemalloc.start()
            comb_list = get_comb(maxi, p_dict_list)
            traced_mem = tracemalloc.get_traced_memory()
            used_mem = traced_mem[1] - traced_mem[0]
            mem_list.append(used_mem)
            tracemalloc.stop()
        display_graph(time_list, 'Execution time', 'Time Analyse')
        display_graph(mem_list, 'Used Memory', 'Memory Analyse')
    else:
        start = time.time()
        comb_list = get_comb(maxi, p_list)
        end = time.time()
        print(f'Actions to buy:')
        for action in comb_list[2]:
            print(action[0])
        print(f'Total cost: {comb_list[0]}')
        print(f'Total return: {round(comb_list[1], 2)}')
        elapsed = end - start
        print(f'Execution time: {elapsed:.2} s')


if __name__ == '__main__':
    main()
