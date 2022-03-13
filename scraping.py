# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    data={
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "Hemispheres":hemisphere_data(),
      "last_modified": dt.datetime.now()}
    browser.quit()
    return data
    

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None,None
    return news_title, news_p


 


def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    try:    
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)    
    url = 'https://marshemispheres.com/'

    browser.visit(url) 
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    mars_hemisphere_html=browser.html
    mars_hemisphere_soup=soup(mars_hemisphere_html,"html.parser")
    #Find each hemishpere section
    mars_hemispheres=mars_hemisphere_soup.find_all("div",class_="item")

    #Iterate through the hemispheres
    for hemishpere in mars_hemispheres:
        #Visit their own page
        link=hemishpere.find("a",class_="itemLink product-item").get("href")
        new_url=url+link
        print(new_url)
        browser.visit(new_url)
        
        #Find wide image and title
        hemisphere_html=browser.html
        hemisphere_soup=soup(hemisphere_html,"html.parser")
        img_src=hemisphere_soup.find("img",class_="wide-image").get("src")
        img_title=hemisphere_soup.find("h2",class_="title").text
        
        #Add the title to a dictionario
        hemisphere_dict={}
        hemisphere_dict["img_url"]=f'{url}{img_src}'
        hemisphere_dict["title"]=img_title
        hemisphere_image_urls.append(hemisphere_dict)
    browser.quit()
    return hemisphere_image_urls

if __name__=="__main__":
    print(scrape_all())





