# importing libraries
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

products = []  # List to store name of the product
prices = []  # List to store price of the product
img = []
link = []
image = []
description = []
reviews = []
tot = []
ratings = []
lim = 15
web = 'https://www.amazon.in/s?k='
keyword = ""
HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
           'Accept-Language': 'en-US, en;q=0.5'})




def main(URL):
    # opening our output file in append mode
    #File = open("out.csv", "a")

    # specifying user agent, You can use other user agents
    # available on the internet
    # ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    #            'Accept-Language': 'en-US, en;q=0.5'})

    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # retrieving product title
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip().replace(',', '')
        if len(products) != lim:
            products.append(title_string)
            # print(title_string)
    except :
        title_string = "NA"
        products.append(title_string)
    #print("product Title = ", title_string)

    # saving the title in the file
    # File.write(f"{title_string},")

    # retrieving price
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip(
        ).replace(',', '').replace('₹', '').strip()
        if len(prices) != lim:
            prices.append(float(price))
        # print(prices)
        # we are omitting unnecessary spaces
        # and commas form our string
    except:
        price = 0
        prices.append(price)
    
    try:
        rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()[0]
        if len(ratings) != lim:
            ratings.append(float(rating))
    except:
        rating = 0
        ratings.append(rating)
    #print("Products price = ", price)

    # saving
    # File.write(f"{price},")

    try:
        review_count = soup.find("img", attrs={'id': 'landingImage'})
        if len(img) != lim:
            img.append(dict(review_count.attrs)["src"])  # print(ratings)

    except :
        review_count = "NA"
        img.append(review_count)
    try:
        desc = soup.find(
            'ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-none'})
        if len(description) != lim:
            description.append(desc.text)
    except :
        description.append('NA')
    #print("Total reviews = ", review_count)
    # File.write(f"{review_count},")
    review(URL, reviews)


def review(URL, reviews):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Accept-Language': 'en-US, en;q=0.5'})

    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    review = soup.find_all('div', attrs={
                           'class': 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})
    # for i in range(1):
    reviews = []
    for j in review:
        reviews.append(j.text.strip())
    if (len(tot) != lim):
        tot.append(reviews)  # print(tot)
    del reviews


def amazon_scraper_func(search_keyword="", sr_no = 16):
    # opening our url file to access URLs
    global keyword
    keyword = search_keyword
    req = requests.get(web+keyword, headers=HEADERS)
    soup = BeautifulSoup(req.content, "lxml")
    links = soup.find_all('a', attrs={
                      'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    for l in links:
        href = l.get('href')
        # print(href)
        url = 'https://www.amazon.in'+href
        # print(url)
        if len(link) != lim:
            link.append(url)

    # iterating over the urls
    for links in link:
        main(links)
    # review(links)
    df = pd.DataFrame({'Srno': [x for x in range(sr_no, sr_no+len(link))], 'Product_Name':products,
                        'Description':description, 'Price':prices, 'Url':link, 'Image_URL':img, 'Ratings':ratings, 
                        'Reviews':tot, 'Store' : 'a'})
    return df

# df_a = amazon_scraper_func(         #To be commented
#     search_keyword="smartphone", sr_no=14+1)

# df_a.to_json('amazon.json', orient='records')
