import requests
import datetime
from requests_html import HTML
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(__file__)

def url_to_txt(url, filename="statista.html", save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"world.html", 'w') as f:
                f.write(html_text)
        return html_text
    return ""

def parse_and_extract(url):
    html_text = url_to_txt(url)

    r_html = HTML(html=html_text)
    img_class = ".infographicsPanelCard__image"
    r_table = r_html.find(img_class)
    urls = []
    for i in range(2,6):
        url = r_table[i].attrs['data-src'] 
        urls.append(url)

    return(urls)

parse_and_extract('https://www.statista.com/chartoftheday/')