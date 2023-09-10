from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Edge('./msedgedriver.exe')
time(10)

page_keyword = {'GLOBAL HOUSE':'?page=', 'DOHOME':'?p='}
target_category = {
    'GLOBAL HOUSE': {'น้ำยาล้างจาน':'https://globalhouse.co.th/category/883'
                    ,'น้ำยาล้างห้องน้ำ':'https://globalhouse.co.th/category/889'
                    ,'ผงซักฟอก/น้ำยาซักผ้า':'https://globalhouse.co.th/category/1136'
                    ,'น้ำยาปรับผ้านุ่ม':'https://globalhouse.co.th/category/1137'
                    ,'น้ำยาปรับอากาศ':'https://globalhouse.co.th/category/878'
                    ,'ถุงขยะ':'https://globalhouse.co.th/category/906'}
    , 'DOHOME': {'น้ำยาล้างจาน':'https://www.dohome.co.th/th/consumption-goods/chattels/dish-detergent/dishwashing-liquid.html'
                ,'น้ำยาล้างห้องน้ำ':'https://www.dohome.co.th/th/consumption-goods/chattels/cleaners/bathroom-cleaners.html'
                ,'ผงซักฟอก/น้ำยาซักผ้า':'https://www.dohome.co.th/th/consumption-goods/chattels/laundry/powder-detergent.html'
                ,'น้ำยาปรับผ้านุ่ม':'https://www.dohome.co.th/th/consumption-goods/chattels/laundry/fabric-softeners.html'
                ,'น้ำยาปรับอากาศ':'https://www.dohome.co.th/th/consumption-goods/chattels/air-fresheners.html'
                ,'ถุงขยะ':'https://www.dohome.co.th/th/household-items/kitchen-appliances-hot-air-oven/bin-bags.html'}
}

col_name = ['store', 'category', 'item', 'price', 'unit']

#Scrape GLOBAL HOUSE
data = []
key = 'GLOBAL HOUSE'
for category,url in target_category[key].items():
    driver.get(url)
    time.sleep(15)
    page_list = [i.text for i in driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section/div[2]/div[2]/nav/ul')][0].split("\n")
    if len(page_list) == 1:
        url_list = [url]
    else:
        url_list = []
        for p in range(len(page_list)):
            if page_list[p] != '1':
                new_url = url + page_keyword[key] + page_list[p]
                url_list.append(new_url)
            else:
                new_url = url
                url_list.append(new_url)

    for u in url_list:
        driver.get(u)
        time.sleep(15)
        elements = [e.text for e in driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section/div[2]/div[2]/div[2]/article')]
        for element in elements:
            item_list = element.split("\n")
            if len(item_list) > 3:
                item_list = item_list[0:2] + item_list[-1:]
            temp = [key, category] + item_list
            data.append(temp)
df_raw_global_house = pd.DataFrame(data, columns=col_name)
df_raw_global_house.to_csv('./raw_global_house_product_details.csv')

#Scrape DOHOME
data = []
key = 'DOHOME'
for category,url in target_category[key].items():
    driver.get(url)
    time.sleep(15)
    try:
        page_list = [i.text for i in driver.find_elements(By.XPATH, '//*[@id="amasty-shopby-product-list"]/div[3]/div[2]/ul')][0].split("\n")
        page_list = [i for i in page_list if i not in ["You're currently reading page", 'หน้าที่', 'Next']]
    except:
        page_list = ['1']
    if len(page_list) == 1:
        url_list = [url]
    else:
        url_list = []
        for p in range(len(page_list)):
            if page_list[p] != '1':
                new_url = url + page_keyword[key] + page_list[p]
                url_list.append(new_url)
            else:
                new_url = url
                url_list.append(new_url)
    for u in url_list:
        driver.get(u)
        time.sleep(15)
        elements = [e.text for e in driver.find_elements(By.XPATH, '//*[@id="amasty-shopby-product-list"]/div[2]/ol')][0].split("\n")
        elements = [e for e in elements if e != 'ให้คะแนน:' and '%' not in e]
        for ii in range(0, len(elements), 3):
            item_list = [elements[ii], elements[ii+2].split(' ')[0], elements[ii+2].split('/')[-1]]
            temp = [key, category] + item_list
            data.append(temp)
df_raw_dohome = pd.DataFrame(data, columns=col_name)
df_raw_dohome.to_csv('./raw_dohome_product_details.csv')
driver.quit()