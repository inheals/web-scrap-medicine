#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


# !pip install beautifulsoup4 
# !pip install requests
# !pip install pandas
# !pip install selenium
# !pip install numpy
# !pip install boto3
# !pip install pymongo


# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy
import time
from pymongo import MongoClient
import boto3
import urllib 


# In[2]:


def get_secret():
    secret_name = "mongoCred-test"
    region_name = "ap-south-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
    return json.loads(text_secret_data)


# In[3]:


client = MongoClient("mongodb+srv://db-test:"+urllib.parse.quote(get_secret()['password'])+"@test.exy5k.mongodb.net/?retryWrites=true&w=majority")
db = client.medicine_database
collection = db.medicine


# In[ ]:





# In[4]:


option = webdriver.ChromeOptions()
# I use the following options as my machine is a window subsystem linux. 
# I recommend to use the headless option at least, out of the 3
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
option.add_experimental_option("detach", True)
# Replace YOUR-PATH-TO-CHROMEDRIVER with your chromedriver location
driver = webdriver.Chrome(r'C:\Users\Siddharth\Desktop\chromedriver.exe', options=option)
driver.set_window_size(19800,20000)
page = driver.get('https://www.1mg.com/drugs-all-medicines?') # Getting page HTML through request
driver.implicitly_wait(220)
# soup = BeautifulSoup(driver.page_source, 'lxml') # Parsing content using beautifulsoup
# print(driver.page_source)


# In[5]:


def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height


# In[6]:


class element_has_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, ele):
    self.ele = ele

  def __call__(self, driver):
    element = self.ele   # Finding the referenced element
    try:
        element.text
        return element
    except:
        return False


# In[8]:


med_name = []
count = 0
for num in range(2,27):
    page = 0
    print('b')
    e = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/a[{}]'.format(num))
    print(e)
    e.click()
    driver.implicitly_wait(220)
#     time.sleep(5)
    while(True):
#         print('vv')
        count += 1
        elements = driver.find_elements(By.CLASS_NAME,"style__width-100p___2woP5.style__flex-row___m8FHw")
#         for e in elements:
#             try:
#                 elements_data.append(e.text.splitlines())
#             except:
#                 driver.navigate.refresh()
                
        for ele in elements:
            wait = WebDriverWait(driver, 10)
            ele = wait.until(EC.visibility_of(ele))
            #print(ele.text)
            data = ele.text.splitlines()
            if(len(data) == 6):
                [medicine_name, mrp,  quantity, manufacture_company,composition,not_req] = data
            else:
                [medicine_name, mrp,prescription, quantity, manufacture_company,composition,not_req] = data
            medicine_data = {
                "medince_name": medicine_name,
                "mrp": mrp,
                "prescription": prescription,
                "quantity": quantity,
                "manufacture_company": manufacture_company,
                "composition": composition
            }
            coll =  collection.insert_one(medicine_data).inserted_id
#             print(coll)
# #         print(med_name)
        try:
            next_button = driver.find_element(By.CLASS_NAME, "button-text.link-next")
            count = 0
            print(page)
            next_button.click()
            page+=1
            driver.refresh()
            #time.sleep(1)
            
        except:
            print('h')
            break

                

    


# In[ ]:


print(count)


# In[ ]:




