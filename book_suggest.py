import requests
import pandas as pd
from io import StringIO

repository = ['link-to-file']

def viz():
    r = requests.get(repository)
    data = r.content
    s=str(data, 'utf-8')
    data = StringIO(s)
    book_list=pd.read_csv(data)
    return book_list

def podcast():
    r = requests.get(repository)
    data = r.content
    s=str(data, 'utf-8')
    data = StringIO(s)
    podcast_list=pd.read_csv(data)

    return podcast_list

def book_iteng():
    r = requests.get(repository)
    data = r.content
    s=str(data, 'utf-8')
    data = StringIO(s)
    book_list=pd.read_csv(data)

    return book_list