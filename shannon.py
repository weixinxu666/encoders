# coding:utf-8
import operator
import re
import math
import numpy as np

file_path = "./GameOfThrones.txt"

def num_dict(str):
    alist = []
    letter_list = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + ["space"]
    for i in range(26):  # 初始化一个长度为26的列表
        alist.append(0)
    str = str.lower()
    for i in str:
        if i.isalpha():  # 利用桶的思想
            alist[ord(i) - 97] += 1
    _, space_num = count_num(file_path)
    alist = alist + [space_num]
    letter_dict = dict(zip(letter_list, alist))
    # letter_list.insert(0, "space")
    return letter_list, letter_dict


def count_num(path):
    letter_num = 0
    space_num = 0
    with open(path, "r") as f:
        file = f.read()
        for i in file:
            if (ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90):
                letter_num = letter_num + 1
            elif ord(i) == 32:
                space_num = space_num + 1
    return letter_num, space_num


def get_txt(file_path):
    fp = open(file_path, 'r')
    file_text = fp.read()
    letter_str = re.findall(r'([a-zA-Z]+)', file_text, re.MULTILINE)
    fp.close()
    return ''.join(letter_str)


def get_sort_prob_k_list_dict(num_dict):
    letter_num, space_num = count_num(file_path)
    sum_num = letter_num + space_num
    list = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + ["space"]
    prob_list = []
    k_list = []
    sorted_letter_list = []
    sorted_prob_dict = {}
    sorted_k_dict = {}
    for letter in list:
        probability = num_dict[letter] / sum_num
        k = math.floor(1 - math.log(probability, 2))
        prob_list = prob_list + [probability]
        k_list = k_list + [k]
    sorted_prob_list = sorted(prob_list, reverse=True)
    sorted_k_list = sorted(k_list, reverse=False)
    prob_dict = dict(zip(list, prob_list))
    k_dict = dict(zip(list, k_list))
    # *******sorted之后还不是真正的字典**********
    prob_dict = sorted(prob_dict.items(), key=operator.itemgetter(1), reverse=True)
    k_dict = sorted(k_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_prob_dict.update(prob_dict)
    sorted_k_dict.update(k_dict)
    for key in sorted_prob_dict:
        sorted_letter_list.append(key)
    return prob_list, sorted_letter_list, sorted_prob_list, sorted_k_list, sorted_prob_dict, sorted_k_dict


def get_append_sorted_prob_list_dict(sorted_prob_dict):
    append_sorted_prob_list = []
    append_sorted_prob_dict = {}
    first_dict = {"zero": 0}
    append_sorted_prob_dict.update(first_dict)
    append_sorted_prob_dict.update(sorted_prob_dict)
    for key in append_sorted_prob_dict:
        append_sorted_prob_list.append(append_sorted_prob_dict[key])
    return append_sorted_prob_list, append_sorted_prob_dict


def get_sumProb_list(append_sorted_prob_list):
    sum_first = 0
    sumProb_list = []
    for i in range(0, 27):
        sum_first = sum_first + append_sorted_prob_list[i]
        sumProb_list.append(sum_first)
    return sumProb_list


def get_entropy(sorted_prob_list):
    entropy = 0
    for prob in sorted_prob_list:
        single_entropy = -prob * math.log(prob, 2)
        entropy = single_entropy + entropy
    return entropy


def get_mean_K(sorted_prob_list, sorted_k_list):
    list_p_k = np.multiply(np.array(sorted_prob_list), np.array(sorted_k_list))
    return sum(list_p_k)


def get_var(sorted_prob_list, sorted_k_list, mean_k):
    sorted_kk_list = sorted_k_list - mean_k
    sorted_k2_list = sorted_kk_list*sorted_kk_list
    list_p_k = np.multiply(np.array(sorted_prob_list), np.array(sorted_k2_list))
    # sqrt_list = []
    # for val in list_p_k:
    #     sqrt_list.append(val*val)
    return sorted_kk_list, sum(list_p_k)


def get_code_efficiency(entropy, mean_k):
    effficiency = entropy / mean_k
    return effficiency


def dec2bin_list_dict(letter_list, sumProb_list, sorted_k_list):
    sorted_bin_list = []
    sorted_bin_dict = {}
    global value
    i = 0
    for value in sumProb_list:
        s = ""
        for k in range(sorted_k_list[i]):
            value = value * 2
            if value >= 1:
                value = value - 1
                s = s + str(1)
            else:
                s = s + str(0)
        i = i + 1
        sorted_bin_list.append(s)
        sorted_bin_dict = dict(zip(letter_list, sorted_bin_list))
    return sorted_bin_list, sorted_bin_dict


def main_shannon():
    file_path = "./GameOfThrones.txt"
    letter_num, space_num = count_num(file_path)
    file_txt = get_txt(file_path)
    letter_list, letter_dict = num_dict(file_txt)
    prob_list, sorted_letter_list, sorted_prob_list, sorted_k_list, sorted_prob_dict, sorted_k_dict = get_sort_prob_k_list_dict(
        letter_dict)
    append_sorted_prob_list, append_sorted_prob_dict = get_append_sorted_prob_list_dict(sorted_prob_dict)
    sumProb_list = get_sumProb_list(append_sorted_prob_list)
    sorted_bin_list, sorted_bin_dict = dec2bin_list_dict(sorted_letter_list, sumProb_list, sorted_k_list)
    entropy = get_entropy(sorted_prob_list)
    mean_k = get_mean_K(sorted_prob_list, sorted_k_list)
    effficiency = get_code_efficiency(entropy, mean_k)
    sorted_kk_list, var = get_var(sorted_prob_list, sorted_k_list, mean_k)
    print("******Shannon encoding******")
    for key, values in sorted_bin_dict.items():
        print('%-10s%-20s' % (key, values))

    print('%-10s%-20s' % ("信源熵 : ", entropy))
    print('%-10s%-20s' % ("平均码字长度 : ", mean_k))
    print('%-10s%-20s' % ("码字长度的方差 : ", var))
    print('%-10s%-20s' % ("编码效率 : ", effficiency))

if __name__ == '__main__':
    main_shannon()