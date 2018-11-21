import requests
import sys
from bs4 import BeautifulSoup
from collections import defaultdict
import pythainlp
import time
import codecs

pos = 0
neg = 0
Room = "food"
BASEURL = "https://pantip.com/"
STARTURL = "https://pantip.com/forum/"+Room
processQueue = []

def parse_list_page(url):
    TITLES = []
    data = requests.get(url)
    soup = BeautifulSoup(data.content,'html.parser')

    # add next page link in to the queue
    links = soup.select('a[rel="next"]')
    nextlink = links[0].attrs['href']
    processQueue.append(
        (parse_list_page, BASEURL + nextlink)
    )

    # find all result
    titles = soup.find("div", {"class": "post-list-wrapper"})
    titles2 = titles.find_all("div", {"class": "post-item"})
    for title in titles2:
        global pos
        global neg

        #  check question post
        qestion = title.find("span", {"class": "icon-mini-posttype-que"})
        if (qestion is not None):
            extractFeature(title,"pos")
        else:
            extractFeature(title, "neg")




def extractFeature(text,postType):
    global pos
    global neg
    if('neg'==postType): neg+=1
    if('pos'==postType): pos+=1
    findalTitle = text.find("div", {"class": "post-item-title"})
    link = text.find_all("a", href=True)
    tags = text.find_all("div", {"class": "tag-item "})
    taglist = ""
    for tag in tags:
        taglist += tag.text.strip() + ","
    taglist = taglist[:-1]
    row = [findalTitle.text.strip(),taglist,link[0]['href'],postType]
    write(row,postType)

def write(row,postType):
    global Room
    f = codecs.open(postType+Room+".txt", "a", "utf-8")
    print(row)
    f.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3])
    f.write("\n")
    f.close()


def main():

    processQueue.append(
        (parse_list_page, STARTURL)
    )



    while len(processQueue):
        if pos>10000 & neg>10000: break
        time.sleep(1)
        call_back, url = processQueue.pop(0)
        call_back(url)
        print("pos: ",pos)
        print("neg: ",neg)



if __name__ == '__main__':
    main()