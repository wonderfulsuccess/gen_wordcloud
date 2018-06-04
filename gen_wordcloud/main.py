import requests
from html2text import html2text
import re

import jieba
from wordcloud import WordCloud

url = "https://mp.weixin.qq.com/s?timestamp=1528099819&src=3&ver=1&signature=xS*qYgru-A-D0yIOpTC3BfbZ6pjUGfayCeFGjmDDWWvX6qix2cbdJ-GbVI2gm34mMsOQnzSAw2PLCJ89V2i8NKvbDOjwnQnUo6UrNoLncLhUGbT5776LQXbwm5RBAZcVSMl-hW14hST-2InP4IfCoomsTV4wGsgNzBUwy0NOzZI="

def userWords(addwords=None, stopwords=None):
    if addwords==None:addwords=''
    if stopwords==None:stopwords=''
    addwords_list = addwords.split()
    stopwords_list = stopwords.split()
    print(stopwords_list)

    if addwords != None:
        for word in addwords_list:jieba.add_word(word)

    return stopwords_list

def segment(text):
    '''
    对一段text进行分词
    input：
    text:待分词的原始文章

    return:
    seg:分词后的text list
    '''
    source_text = text
    stop_words = userWords()
    # 得到分词原始list
    seg_list = list(jieba.cut((source_text), cut_all=False))

    # 加载停用词，转化为一个list一个词为一个项目
    with open('stop_words.txt') as f:
        stop_words_part = f.read().splitlines()
        stop_words = stop_words + stop_words_part
        
    # 将单个文档分词成为一个list，文档集合和文档list的集合
    seg=[]
    for i in seg_list:
        if i=='':
                continue
        if (i not in stop_words) and (len(i)<=8):
            if len(i)==1 and ord(i)==10:
                continue
            seg.append(i)
    return seg

r = requests.get(url)

text = html2text(r.text)
text = re.split(r'\(\S+?\)',text)
text = ''.join(text)
text = segment(text)
text = " ".join(text)

wordcloud = WordCloud(font_path = "msyh.ttf").generate(text)

import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()