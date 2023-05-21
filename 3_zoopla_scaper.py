from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import datetime
from datetime import datetime, date
import time
import re


zrent_url = 'https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=london&results_sort=newest_listings&search_source=to-rent&pn={}_next'
zsales_url = 'https://www.zoopla.co.uk/for-sale/property/london/?price_frequency=per_month&q=london&results_sort=newest_listings&search_source=for-sale&pn={}_next'


def get_driver():
    options = uc.ChromeOptions()
    

    driver = uc.Chrome( options = options )
    # options = webdriver.ChromeOptions()

    # capabilities = DesiredCapabilities.CHROME.copy()
    # capabilities['acceptInsecureCerts'] = True

    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')
    # driver = webdriver.Chrome(r'C:\Windows\chromedriver.exe', options=options, desired_capabilities=capabilities)
    
    return driver

def get_pages(driver,page,url):
    """
    Retrieves the content of a web page using the provided Selenium WebDriver.

    Parameters:
        - driver (WebDriver): The Selenium WebDriver instance used to access the web page.
        - page (str): The name or identifier of the page being retrieved.
        - url (str): The URL of the web page to be retrieved.

    Returns:
        The HTML content of the web page.
    
    """
    driver.get(url.format(page))
    OM_DIV_TAG = 'kii3au6'
    page_html = driver.find_elements(By.CLASS_NAME, OM_DIV_TAG)
    return page_html

def parse_pages(page_html:'page_html', transaction_type:str, source:str):
    """
    Parses the given HTML content of a web page and extracts relevant information based on the provided transaction type and source.

    Parameters:
        - page_html (html elements): The HTML content of the web page to be parsed.
        - transaction_type (str): The type of transaction for which information needs to be extracted.
        - source (str): The source of the web page content.

    Returns:
        dataframe containing the data sccrapped from the website
        
    """
    page_data = []


    for page in page_html:
        # Transaction

        try:
            if transaction_type == 'rent':
                transaction = transaction_type

            elif transaction_type == 'sales':
                transaction = transaction_type

            else:
                print('transaction_type can either be sales or rent')
                break

        except:
                print('transaction_type can either be sales or rent')
                break
        

        # Address
        try:
            address_tag = page.find_element(By.CLASS_NAME, "_1ankud52")
            address = address_tag.text
        except:
            address = None

        # Bedroom
        try:         
            
            bedroom_element = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if bedroom_element.text.split("\n")[0].strip() == 'Bedrooms':
                bedroom = bedroom_element.text.split("\n")[1].strip()
            else:
                bedroom = None

        except:
            bedroom = None

        # Bathroom
        try:
            
            bathroom_tag = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if bathroom_tag.text.split("\n")[0].strip() == 'Bathrooms':
                bathroom = bathroom_tag.text.split("\n")[1].strip()

            elif bathroom_tag.text.split("\n")[2].strip() == 'Bathrooms':
                bathroom = bathroom_tag.text.split("\n")[3].strip()

            else:
                bathroom = None
        except:
            bathroom =None

        # Living room

        try:
            
            livingroom_tag = page.find_element(By.CLASS_NAME,"_1ljm00u3z    ")
            if livingroom_tag.text.split("\n")[0].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[1].strip()

            elif livingroom_tag.text.split("\n")[2].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[3].strip()

            elif livingroom_tag.text.split("\n")[4].strip() == 'Living rooms':
                living_room = livingroom_tag.text.split("\n")[5].strip()

            else:
                living_room = None
        except:
            living_room =None

        # Description
        try:
            description_tag = page.find_element(By.CLASS_NAME, '_1ankud53')
            description = description_tag.text

        except:
            description = None


        # property Type
        try:
            property_type_tag =page.find_element(By.CLASS_NAME, '_1ankud51')
            property_desc = property_type_tag.text.split("\n")[0].strip()


            match_semi = re.search(r'\bsemi-detached\b', property_desc)
            match_flat = re.search(r'\bflat\b', property_desc)
            match_apartment = re.search(r'\bapartment\b', property_desc)
            match_studio = re.search(r'\bStudio\b', property_desc)
            match_terraced = re.search(r'\bterraced\b', property_desc)
            match_penthouse = re.search(r'\bpenthouse\b', property_desc)
            match_duplex = re.search(r'\bduplex\b', property_desc)
            match_house = re.search(r'\bhouse\b', property_desc)
            match_detached = re.search(r'\bdetached\b', property_desc)
            match_maisonette = re.search(r'\bmaisonette\b', property_desc)
        
            if match_semi is not None:
                property_type = match_semi.group(0)

            elif match_flat is not None:
                property_type = match_flat.group(0)

            elif match_apartment is not None:
                property_type = match_apartment.group(0)

            elif match_studio is not None:
                property_type = match_studio.group(0)

            elif match_terraced is not None:
                property_type = match_terraced.group(0)

            elif match_penthouse is not None:
                property_type = match_penthouse.group(0)

            elif match_duplex is not None:
                property_type = match_duplex.group(0)
            
            elif match_detached is not None:
                property_type = match_detached.group(0)

            elif match_house is not None:
                property_type = match_house.group(0)

            elif match_maisonette is not None:
                property_type = match_maisonette.group(0)

            else:
                property_type = None

        except:
            property_type = None

        # rent payment
        if transaction_type == 'rent':

            sales_price = None
            
            # rent price per month
            try:
                pcm = page.find_element(By.CLASS_NAME, '_170k6632')
                per_month = int(pcm.text.split(" ")[0].strip().split("£")[1].split(" ")[0].replace(",", ""))
                
            except:
                per_month = None
                
            # rent price per week
            try:
                pw = page.find_element(By.CLASS_NAME, '_170k6633')
                per_week = int(pw.text.split(" ")[0].strip().split("£")[1].split(" ")[0].replace(",", ""))

            except:
                per_week = None               

        else:
            # sales Price
            try:
                per_week = None  
                per_month = None
                
                price_tag = page.find_element(By.CLASS_NAME, '_170k6632 ')
                sales_price = int(price_tag.text.split(" ")[0].strip().split("£")[1].split(" ")[0].replace(",", ""))
                
            except:
                sales_price = None
           
        # Location
        try:
            location_tag = page.find_element(By.CLASS_NAME, '_1ankud52')
            location = location_tag.text.split(" ")[-1].strip()
            
        
        except:
            location =None
    
        # Agent
        try: 
            agent_tag =page.find_element(By.CLASS_NAME, '_12bxhf70')
            # print(agent_tag.get_attribute('innerHTML'))
            agent = agent_tag.get_attribute('alt')
            
        except:
            agent = None


        #Listing Source
        listing_source = source

        # Listing URL
        try:
            listing_url_tag =page.find_element(By.CLASS_NAME, '_1maljyt1')
            listing_url = listing_url_tag.get_attribute('href')

        except:
            listing_url = None
        
        # Date Added
        try:
            date_tag = page.find_element(By.CLASS_NAME, '_18cib8e1')
            date_string = date_tag.text.split(" on ")[-1].strip()
            added_date = datetime.strptime(date_string,"%dth %B %Y").strftime("%d-%m-%Y")
            
        except:
            added_date = None

        # availibility
        # try:
        #     date_tag = page.find_element(By.CLASS_NAME, '_18cib8e1')
        #     date_string = date_tag.text.split(" on ")[-1].strip()
        #     available_date = datetime.strptime(date_string,"%dth %B %Y").strftime("%d-%m-%Y")
            
        # except:
        #      available_date = None
     
            
        page_data.append({
            'transaction': transaction,
            'address': address,
            'bedroom': bedroom,
            'bathroom': bathroom,
            'living_room': living_room,
            'sales_price': sales_price,
            'rent_perMonth': per_month,
            'rent_perWeek': per_week,
            'description': description,
            'propertyType': property_type,
            'location':location,
            'agent':agent,
            'listing_source':listing_source,
            'listing_url':listing_url,
            'listed_date': added_date,
            # 'available_date': available_date,
            })

    return page_data


