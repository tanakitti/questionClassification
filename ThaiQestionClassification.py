import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pythainlp
QUEUE = []
TITLES = []
BASEURL = "https://pantip.com/"
URL = "https://pantip.com/forum?tid=38260667"
food_count = defaultdict(int)  # default value of int is 0



def parse_detail_page(url):
    print("processing " + url)


def parse_list_page(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.content,'html.parser')

    links = soup.select('a[rel="next"]')
    nextlink = links[0].attrs['href']
    QUEUE.append(
        (parse_list_page, BASEURL+nextlink)
    )

    titles = soup.find("div",{"class":"post-list-wrapper"})
    titles2 = titles.find_all("div",{"class" : "post-item"})
    for title in titles2:
        qestion = title.find("span", {"class": "icon-mini-posttype-que"})
        if(qestion is not None):
            findalTitle = title.find("div",{"class":"post-item-title"})
            # print(findalTitle.text.strip())
            countPOS(findalTitle.text.strip())
            TITLES.append(findalTitle.text.strip())

def countPOS(text):
    words = pythainlp.tokenize.word_tokenize(text, engine='mm')
    partofspeech = pythainlp.tag.pos_tag(words, engine='perceptron', corpus='orchid')

    print(text)
    for food in partofspeech:
        food_count[food[1]] += 1  # increment element's value by 1


def main():

    QUEUE.append(
        (parse_list_page, URL)
    )

    i = 0;

    while len(QUEUE):
        i = i+1
        if i== 10:
            break;
        call_back, url = QUEUE.pop(0)
        call_back(url)

    print(food_count)

if __name__ == '__main__':
    main()