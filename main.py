import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

ZILLOW_PAGE = "https://appbrewery.github.io/Zillow-Clone/"
SURVEY_FORM="https://docs.google.com/forms/d/e/1FAIpQLSe_ViT32Atkwb2b4nCQXD0F2GpnwY6GpuvZXw4P8nb7Pxxfhg/viewform?usp=sf_link"
XPATH_address = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
XPATH_price ='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
XPATH_link = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
XPATH_submit = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
XPATH_another_entry = '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'

def collect_property_data():
    """Using BS4 to find the property data, clean up their format,
    and convert them into 3 separate lists"""
    response = requests.get(url=ZILLOW_PAGE)
    zillow_webpage = response.text
    soup = BeautifulSoup(zillow_webpage,"lxml")

    ## Find the elements and convert into 3 lists.
    addresses = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
    address_list = [address.getText().strip().replace("|","") for address in addresses]

    rents = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
    rents_list = [[rent.getText().replace("+","").replace("/"," ").split(" ")][0][0] for rent in rents]

    links = soup.find_all(class_="property-card-link")
    links_list = [link['href'] for link in links]

    return address_list, rents_list, links_list

def fill_form(address_list, rents_list, links_list):
    """initiate the Webdriver, find the fields elements on the form
    and loop through the list to fill out the property data """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SURVEY_FORM)
    time.sleep(3)
    for i in range(0,len(address_list)+1):
        address_field = driver.find_element(By.XPATH, value=XPATH_address)
        address_field.send_keys(address_list[i])

        price_field = driver.find_element(By.XPATH, value=XPATH_price)
        price_field.send_keys(rents_list[i])

        link_field = driver.find_element(By.XPATH, value=XPATH_link)
        link_field.send_keys(links_list[i])
        time.sleep(2)

        submit = driver.find_element(By.XPATH, value=XPATH_submit)
        submit.click()
        time.sleep(2)

        another_entry = driver.find_element(By.XPATH, value=XPATH_another_entry)
        another_entry.click()
        time.sleep(2)

    driver.quit()


address_list, rents_list, links_list= collect_property_data()
fill_form(address_list, rents_list, links_list)