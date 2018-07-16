#import urllib.request
#from bs4 import BeautifulSoup


# creating a function for Source ID
def source_id():
    source = str(input('Enter the news source type:: e.g. News Website, TV, Radio Feed, etc. '))
    s_uid = list(range(101))
    if source == 'News Website':
        return s_uid[0]
    else:
        print("Enter 'News Website' and try again")
        exit(0)


# creating a function for Sub Source ID
def sub_source_id():
    sub_source = str(input('Enter the news source:: '))
    ss_uid = list(range(10000))
    if sub_source == 'Times of India' or sub_source == 'TOI':
        return ss_uid[0]
    else:
        print("Enter 'Times of India' or 'TOI' and try again")
        exit(0)


# creating a function for Text ID
def text_id(title):
    if title is not None:
        return 1
    else:
        return 0


# creating a function for audio ID
def audio_id(url):
    html = url.split('/')
    if html[-1] is not 'video':
        return 0
    if html[-1] == 'video':
        web = urllib.request.urlopen(url)
        soup = BeautifulSoup(web, 'lxml')
        for link in soup.findAll('a', {'pg': 'NavBar-/subsec1-Live-Audio'}):
            href = link.get('href')
            href = 'https://timesofindia.indiatimes.com' + href
            print(href)
            return 1


# creating a function for video ID
def video_id(url):
    html = url.split('/')
    if html[-1] is not 'video':
        return 0
    else:
        web = urllib.request.urlopen(url)
        soup = BeautifulSoup(web, 'lxml')
        for link in soup.findAll('a', {'class': 'viewmore-btn jviewmore'}):
            title = link.get('title')
            print(title[10:], '\n\t')
            href = link.get('href')
            decode = href.split(':')
            if decode[0] == 'https':
                for vlink in href.findAll('class: w_img'):
                    title1 = vlink.get('title')
                    print(title1)
                    vlink2 = vlink.get('link')
                    print(vlink2)
            else:
                href = 'https://timesofindia.indiatimes.com' + href
                for vlink in href.findAll('class: w_img'):
                    title1 = vlink.get('title')
                    print(title1)
                    vlink2 = vlink.get('link')
                    print(vlink2)
        return 1


# creating a function for image ID
def image_id():
    return 1


# creating a function for date ID
def date_id(dt):
    dat = dt.strftime('%d%m%Y')
    return dat