def get_data(url,transaction_type,source,start_page, end_page):
    """
    Retrieves data from a specific range of pages on a website based on the provided parameters.

    Parameters:
        - url (str): The URL of the website.
        - transaction_type (str): The type of transaction for which data needs to be retrieved.
        - source (str): The source of the data.
        - start_page (int): The starting index of the pages to retrieve.
        - end_page (int): The ending index of the pages to retrieve (inclusive).

    Returns:
        dataframe: Data retrieved from the specified pages.

    """
    browser = get_driver()
    all_pages_data = []

    print('runing.....................................')
    
    for page in range(start_page, end_page+1):
        page_html = get_pages(browser,page,url)
        pages_data = parse_pages(page_html,transaction_type, source)
        all_pages_data.extend(pages_data)

    browser.quit()

    data = pd.DataFrame(all_pages_data)
    return data


if __name__ == "__main__":
    # Specify the start and end page numbers for scraping
    start_page = 1
    end_page = 42

    # Call the get_data function to scrape the data
    rent_data = get_data(zrent_url,'rent','zoopla',start_page, end_page)
    sales_data = get_data(zsales_url,'sales','zoopla',start_page, end_page)

    # merged the two data
    appended_data = pd.concat([rent_data, sales_data])

    #save it as csv
    appended_data.to_csv(f'data_output/zoopla_{date.today()}.csv', index=False)

    # save scrapped data to csv

    print('data scraped successfully')    


    