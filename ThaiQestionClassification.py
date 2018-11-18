import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pythainlp
import time
import codecs
post = 0;
Room = "food"
QUEUE = []
BASEURL = "https://pantip.com/"
URL = "https://pantip.com/forum/"+Room
food_count = defaultdict(int)  # default value of int is 0



def parse_detail_page(url):
    print("processing " + url)


def parse_list_page(url):
    TITLES = []
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
        global post;

        qestion = title.find("span", {"class": "icon-mini-posttype-que"})
        if(qestion is not None):
            post += 1
            print("processing "+post)
            findalTitle = title.find("div",{"class":"post-item-title"})
            tags =  title.find_all("div",{"class":"tag-item "})
            # print(findalTitle.text.strip())
            taglist = ""
            for tag in tags:
                taglist += tag.text.strip()+","
            taglist = taglist[:-1]
            row = [findalTitle.text.strip(),taglist]
            TITLES.append(row)
    return TITLES

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
        if post>10000 : break
        time.sleep(1)
        call_back, url = QUEUE.pop(0)
        write(call_back(url))

    print(food_count)

def write(texts):
    global Room
    f = codecs.open(Room+"txt", "a", "utf-8")
    for i in range(len(texts)):

        f.write(texts[i][0]+"\t"+texts[i][1])
        f.write("\n")

    f.close()


if __name__ == '__main__':
    main()