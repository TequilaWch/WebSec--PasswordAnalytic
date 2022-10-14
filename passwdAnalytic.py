"""
    统计内容：
    Has Done:
    数字出现频次表：0-9排序
    字符出现频次表: a-z排序，区分大小写
    符号出现频次表：统计常见的吧，给个TOP10差不多了?
    TODO:
    L(字符)D(数字)S(符号)组合：例如Clearlove7为L9D1，统计最常见的TOP10-50
    纯数字/纯字母/纯符号类型：
    数据可视化？
    What's more？
"""
from load import loadData
import numpy as np

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

    # numberFeatures(wordsInPassword)
    # letterFeatures(wordsInPassword)
    symbolFeatures(wordsInPassword)