from newsapi.newsapi_client import NewsApiClient

newsapi = NewsApiClient(api_key='YOUR-API-KEY')

def general():
    all_articles = newsapi.get_everything(domains='reuters.com', sources='bbc-news,abc-news,associated-press,cnn',
                                  language='en',
                                  sort_by='publishedAt',
                                  page=1,
                                  page_size=10)
    list_articles = []
    for i in range(10):
        title = all_articles['articles'][i]['title']
        url = all_articles['articles'][i]['url']
        title_url = [title,url]
        list_articles.append(title_url)
    return list_articles


def tech():
    all_articles = newsapi.get_everything(domains='techcrunch.com,thenextweb.com', sources='crypto-coins-news,hacker-news,next-big-future,techradar,new-scientist',
                                  language='en',
                                  sort_by='publishedAt',
                                  page=1,
                                  page_size=10)
    list_articles = []
    for i in range(10):
        title = all_articles['articles'][i]['title']
        url = all_articles['articles'][i]['url']
        title_url = [title,url]
        list_articles.append(title_url)
    return list_articles

def finance():
    all_articles = newsapi.get_everything(domains='nasdaq.com,barrons.com, cnbc.com,bloomberg.com',sources='crypto-coins-news,business-insider,the-wall-street-journal',
                                  language='en',
                                  sort_by='publishedAt',
                                  page=1,
                                  page_size=10)
    list_articles = []
    for i in range(10):
        title = all_articles['articles'][i]['title']
        url = all_articles['articles'][i]['url']
        title_url = [title,url]
        list_articles.append(title_url)
    return list_articles

def creative():
    all_articles = newsapi.get_everything(sources='buzzfeed,entertainment-weekly,mtv-news,national-geographic,polygon,vice-news',
                                  language='en',
                                  sort_by='publishedAt',
                                  page=1,
                                  page_size=10)
    list_articles = []
    for i in range(10):
        title = all_articles['articles'][i]['title']
        url = all_articles['articles'][i]['url']
        title_url = [title,url]
        list_articles.append(title_url)
    return list_articles