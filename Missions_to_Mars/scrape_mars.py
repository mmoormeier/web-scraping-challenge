#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all("div", class_= "image_and_description_container")

    for result in results:
        print("_______")
        #print (result)
        try:
            print(result.find("div", class_='content_title').text)
            news_title = (result.find("div", class_='content_title').text)
        except:
            print("")
        try:
            print(result.find("div", class_='article_teaser_body').text)
            news_p = (result.find("div", class_='article_teaser_body').text)
        except:
            print("")



    # JPL Mars Space Images

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser = init_browser()
   
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.find_by_id("full_image").click()

    browser.find_by_text("more info")

    browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]')

    #build url query
    url = browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last['href']

    browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last.click()

    print(url)


    browser = init_browser()
    browser.visit(url)



    html = browser.html
    soup = bs(html, 'html.parser')

    p_tag = soup.find_all('aside')[0].find_all('p')


    soup.find_all('aside')[0].find_all('p')[6].text


    for p in p_tag:
        print(p)
        if 'Full-Res JPG' in p.text:
            featured_image_url = p.a['href']


    featured_image_url
 
    # Mars Weather - Twitter

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)


    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('span')

    # loop through list of tweets to find latest with weather data
    y=0
    found = False

    for result in results:
        y = y+1
        if (('low' in result.text) & ('C' in result.text) & (not found)):
            print(result)
            print(y)
            mars_weather = result.text
            found = True


       # Mars Facts

    fact_url = 'https://space-facts.com/mars'
    fact_list = pd.read_html(fact_url)

    fact_df = fact_list[0]

    fact_df.columns = ["measure", "value"]


    fact_df.set_index('measure', inplace = True)
    fact_df


    # Mars Hemisphere

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_ = "item")


    for result in results:
        print(result)


    hemisphere_link = []
    hidef_hemisphere_link = []
    hemisphere_name = []

    x = 0
    for result in results:
        x = x+1
        if result.find('a', class_ = "itemLink product-item"):
            print("-------------------")
            print(x)
            print(result)
            hemisphere_label = result.find_all('a', class_ = "itemLink product-item")[0].find('img')['alt']
            split_name = hemisphere_label.split()
            remove_words = ['Enhanced', 'thumbnail']
            print(split_name)
            result_words = [word for word in split_name if word not in remove_words]
            hemisphere_name.append(" ".join(result_words))
            print(hemisphere_name)
            print(result.find_all('a', class_ = "itemLink product-item")[0]['href'])
            hemisphere_link.append(result.find_all('a', class_= "itemLink product-item")[0]['href'])



    hemisphere_name

    hemisphere_link


    for x in range(0,4):
        browser = init_browser()
        browser.visit('https://astrogeology.usgs.gov/' +hemisphere_link[x])
        html = browser.html
        soup = bs(html, 'html.parser')
        hidef_hemisphere_link.append(soup.find_all('ul')[0].find_all('li')[1].find('a')['href'])


    hidef_hemisphere_link

    # Put it all together
    mars_data = {'news_title' : news_title, 'news_p' : news_p, 'featured_image_url' : featured_image_url, 'mars_weather' : mars_weather, 'hemisphere_name' : hemisphere_name, 'hidef_hemisphere_link' : hidef_hemisphere_link}


 # Close the browser after scraping
    browser.quit()




    return mars_data

  




