import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#Function to extract Title
def get_title(soup):
    try:
        title = soup.find("a", attrs={"class": 'title'})

        title_value = title.text

        #Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


#Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("h4", attrs={'class': 'price float-end card-title pull-right'}).string.strip()

    except:
        price = ""

    return price


#Function to extract Product Description
def get_desc(soup):
    try:
        description = soup.find("p", attrs={'class': 'description card-text'}).string.strip()

    except:
        description = ""

    return description


#Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("p", attrs={'class': 'review-count float-end'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


if __name__ == '__main__':

    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})

    #webpage URL
    URL = "https://webscraper.io/test-sites/e-commerce/ajax"

    #HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    #Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    links = soup.find_all("a", attrs={'class': 'title'})
    links_list = []

    #Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    d = {"title": [], "price": [], "description": [], "reviews": []}

    for link in links_list:
        new_webpage = requests.get("https://webscraper.io/" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        #Functions to display all necessary product information
        d['title'].append(get_title(soup))
        d['price'].append(get_price(soup))
        d['description'].append(get_desc(soup))
        d['reviews'].append(get_review_count(soup))

    demo_df = pd.DataFrame.from_dict(d)
    demo_df.to_csv("scrapped_data.csv", header=True, index=False)


print(demo_df)

