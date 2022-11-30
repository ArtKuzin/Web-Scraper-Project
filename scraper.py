import os
import string
import requests
from bs4 import BeautifulSoup


def save_article(url):
    url = 'https://www.nature.com' + url
    r = requests.get(url)
    if r.status_code != 200:
        print(f'The URL returned {r.status_code}!')
        exit(1)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('title').string.strip()
    filename = ''
    for i in title:
        if i not in string.punctuation:
            filename += i
    filename = filename.replace(' ', '_') + '.txt'
    body = soup.find('div', {'class': 'c-article-body main-content'}).text.strip().encode(encoding='utf-8')
    file = open(filename, 'wb')
    file.write(body)
    file.close()


def main():
    wanted_pages = int(input())
    wanted_types = input()
    for i in range(wanted_pages):
        os.mkdir('Page_' + str(i + 1))
        os.chdir('Page_' + str(i + 1))
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(i + 1)
        r = requests.get(url)
        if r.status_code != 200:
            print(f'The URL returned {r.status_code}!')
            exit(1)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        for a in articles:
            article_type = a.find('span', {'class': 'c-meta__type'})
            if article_type.string == wanted_types:
                link = a.find('a', {'data-track-action': 'view article'}).get('href')
                save_article(link)
        os.chdir(os.path.dirname(os.getcwd()))
    print('Saved all articles.')


if __name__ == '__main__':
    main()
