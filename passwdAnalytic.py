"""
    统计内容：
    Has Done:
    数字出现频次表：0-9排序
    字符出现频次表: a-z排序，区分大小写
    符号出现频次表：统计常见的吧，给个TOP10差不多了?
    L(字符)D(数字)S(符号)组合：例如Clearlove7为L9D1，统计最常见的TOP10-50
    纯数字/纯字母/纯符号类型：
    数据可视化？
    What's more？
"""
from load import loadData
import numpy as np
import pandas as pd
from pandas import DataFrame
import xlwt
import openpyxl

# 字符字典生成
def wordCount(passwd, wCount):
    for pwd in passwd:
        # print(pwd)
        for i in pwd:
            if i in wCount:
                wCount[i] = wCount[i] + pwd.count(i)
            else:
                wCount[i] = pwd.count(i)

    # 存个文件
    f = open('data/wordsInPassword.txt', 'w', encoding="utf-8")
    for key in wCount:
        f.write(key + ':' + str(wCount[key]) + '\n')
    f.close()


# 统计数字特征
def numberFeatures(wordsInPassword):

    numTotal = 0
    numCount = []
    i = 0
    while i < 10:
        numTotal += wordsInPassword[str(i)]
        numCount.append(wordsInPassword[str(i)])
        i += 1

    numRank = np.array(numCount).argsort()[::-1]
    # print(numRank)

    # 存个文件
    f = open('data/numberRank.txt', 'w', encoding="utf-8")
    f.write("The number of times the number appears: " + str(numTotal) + '\n')
    for num in numRank:
        f.write("Number " + str(num) + ' :\t' + str(numCount[num]) + ' times\t' +
                str(numCount[num]/numTotal*100) + '%\n')
    f.close()


# 统计字母特征 w:words 总体字母; u:uppercase 大写字母; l:lowercase 小写字母
def letterFeatures(wordsInPassword):

    uTotal = 0
    lTotal = 0

    wCount = []
    uCount = []
    lCount = []

    i = 0
    while i < 26:
        uTotal += wordsInPassword[str(chr(ord('A') + i))]
        lTotal += wordsInPassword[str(chr(ord('a') + i))]

        uCount.append(wordsInPassword[str(chr(ord('A') + i))])
        lCount.append(wordsInPassword[str(chr(ord('a') + i))])
        wCount.append(wordsInPassword[str(chr(ord('a') + i))] + wordsInPassword[str(chr(ord('A') + i))])
        i += 1
    wTotal = uTotal + lTotal

    wRank = np.array(wCount).argsort()[::-1]
    uRank = np.array(uCount).argsort()[::-1]
    lRank = np.array(lCount).argsort()[::-1]
    # print(uRank)

    # 存个文件
    f = open('data/letterRank.txt', 'w', encoding="utf-8")
    f.write("The number of times the letters appear:\tUppercase: " + str(uTotal) +
            "\tLowercase: " + str(lTotal) + "\tTotal: " + str(wTotal) + '\n')

    f.write("For uppercase letters:\n")
    for u in uRank:
        f.write(str(chr(u + ord('A'))) + ' :\t' + str(uCount[u]) + ' times\t' +
                str(uCount[u]/uTotal*100) + '%\n')
    f.write("For lowercase letters:\n")
    for l in lRank:
        f.write(str(chr(l + ord('a'))) + ' :\t' + str(lCount[l]) + ' times\t' +
                str(lCount[l] / lTotal * 100) + '%\n')
    f.write("For all letters:\n")
    for w in wRank:
        f.write(str(chr(w + ord('A'))) + ' :\t' + str(wCount[w]) + ' times\t' +
                str(wCount[w] / wTotal * 100) + '%\n')
    f.close()


# 统计符号特征
def symbolFeatures(wordsInPassword):
    sTotal = 0
    sDict = {}

    for key in wordsInPassword:
        # 数字或字母
        # if ord(chr(key)) in range(48, 58) or ord(chr(key)) in range(65, 91) or ord(chr(key)) in range(97, 123):
        if ord(key) in range(48, 58) or ord(key) in range(65, 91) or ord(key) in range(97, 123):
            continue
        else:
            sTotal += wordsInPassword[key]
            sDict[key] = wordsInPassword[key]

    sOrder = sorted(sDict.items(), key=lambda x: x[1], reverse=True)
    # print(sOrder)
    f = open('data/symbolRank.txt', 'w', encoding="utf-8")
    f.write(str(len(sDict)) + " kinds of symbol appear " + str(sTotal) + " times\n")
    for s in sOrder:
        f.write("Symbol:\t \"" + s[0] + "\"\t" + str(s[1]) + " times\t" + str(s[1]/sTotal*100) + "%\n")
    f.close()

