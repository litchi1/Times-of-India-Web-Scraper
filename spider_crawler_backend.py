import urllib.request
from bs4 import BeautifulSoup
from datetime import date, timedelta
import threading
import json
import csv
import os
from all_ids import *


# create a folder to store all the images
directory1 = 'Images'
if not os.path.exists(directory1):
    os.makedirs(directory1)


# create a folder to store all the articles
directory2 = 'Articles'
if not os.path.exists(directory2):
    os.makedirs(directory2)


def spider():
    with open('my_csv.csv', 'w') as csv_file:
        field = ('UID', 'DATE', 'TITLE', 'ARTICLE_LINK')
        csv_writer = csv.DictWriter(csv_file, fieldnames=field)
        csv_writer.writeheader()

    sid = source_id()
    ssid = sub_source_id()

    # finding the start date
    st_year = int(input('Enter the starting year:: '))
    st_month = int(input('Enter the starting month:: '))
    st_day = int(input('Enter the starting day:: '))
    start_date = date(st_year, st_month, st_day)

    # finding the end date
    en_year = int(input('Enter the end year:: '))
    en_month = int(input('Enter the end month:: '))
    en_day = int(input('Enter the end day:: '))
    last_date = date(en_year, en_month, en_day)

    # compare dates
    if last_date < start_date:
        print('Date Error. Try again !')
        exit(0)

    # starttime of default tart date i.e. 01-01-2001
    start_time = 36892
    default_date = date(2001, 1, 1)

    if start_date == default_date:
        start_time = start_time
    else:
        s_day = (start_date - default_date).days
        start_time = start_time + s_day

    if last_date == start_date:
        end_time = start_time
    else:
        e_day = (last_date - start_date).days
        end_time = start_time + e_day

    end_time_limit = end_time + 1

    for dt, date1 in zip(date_range(start_date, last_date), range(start_time, end_time_limit)):
        url1 = 'https://timesofindia.indiatimes.com/2007/4/17'
        alist = '/archivelist/year-'
        year = '2007'
        month = ',month-'
        day = '4'
        starttime = ',starttime-'
        cms = '.cms'
        html = str(url1) + str(alist) + str(year) + str(month) + str(day) + str(starttime) + str(date1) + str(cms)
        try:
            url = urllib.request.urlopen(html)
            soup = BeautifulSoup(url, 'lxml')
            count = 1
            for span in soup.findAll('span', {'style': 'font-family:arial ;font-size:12;color: #006699'}):
                for link in span.findAll('a'):
                    title = link.string
                    tid = text_id(title)
                    hre = link.get('href')
                    decode = hre.split(':')
                    href = 'https' + ':' + decode[1]
                    iid = image_id()
                    auid = audio_id(html)
                    vid = video_id(html)
                    did = date_id(dt)
                    aid = all_id(sid, ssid, tid, iid, auid, vid, did, count)
                    t3 = threading.Thread(target=image(href, aid))
                    t4 = threading.Thread(target=article(href, aid))
                    t3.start()
                    t4.start()
                    with open('my_csv.csv', 'a') as csv_file:
                        field = ('UID', 'DATE', 'TITLE', 'ARTICLE_LINK')
                        csv_writer = csv.DictWriter(csv_file, fieldnames=field)
                        csv_writer.writerow({'UID': aid, 'DATE': str(dt), 'TITLE': title, 'ARTICLE_LINK': href})
                        count += 1
        except Exception:
            print('TIMES OF INDIA SERVER IS OVERLOADED NOW. INCONVENIENCE IS REGRETTED. PLEASE TRY AGAIN LATER!!')


# function to increment the dates between two dates
def date_range(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


# function to generate the url of image
def image(url, aid):
    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        for img_link in soup.findAll('link', {'itemprop': 'thumbnailUrl'}, {'rel': 'image_src'}):
            href = img_link.get('href')
            download_image(href, aid)
    except Exception:
        print('TIMES OF INDIA SERVER IS OVERLOADED NOW. INCONVENIENCE IS REGRETTED. PLEASE TRY AGAIN LATER!!')


# function to download the image
def download_image(url, aid):
    name = aid + '.jpg'
    f = open(os.path.join(directory1, name), 'wb')
    f.write(urllib.request.urlopen(url).read())
    f.close()


# function to generate the url of article and save the article in a json file
def article(url, aid):
    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        namelist = soup.findAll('div', {'class': 'article_content clearfix'}, 'arttextxml')
        for name in namelist:
            text = name.get_text()
            f_name = str(aid) + '.json'
            with open(os.path.join(directory2, f_name), 'w') as json_file:
                obj = {'UID': aid, 'Article': text}
                json.dump(obj, json_file, indent='\n')
    except Exception:
        print('TIMES OF INDIA SERVER IS OVERLOADED NOW. INCONVENIENCE IS REGRETTED. PLEASE TRY AGAIN LATER!!')


# function to generate the unique identification number
def all_id(sid, ssid, tid, iid, auid, vid, did, count):
    total = str(sid) + str(ssid) + str(tid) + str(iid) + str(auid) + str(vid) + str(did) + str(count)
    return total


# converting csv file into json file
def csv_to_json():
    with open('my_csv.csv') as c:
        reader = csv.DictReader(c)
        rows = list(reader)

    with open('my_json.json', 'w') as j:
        json.dump(rows, j, indent=4)


spider()
csv_to_json()

