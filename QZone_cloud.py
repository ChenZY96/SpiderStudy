#coding:utf-8
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

#提取出原来字典中的content内容，用于制作词云
#f = open('QZone.txt').readlines()
#for each in f:
#    content = eval(each)
#    with open('content.txt','a+') as f:
#        f.write(content['content']+'\n')

#添加不被分割的词
#jieba.add_word()



#生成词云
def create_word_cloud(filename):
    text= open("{}.txt".format(filename)).read()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
       background_color="white",
         # 设置最大显示的词云数
       max_words=2000,
         # 这种字体都在电脑字体中，一般路径
       font_path=r'/System/Library/Fonts/STHeiti Light.ttc',
       height= 1200,
       width= 1600,
        # 设置字体最大值
       max_font_size=100,
     # 设置有多少种随机生成状态，即有多少种配色方案
       random_state=30,
    )

    myword = wc.generate(wl)  # 生成词云
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('WordCloud.png')  # 把词云保存下

if __name__ == '__main__':
    create_word_cloud('content')

