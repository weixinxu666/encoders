# coding:utf-8
from shannon import main_shannon
from huffman import main_huffman

file_path = "./GameOfThrones.txt"

def chooseUI(choice):
    if choice == "1":
        main_shannon()
    elif choice == "2":
        main_huffman()
    elif choice == "3":
        exit()

def main():
    while True:
        choice = input("请选择您想使用的编码（输入一个数字）：1--香农编码   2--哈夫曼编码   3--退出软件\n")
        chooseUI(choice)

if __name__ == '__main__':
    main()
