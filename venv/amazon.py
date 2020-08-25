from selectorlib import Extractor
import requests 
import json 
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
i=0
j=0
item_weights = []
optionss = webdriver.ChromeOptions();
optionss.add_argument("headless")
#Driver for chrome
driver = webdriver.Chrome("/home/puneeth/PycharmProjects/pythonProject/amazon_scraper/venv/chromedriver", options=optionss)


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

desc_file = open('product_desc.json', 'w')
desc_file.write('[\n')
desc_file.write("{")

# product_data = []
with open("urls.txt",'r') as urllist, open('output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        '''Temporarily commented'''
        data = scrape(url)
        if data:
            json.dump(data,outfile)
            outfile.write(",\n")
            # sleep(5)
        '''Temporarily commented'''
with open("urls.txt", "r") as urllist:
    for url in urllist.read().splitlines():
        try:
            driver.get(url)
            table = driver.find_elements_by_tag_name('table')
            t = table[1]
            t2 = table[2]
            t_body = t.find_element_by_tag_name('tbody')
            trs = t.find_elements_by_tag_name('tr')
            trs2 = t2.find_elements_by_tag_name('tr')

            print(t.text)
            print(t2.text)


            if(len(trs2) > 7):
                # desc_file.write('{')
                for i in range(len(trs2)):
                    if(i == (len(trs2) - 1)):
                        th = trs2[i].find_element_by_tag_name('th')
                        td = trs2[i].find_element_by_tag_name('td')
                        desc_file.write("\"" + th.text + "\"" + ":" + "\"" + td.text + "\"")
                        if(th.text == 'Item Weight'):
                            item_weights.append(td.text)
                        break

                    else:
                        th = trs2[i].find_element_by_tag_name('th')
                        td = trs2[i].find_element_by_tag_name('td')
                        desc_file.write("\"" + th.text + "\"" + ":" + "\"" + td.text + "\",")
                        if (th.text == 'Item Weight'):
                            item_weights.append(td.text)
                desc_file.write("},\n{")
            if (len(trs) > 7):
                for i in range(len(trs)):
                    if (i == len(trs) - 1):
                        th = trs[i].find_element_by_tag_name('th')
                        td = trs[i].find_element_by_tag_name('td')
                        desc_file.write("\"" + th.text + "\"" + ":" + "\"" + td.text + "\"")
                        if (th.text == 'Item Weight'):
                            item_weights.append(td.text)
                        break

                    else:
                        th = trs[i].find_element_by_tag_name('th')
                        td = trs[i].find_element_by_tag_name('td')
                        desc_file.write("\"" + th.text + "\"" + ":" + "\"" + td.text + "\",")
                        if (th.text == 'Item Weight'):
                            item_weights.append(td.text)

                desc_file.write("}\n{")
        except:
                pass

        print('Finished ROUND -',j)
        j+=1


desc_file.write('\n]')
desc_file.close()
print('\n\n')
print(item_weights)

def getWeight(item_weight_str):
    weight_lst = weight_str.split(" ")
    kilos = 0.0
    grams = 0.0
    try:
        grams = float(weight_lst[weight_lst.index('g') - 1])
    except:
        pass
    try:
        kilos = float(weight_lst[weight_lst.index('kg') - 1])
    except:
        pass
    total_weight = kilos + (grams/1000)
    return total_weight
print('\n')

weights = []

for l in item_weights:
    stri = l
    st_lis = stri.split()
    if(len(st_lis) == 4):
        print((int(st_lis[0])*1000) + int(st_lis[2]))
        weights.append((int(st_lis[0])*1000) + int(st_lis[2]))
    else:
        print(int(st_lis[0]))
        weights.append(int(st_lis[0]))

if(len(weights) < 1):
    print("Weights couldn't be scraped. Sorry!")
else:
    print('\nmaximum value:\t',  max(weights))


print(weights)
