import os
from collections import OrderedDict

import chardet


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def counter_files_lines(files):
    lines_counter = OrderedDict()
    for file in files:
        encoding = get_encoding(file)
        for line in open(file, encoding=encoding):
            line = line.strip()
            if line in lines_counter:
                lines_counter[line] += 1
            else:
                lines_counter[line] = 1
    return lines_counter


def get_folder_files(folder):
    files = []
    for file in os.listdir(folder):
        if file[0] == "_":
            continue
        files.append(file)
    return files


def get_input_folder():
    print("请输入目录：")
    folder = input()
    if folder[-1] != "/":
        folder += "/"
    return folder


def find_intersection():
    folder = get_input_folder()
    files = get_folder_files(folder)
    lines_counter = counter_files_lines(files)

    with open(folder + "_RESULT.txt", encoding="UTF-8", mode="w") as r:
        for k, v in lines_counter.items():
            if v < len(files):
                continue
            r.write(k + "\n")
    print("done")


def find_diffset():
    folder = get_input_folder()
    files = get_folder_files(folder)
    lines_counter = counter_files_lines(files)

    with open(folder + "_RESULT.txt", encoding="UTF-8", mode="w") as r:
        for k, v in lines_counter.items():
            if v > 1:
                continue
            r.write(k + "\n")
    print("done")


def find_unionset():
    folder = get_input_folder()
    files = get_folder_files(folder)
    lines_counter = counter_files_lines(files)

    with open(folder + "_RESULT.txt", encoding="UTF-8", mode="w") as r:
        for k, v in lines_counter.items():
            r.write(k + "\n")
    print("done")


if __name__ == "__main__":
    print("请输入数字：1.取文件的交集；2.取文件的差集; 3.取文件的并集")
    action = input()
    if action == "1":
        find_intersection()
    elif action == "2":
        find_diffset()
    elif action == "3":
        find_unionset()
    else:
        print("请输入正确的数字")

    print("按任意键退出...")
    input()
