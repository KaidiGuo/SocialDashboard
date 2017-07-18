#coding=utf-8
import os
import time
import re
import json
from collections import Counter


def turn_tags_tostring(sql_result):
    outputstring = ""
    for row in sql_result:
        longlist = row[0].split(" ")
        for i in range(len(longlist)-1):
            outputstring = outputstring + longlist[i+1] +","
    return outputstring

def linear_scale(inputmin,inputmax,outputmin,outputmax,item):
    a = (outputmax-outputmin)/(inputmax-inputmin)
    b = outputmax - a*inputmax
    output = a*item +b
    return output

def wordscounter(text, n):
    wordDict = {}
    wordlist =text.split(",")
    for word in wordlist:
        if word in wordDict:
            wordDict[word] = wordDict[word] + 1
        else:
            wordDict[word] = 1

    removelist = ["秒拍", "视频", "网页", "分享","全文","链接","00","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","21","22","23","24","26","27","28","100","25","20","30","40","50","60","70","80"]
    for word in removelist:
        try:
            del wordDict[word]
        except Exception:
            pass

    count = Counter(wordDict)
    rank = count.most_common()[:n]
    countmax = rank[1][1]
    countmin = rank[-1][1]
    diclist = []
    for item in rank :
        rankdic = {}
        rankdic['text'] = item[0]
        rankdic['size'] = linear_scale(countmin,countmax,10,110,item[1])
        diclist.append(rankdic)

    diclist[0]['size'] = 120
    return diclist


    # print json.dumps(count.most_common()[:n], encoding="UTF-8", ensure_ascii=False)
    # print rank
    # print json.dumps(diclist, encoding="UTF-8", ensure_ascii=False)