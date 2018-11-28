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


def get_huffman(sorted_prob_list):

    resortted_prob_list = sorted(sorted_prob_list,reverse=False)
    for prob in resortted_prob_list:

        # Tree-Node Type
        class Node:
            def __init__(self, freq):
                self.left = None
                self.right = None
                self.father = None
                self.freq = freq

            def isLeft(self):
                return self.father.left == self

        # create nodes创建叶子节点
        def createNodes(freqs):
            return [Node(freq) for freq in freqs]

        # create Huffman-Tree创建Huffman树
        def createHuffmanTree(nodes):
            queue = nodes[:]
            while len(queue) > 1:
                queue.sort(key=lambda item: item.freq)
                node_left = queue.pop(0)
                node_right = queue.pop(0)
                node_father = Node(node_left.freq + node_right.freq)
                node_father.left = node_left
                node_father.right = node_right
                node_left.father = node_father
                node_right.father = node_father
                queue.append(node_father)
            queue[0].father = None
            return queue[0]

        # Huffman编码
        def huffmanEncoding(nodes, root):
            codes = [''] * len(nodes)
            for i in range(len(nodes)):
                node_tmp = nodes[i]
                while node_tmp != root:
                    if node_tmp.isLeft():
                        codes[i] = '0' + codes[i]
                    else:
                        codes[i] = '1' + codes[i]
                    node_tmp = node_tmp.father


#Tree-Node Type
class Node:
    def __init__(self,freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq
    def isLeft(self):
        return self.father.left == self
#create nodes创建叶子节点
def createNodes(freqs):
    return [Node(freq) for freq in freqs]

#create Huffman-Tree创建Huffman树
def createHuffmanTree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item:item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_father = Node(node_left.freq + node_right.freq)
        node_father.left = node_left
        node_father.right = node_right
        node_left.father = node_father
        node_right.father = node_father
        queue.append(node_father)
    queue[0].father = None
    return queue[0]
#Huffman编码
def huffmanEncoding(nodes,root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.father
    return codes


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
    return sum(list_p_k)


def get_code_efficiency(entropy, mean_k):
    effficiency = entropy / mean_k
    return effficiency


def main_huffman():
    file_path = "./GameOfThrones.txt"
    letter_num, space_num = count_num(file_path)
    file_txt = get_txt(file_path)
    letter_list, letter_dict = num_dict(file_txt)
    prob_list, sorted_letter_list, sorted_prob_list, sorted_k_list, sorted_prob_dict, sorted_k_dict = get_sort_prob_k_list_dict(
        letter_dict)
    sorted_letter_dict = k_dict = sorted(letter_dict.items(), key=operator.itemgetter(1), reverse=True)

    entropy = get_entropy(sorted_prob_list)

    chars_freqs = sorted_letter_dict
    nodes = createNodes([item[1] for item in chars_freqs])
    root = createHuffmanTree(nodes)
    codes = huffmanEncoding(nodes, root)
    print("******Huffman encoding******")
    k_list = []
    for item in zip(chars_freqs, codes):
        print('%-10s%-20s' % (item[0][0], item[1]))
        k_list.append(len(item[1]))

    mean_k = get_mean_K(sorted_prob_list,k_list)
    var = get_var(sorted_prob_list,k_list,mean_k)
    effficiency = get_code_efficiency(entropy,mean_k)
    print('%-10s%-20s' % ("信源熵 : ", entropy))
    print('%-10s%-20s' % ("平均码字长度 : ", mean_k))
    print('%-10s%-20s' % ("码字长度的方差 : ", var))
    print('%-10s%-20s' % ("编码效率 : ", effficiency))

if __name__ == '__main__':
    main_huffman()