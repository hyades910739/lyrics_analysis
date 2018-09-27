from collections import  Counter
import random
import itertools
import os
import re
import pandas as pd
import numpy as np
from numpy import NaN
import jieba
from sklearn.feature_extraction import DictVectorizer
from sklearn import neighbors, datasets
#jieba source : https://github.com/ldkrsi/jieba-zh_TW

def clean(documents={}):
    re_composer = re.compile("作曲：.{3}|編曲：.{3}|監製：.{3}|製作：.{3}|人：.{3}")
    re_quote = re.compile('\(.{0,3}\)')
    re_clean = re.compile("[^\w\s]|Repeat|repeat|[0-9]|-.*-")
    res = {title:clean_main(document,re_composer,re_quote,re_clean) for title,document in documents.items()}
    return res

def clean_main(doc,reg1,reg2,reg3):
    doc = reg1.split(doc)[-1]
    doc = reg2.sub(" ",doc)
    doc = reg3.sub(" ",doc)
    return doc  

#filter word count(column sums) less than n:
def wordcount_filter(df,n=1):
    sel = np.where(df.sum(0)>n)[0]
    return df.iloc[:,sel]

# since there's a problem in googletrans API
# we temporarily remove eng words instead of translate it 

'''
def trans_eng(documents,remove=True):    
    translator = Translator()
    def trans(match):
        print("hi")
        print(match.group())
        return translator.translate(match.group(),dest='zh-TW').text
    for title,document in documents.items():
        documents[title] = re.sub(pattern="([A-za-z]+[\[ \]*\[A-Za-z\]]+[A-Za-z])",repl=trans,string=document)
    if remove:
        sel = [title for title,document in documents.items() if re.search("([A-za-z]+[\[ \]*\[A-Za-z\]]+[A-Za-z])",document) is not None]
        documents = {title:re.subn("[A-za-z]","",document)[0] for title,document in documents.items()}
    return documents
'''
def trans_eng(documents,remove=True):    
    translator = Translator()
    def trans(match):
        print("hi")
        print(match.group())
        return translator.translate(match.group(),dest='zh-TW').text
    for title,document in documents.items():
        documents[title] = re.sub(pattern="[A-za-z]+[\[ \]*\[A-Za-z\]]+[A-Za-z]",repl="",string=document)
    if remove:
        sel = [title for title,document in documents.items() if re.search("[A-za-z]+[\[ \]*\[A-Za-z\]]+[A-Za-z]",document) is not None]
        documents = {title:re.subn("[A-za-z]","",document)[0] for title,document in documents.items()}
    return documents


def main():
    #read lyrics:
    lyrics_dic = {}
    for filename in os.listdir("jay_lyrics/"):
        with open(os.path.join("jay_lyrics/",filename),"r") as f:
            filename = filename.split(".")[0]
            lyrics_dic[filename] = f.read()

    # open stopwords
    with open( "stop_cn.txt","r") as file:
        stop = file.read().split("\n")  
        file.close()   
    stop = stop[0:13]
    stop.append("的")
    stop.append(" ")
    stop.append("你")
    stop.append("\n")
    stop.append("我")
    stop.append("周杰倫")    

    # open labels:
    df_label = pd.read_csv("label.csv",encoding = "utf-16",index_col=0)

    documents = clean(lyrics_dic)

    # remove stop word and not chinese word
    def clean_stop(document,stop,reg):
        return [word for word in document if word not in stop and not reg.findall(word)]
    reg = re.compile("[^\u4e00-\u9fa5]")
    words = {title: clean_stop(jieba.lcut(document),stop=stop,reg=reg) for title,document in documents.items()}
    wordcounts = {title:Counter(word) for title,word in words.items()}

    for word in wordcounts.keys():
        wordcounts[re.split("\(",word)[0]] = wordcounts.pop(word)

    vectorizer = DictVectorizer()
    vsm_sparse = vectorizer.fit_transform(wordcounts.values())
    rownames = list(wordcounts.keys())
    #把括號去掉(才能跟label df 對得上)
    rownames = np.array([re.split("\(",word)[0] for word in rownames])

    vsm_sparse = pd.DataFrame(wordcounts)
    vsm_sparse = vsm_sparse.transpose()


    vsm_sparse = wordcount_filter(vsm_sparse,1)    
    pd.DataFrame.to_csv(vsm_sparse.fillna(0),"vsm.csv",encoding="utf_8_sig")
    return 0

if __name__ == '__main__':
    main()