import requests
import sys
from bs4 import BeautifulSoup
from collections import defaultdict
import pythainlp
import time
import codecs
import csv
Room = 'art'
pos = 0
neg = 0
#Room = sys.argv[1]
# category
question_count = 0
chat_count = 0
review_count = 0
poll_count = 0
news_count = 0
sell_count = 0

# Room = "food"
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
        tag = ""
        global question_count
        global chat_count
        global review_count
        global poll_count
        global news_count
        global sell_count
        # check question post
        qestion = title.find("span", {"class": "icon-mini-posttype-que"})
        if qestion is not None :
            tag = "question"
            question_count = question_count +1
            extractFeature(title, tag)
            # extractFeature(title,"pos")
        # else:
        #     extractFeature(title, "neg")

        # check chat post
        chat = title.find("span", {"class": "icon-mini-posttype-chat"})
        if chat is not None :
            tag="chat"
            chat_count = chat_count +1
            extractFeature(title, tag)
        #     extractFeature(title, "pos")
        # # else:
        #     # extractFeature(title, "neg")
        #
        review = title.find("span", {"class": "icon-mini-posttype-review"})
        if review is not None :
            tag="review"
            review_count = review_count +1
            extractFeature(title, tag)
        #     extractFeature(title, "pos")
        #
        poll = title.find("span", {"class": "icon-mini-posttype-poll"})
        if poll is not None :
            tag = "news"
            poll_count = poll_count +1
            extractFeature(title, tag)

        news = title.find("span", {"class": "icon-mini-posttype-news"})
        if news is not None :
            tag="news"
            news_count = news_count +1
            extractFeature(title, tag)
        #     extractFeature(title, "pos")
        #
        sell = title.find("span", {"class": "icon-mini-posttype-sell"})
        if sell is not None and sell_count<=2500:
            tag="sell"
            sell_count = sell_count +1
            extractFeature(title, tag)
        #





def extractFeature(text,postType):
    global pos
    global neg
    # if('neg'==postType): neg+=1
    # if('pos'==postType): pos+=1
    findalTitle = text.find("div", {"class": "post-item-title"})
    link = text.find_all("a", href=True)
    tags = text.find_all("div", {"class": "tag-item "})
    time = text.find_all("abbr",{"class": "timeago"})
    # print(time[0]['data-utime'])
    taglist = ""
    for tag in tags:
        taglist += tag.text.strip() + ","
    taglist = taglist[:-1]
    row = [link[0]['href'].replace("/topic/",""),time[0]['data-utime'],postType,taglist,findalTitle.text.strip()]
    write(row,postType)

def write(row,postType):
    global Room
    # f = codecs.open(postType+Room+".txt", "a", "utf-8")
    # f = codecs.open(Room + "_alltags.csv", "a", "utf-8")
    print(row)
    # f.write(row[0]+", "+row[1]+", "+row[2]+", "+row[3])
    # f.write("\n")
    # f.close()

    with open(Room + "_alltags_v2.csv", mode = "a" , encoding='utf-8') as csv_file:
        # fieldnames = ['id', 'datetime', 'category','tags','title']
        # f = csv.DictWriter(csv_file, fieldnames=fieldnames)
        f = csv.writer(csv_file)
        # f.writeheader()
        # f.writerow({'id': row[0], 'datetime': row[1], 'category': row[2], 'tags': row[3], 'title': row[4]})
        f.writerow(row)



def main():

    processQueue.append(
        (parse_list_page, STARTURL)
    )



    while len(processQueue):
        # if pos>10000 & neg>10000: break
        if chat_count + review_count + poll_count + news_count + sell_count > 10000: break
        time.sleep(1)
        call_back, url = processQueue.pop(0)
        call_back(url)
        # print("pos: ",pos)
        # print("neg: ",neg)
        print("ques : ", question_count)
        print("chat : ", chat_count)
        print("review: ", review_count)
        print("poll : ", poll_count)
        print("news : ", news_count)
        print("sell : ", sell_count)
        print(chat_count + review_count + poll_count + news_count + sell_count)



if __name__ == '__main__':
    main()