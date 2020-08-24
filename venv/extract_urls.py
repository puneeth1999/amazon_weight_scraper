import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import os
import time

key = input('Please enter the item you need to scrape the details of:')

optionss = webdriver.ChromeOptions();
optionss.add_argument("headless")
#Driver for chrome
driver = webdriver.Chrome("/home/puneeth/PycharmProjects/pythonProject/amazon_scraper/venv/chromedriver", options=optionss)


#open amazon.in
driver.get("https://www.amazon.in/")
sleep(5)



#fill in the search box
try:
    driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")\
        .send_keys(str(key))
except:
    driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[3]/div/form/div[3]/div[1]/input")\
        .send_keys(str(key))

try:
    driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input").click()
except:
    driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[3]/div/form/div[2]/div/input").click()
sleep(2)
'''___________________________________________________WORKS FINE TILL NOW______________________________________________________________________________________'''

sleep(2)
#find the individual item blocks using class name
blocks = driver.find_elements_by_class_name('sg-col-inner')
sleep(2)

#Open a file outside the loop
file = open('urls.txt', 'w')


#inner blocks
for block in blocks:
    try:
        divver = block.find_element_by_tag_name('div')
        insider = divver.find_element_by_class_name('sg-col-inner')
        h2 = insider.find_element_by_tag_name('h2')
        a = h2.find_element_by_tag_name('a')
        res= a.get_attribute("href")
        file.write(str(res)+"\n")
    except:
        pass
file.close()
os.system('python amazon.py')

'''_NOTHING TO DO HERE_'''


