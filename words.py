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
        self.sim_words = []
        self.get_root_url()
        self.get_similar_words()
    
    def get_root_url(self,):
        html = requests.get(url=self.base_url).content
        soup = BeautifulSoup(html, 'lxml')
        try: soup.find('ul',{'class':'titles'}).find('h3').find('a')['href']
        except: return
        self.root_url = soup.find('ul',{'class':'titles'}).find('h3').find('a')['href']
        self.word_root = soup.find('ul',{'class':'titles'}).find('h3').find('a').text[3:]

    def get_similar_words(self,):
        if self.root_url == '': return
        html = requests.get(url=self.root_url).content
        soup = BeautifulSoup(html,'lxml')
        sim_words = soup.find('div',{'class':'wdef'}).find_all('li')[1:]
        for i in range(len(sim_words)):
            self.sim_words.append(sim_words[i].text.replace('\t','').replace('\n','').replace('\xa0',''))

    def get_mk(self,):
        if self.root_url == '':
            print("抱歉，这个单词目前没有找到词根！")
            return
        words_meanings = []
        for i in self.sim_words:
            words_meanings.append((i.split(' ')[0],i.split(' ')[2]))
        title = '\n### {}\n|单词|释义|\n|:---:|:---:|\n'.format(self.word_root)
        with open(self.path,'a+') as f:
            f.write(title)
            for i in words_meanings:
                f.write('|{}|{}|\n'.format(i[0],i[1]))

if __name__ == '__main__':
    word = input('请输入您要查询的单词：')
    wr = WordRoot(word)
    wr.get_mk()

