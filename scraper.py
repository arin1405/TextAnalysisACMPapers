import re
import gc
import time
import random
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    
def connect(url):      
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    abstract_content = soup.find('div',attrs={"id" : "cf_layoutareaabstract"}).findAll(text=True)
    abstract_str = ', '.join([x.strip() for x in abstract_content])
    abstract = abstract_str.strip("\n").replace(",","").replace("\n","").replace("'","")
    return abstract

#connection
domain = 'http://dl.acm.org/'
publication_id = 100001
i = 0
while i < 1:
    try:
        abstract = connect(domain+'citation.cfm?id='+str(publication_id))
    except Exception as e: 
        print(e)
        gc.collect()
        driver.quit()
    if abstract=='':
        print('Abstract not available: ',publication_id)
        publication_id+=1
        continue
    else:
        print('Abstract available: ',publication_id)
        i+=1
    try:
        file = open('datafile.csv','a+')
        l = str(publication_id)+','+abstract+'\n'
        file.write(l)
        file.close()
    except Exception as e: 
        print(e)
        gc.collect()
        driver.quit()
    publication_id+=1       
    print("\npublication added!")
gc.collect()
driver.quit()