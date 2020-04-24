import requests
from bs4 import BeautifulSoup
import os

class WordRoot:

    def __init__(self,word):
        self.path = 'D:\Markdown\words.md'
        self.word = word
        self.base_url = 'http://www.cgdict.com/index.php?app=cigen&ac=word&w={}'.format(word)
        self.root_url = ''
        self.word_root = ''
        self.root_meaning = ''
        self.sim_words = []
        self.get_root_url()
        self.get_similar_words()
    
    def get_root_url(self,):
        html = requests.get(url=self.base_url).content
        soup = BeautifulSoup(html, 'lxml')
        try: soup.find('ul',{'class':'titles'}).find('h3').find('a')['href']
        except: return
        self.root_url = soup.find('ul',{'class':'titles'}).find('h3').find('a')['href']
        self.word_root = soup.find('ul', {'class': 'titles'}).find('h3').find('a').text[3:]
        self.root_meaning = soup.find('p', {'class': 'titles-b'}).text.replace('\t','').replace('\n','').replace('\xa0','')[3:-1]

    def get_similar_words(self,):
        if self.root_url == '': return
        html = requests.get(url=self.root_url).content
        soup = BeautifulSoup(html,'lxml')
        sim_words = soup.find('div',{'class':'wdef'}).find_all('li')[1:]
        for i in range(len(sim_words)):
            self.sim_words.append(sim_words[i].text.replace('\t','').replace('\n','').replace('\xa0',''))

    def get_mk(self,):
        words_meanings = []
        for i in self.sim_words:
            words_meanings.append((i.split(' ')[0],i.split(' ')[2]))
        title = '\n### {} ：{}\n|单词|释义|\n|:---:|:---:|\n'.format(self.word_root,self.root_meaning)
        with open(self.path,'a+') as f:
            f.write(title)
            for i in words_meanings:
                f.write('|{}|{}|\n'.format(i[0],i[1]))

if __name__ == '__main__':
    while True:
        word = input('请输入您要查询的单词：')
        if word == '-1':
            break
        wr = WordRoot(word)
        if wr.word_root == '':
            print("抱歉，这个单词目前没有找到词根！")
            continue
        do = input('查询到 {} 的词根是 {} ，请问是否写入笔记： '.format(word,wr.word_root))
        if do == '1':
            wr.get_mk()
            print('词根 {} 已写入笔记！！！'.format(wr.word_root))
        else: print('并未写入笔记！！！')

