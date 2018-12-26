import jieba
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from scipy.misc import imread
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from wordcloud import WordCloud, ImageColorGenerator

def structure_url():
    urls = []
    url_bas = 'https://movie.douban.com/subject/25949771/comments?'
    for i in range(0, 180, 20):
        params = {
            'start': i,
            'limit': 20,
            'sort': 'new_score',
            'status': 'P'
        }
        url = url_bas + urlencode(params)
        yield url

def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)

def parse(text, comments, pub_date, supports):
    soup = BeautifulSoup(text, 'lxml')
    comment = soup.find_all('span', class_='short')
    pub_time = soup.find_all('span', class_='comment-time')
    support = soup.find_all('span', class_='votes')
    for i in range(len(comment)):
        comments.append(comment[i].text)
        pub_date.append(pub_time[i].text.strip())
        supports.append(support[i].text)
    return comments, pub_date, supports

def pads(comments, pub_date, supports):
    data = pd.DataFrame({'date': pub_date, 'comment': comments, 'support': supports})
    data['showName'] = '非常6+1'
    data.sort_values('date', ascending=True)
    return data

def jb(comment):
    '''
    分词
    :param comment:
    :return:
    '''
    line = ','.join(comment)
    word_list = jieba.cut(line, cut_all=False)
    word_cut = ','.join(word_list)
    return word_cut

def wdcld(word_cut):
    '''
    生成词云
    :param word_cut:
    :return:
    '''
    cloud_mask = np.array(Image.open(r'D:\tools_WorkSpace\python-code\wordCloud\images\Alice_1.jpg'))
    back_color = imread(r'D:\tools_WorkSpace\python-code\wordCloud\images\Alice_1.jpg')
    image_colors = ImageColorGenerator(back_color)

    wd = WordCloud(font_path=r'D:\tools_WorkSpace\python-code\wordCloud\font-style\HYBOBOXianShengW.ttf',
                   background_color='white', max_words=500,
                   # max_font_size=50,
                   # random_state=15,
                   width=1000,
                   height=1000,
                   mask=cloud_mask)

    WD = wd.generate(word_cut)
    WD.to_file('非常6+1.jpg')
    show(WD, image_colors)
def show(WD, image_colors):
    '''
    显示词云图片
    :return:
    '''
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(WD.recolor(color_func=image_colors))
    plt.show()


def main():
    comments = []
    pub_date = []
    supports = []
    for url in structure_url():
        text = download(url)
        comments, pub_date, supports = parse(text, comments, pub_date, supports)
    data = pads(comments, pub_date, supports)
    # print(data)
    word_cut = jb(comments)
    wdcld(word_cut)

if __name__ == '__main__':
    main()