# 密码结构分析，例如Clearlove7为L9D1  &&  分析纯数字，纯字母，纯符号的比例
def passwords_structure_analyse(passwd):
    len_of_password = []
    num_of_types = []
    num_of_letters = []
    num_of_digits = []
    num_of_others = []
    structure = []
    all_litters = []
    all_digits = []
    all_others = []

    for password in passwd:
        password = str(password)
        len_of_password.append(len(password))
        digit, letter, other, typep = 0, 0, 0, 0  # 分别统计数字、字母、其他字符个数和字符类型数量
        flag1, flag2 = 0, 0  # flag1, flag2用于判断字符类型是否发生变化，比如从字母变成了数字等
        s = ''
        num = -1
        g = 0
        for i in password:
            if i.isalpha():
                letter = letter + 1
                flag1 = 1
            elif i.isdigit():
                digit = digit + 1
                flag1 = 2
            else:
                other = other + 1
                flag1 = 3
            num += 1
            if flag2 != flag1:
                # 如果s为空，也就是第一个类型，前面不用加'-'
                # if len(s) != 0:
                #     s = s + '-'
                if flag2 != 0:
                    if flag2 == 1:
                        s = s + 'L' + str(num)
                    elif flag2 == 2:
                        s = s + 'D' + str(num)
                    else:
                        s = s + 'O' + str(num)
                    num = 0
            flag2 = flag1
            if g == len(password) - 1:
                if flag1 == 1:
                    s = s + 'L' + str(num + 1)
                elif flag1 == 2:
                    s = s + 'D' + str(num + 1)
                else:
                    s = s + 'O' + str(num + 1)
            g += 1

        num_of_letters.append(letter)
        num_of_digits.append(digit)
        num_of_others.append(other)

        if letter != 0:
            typep = typep + 1
        if digit != 0:
            typep = typep + 1
        if other != 0:
            typep = typep + 1

        if letter == 0 and digit == 0:
            all_others.append(password)
        if digit == 0 and other == 0:
            all_litters.append(password)
        if letter == 0 and other == 0:
            all_digits.append(password)

        num_of_types.append(typep)

        structure.append(s)

    # print("数据处理完成")

    # 拼接之前检查口令数量和各列表长度是否相等
    # print("每个列表长度如下：")
    # print(len(passwd), len(len_of_password), len(num_of_types), len(num_of_letters), len(num_of_digits),
    #       len(num_of_others), len(structure))

    passwd1 = pd.Series(passwd)
    len_of_password = pd.Series(len_of_password)
    num_of_types = pd.Series(num_of_types)
    num_of_letters = pd.Series(num_of_letters)
    num_of_digits = pd.Series(num_of_digits)
    num_of_others = pd.Series(num_of_others)
    structure = pd.Series(structure)

    # 拼接+写入文件
    analysis_of_elements_and_structure = pd.concat(
        [passwd1, len_of_password, num_of_types, num_of_letters, num_of_digits, num_of_others, structure], axis=1)
    analysis_of_elements_and_structure.columns = ['password', 'len_of_password', 'num_of_types', 'num_of_letters',
                                                  'num_of_digits', 'num_of_others', 'structure']
    df = pd.DataFrame(analysis_of_elements_and_structure)
    df2 = df.head(10000)  # max_row = 1048576
    df2.to_excel('data/passwords_analyse.xlsx', index=False)

    # print("拼接完成")

    # analysis_of_elements_and_structure.to_csv('data/analysis_of_elements_and_structure.csv', index=False)
    # print("写入文件完成")
    # print(analysis_of_elements_and_structure)

    structure = analysis_of_elements_and_structure['structure']
    dic_of_structure = {}
    for i in structure:
        if i not in dic_of_structure.keys():
            dic_of_structure[i] = 1
        else:
            dic_of_structure[i] = dic_of_structure[i] + 1
    sorted_dic_of_structure = sorted(dic_of_structure.items(), key=lambda x: x[1], reverse=True)

    # print("所有口令的结构共有{}种".format(len(sorted_dic_of_structure)))
    # print("排名前100的结构为：")
    # for i in range(100):
    #     print(sorted_dic_of_structure[i])

    keys = []
    values = []
    percent = []

    for i in sorted_dic_of_structure:
        keys.append(i[0])
        values.append(i[1])
        percent.append(str(i[1] / len(structure) * 100) + '%')

    keys = pd.Series(keys)
    values = pd.Series(values)
    percent = pd.Series(percent)
    structure_statistics = pd.concat([keys, values, percent], axis=1)
    structure_statistics.columns = ['structure', 'frequency', 'percent']
    df3 = pd.DataFrame(structure_statistics)
    df3.to_excel('data/passwords_structure_analyse.xlsx', index=False)
    # structure_statistics.to_csv('/data/structure_statistics.csv', index=False)

    # 分析纯数字，纯字母，纯符号的比例
    all_litters_percent = len(all_litters) / len(passwd) * 100
    all_digits_percent = len(all_digits) / len(passwd) * 100
    all_others_percent = len(all_others) / len(passwd) * 100
    s1 = str(all_digits_percent) + '%'
    s2 = str(all_litters_percent) + '%'
    s3 = str(all_others_percent) + '%'
    all_litters.insert(0, s2)
    all_digits.insert(0, s1)
    all_others.insert(0, s3)
    all_litters = pd.Series(all_litters)
    all_digits = pd.Series(all_digits)
    all_others = pd.Series(all_others)
    all_statistics = pd.concat([all_digits, all_litters, all_others], axis=1)
    all_statistics.columns = ['all_digits', 'all_litters', 'all_others']
    df4 = pd.DataFrame(all_statistics)
    df5 = df4.head(10000)
    df5.to_excel('data/all_statistics.xlsx', index=False)
    # all_statistics.to_csv('/data/all_statistics.csv', index=False)


if __name__ == "__main__":
    name = []
    passwd = []
    email = []
    wordsInPassword = {}  # 单个字符统计

    loadData(name, passwd, email)  # 加载数据
    num = len(passwd)
    print(num, "passwords have been loaded\nStart analysing")
    # print(passwd)

    wordCount(passwd, wordsInPassword)
    # print(wordsInPassword)

    numberFeatures(wordsInPassword)
    letterFeatures(wordsInPassword)
    symbolFeatures(wordsInPassword)
    passwords_structure_analyse(passwd)
