#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import re
import time

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

    try:
        slide = soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None



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
    new_url = browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last['href']

    browser.find_by_css('div[class="addthis_toolbox addthis_default_style"]').find_by_css('a').last.click()

    browser = init_browser()
    browser.visit(new_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    p_tag = soup.find_all('aside')[0].find_all('p')


    
    for p in p_tag:
        print(p)
        if 'Full-Res JPG' in p.text:
            featured_image_url = 'https:'+p.a['href']


    
 
    # Mars Weather - Twitter

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    browser = init_browser()
    mars_weather = ''
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    browser.reload()
    time.sleep(5)
    html = browser.html
    time.sleep(5)
    soup = bs(html, 'html.parser')
    time.sleep(5)
    results = soup.find('div', class_= 'css-1dbjc4n').find_all('span', class_ ="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    found = False
    for result in results:
        if (bool(result.find(string=re.compile("InSight"))) & (not found)):
            mars_weather = result.find(string=re.compile("InSight"))
            print(mars_weather)
            found = True
    print(mars_weather)

       # Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    facts_list = pd.read_html(mars_facts_url)

    facts_df = facts_list[0]

    facts_df.columns = ["measure", "value"]
    
    facts_df.set_index('measure', inplace = True)
    
    facts_df_html = facts_df.to_html(classes = "table")

    facts_df.to_html('mars_fact_table.html')
    

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
           
            hemisphere_label = result.find_all('a', class_ = "itemLink product-item")[0].find('img')['alt']
            split_name = hemisphere_label.split()
            remove_words = ['Enhanced', 'thumbnail']
            
            result_words = [word for word in split_name if word not in remove_words]
            hemisphere_name.append(" ".join(result_words))
            
            hemisphere_link.append(result.find_all('a', class_= "itemLink product-item")[0]['href'])

 


    for x in range(0,4):
        browser = init_browser()
        browser.visit('https://astrogeology.usgs.gov/' +hemisphere_link[x])
        html = browser.html
        soup = bs(html, 'html.parser')
        hidef_hemisphere_link.append(soup.find_all('ul')[0].find_all('li')[1].find('a')['href'])


    

    # Put it all together
    mars_data = {'news_title' : news_title, 'news_p' : news_p, 'featured_image_url' : featured_image_url, 'mars_weather' : mars_weather, 'mars_facts' : facts_df_html, 'hemisphere_name' : hemisphere_name, 'hidef_hemisphere_link' : hidef_hemisphere_link}


 # Close the browser after scraping
    browser.quit()

    return mars_data

  




