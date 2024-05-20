from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent
import time
import random
from selenium.webdriver.chrome.options import Options
import pymysql
import pymysql.cursors

url = ("https://www.doordash.com/store/mcdonald's-southside-837652/?cursor=eyJzZWFyY2hfaXRlbV9jYXJvdXNlbF9jdXJzb3IiOnsicXVlcnkiOiJtYyBkb24iLCJpdGVtX2lkcyI6W10sInNlYXJjaF90ZXJtIjoibWMgZG9uIiwidmVydGljYWxfaWQiOi05OTksInZlcnRpY2FsX25hbWUiOiJhbGwifSwic3RvcmVfcHJpbWFyeV92ZXJ0aWNhbF9pZHMiOlsxLDE5Nl19&pickup=false")
url2=('https://frugal-foods.circuitbreakers.tech/restaurant/7')
url3=('https://www.grubhub.com/restaurant/mcdonalds-267-broadway-brooklyn/1339391')
url4=("https://www.ubereats.com/store/mcdonalds-brooklyn-flatbush-ave/mAWk-EcAQ3GYjO2AIcKMrw?diningMode=DELIVERY")
# result = requests.get(url).text

# options = Options()
# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
# options.add_argument(f'--user-agent={user_agent}')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.get(url)

x = 0
l = 50
divs = []

while True:
    x += 1
    driver.execute_script('scrollBy(0,30)')
    page = BeautifulSoup(driver.page_source, 'lxml')
    results = page.findAll('div', {'data-anchor-id' : "MenuItem"})
    divs.extend(results)
    print(f'{x} of {l} done.')
    # with open('dd.html', 'w', encoding='utf-8') as f:
    #     f.write(str(page.contents))
    # n = random.randint(0,50)
    # if n == 5:
    #     print('Time to sleep')
    #     time.sleep(2)
        
    # if x == l:
    #     j = input('Do you want to add more? (Y/N)')
    #     if j == 'Y':
    #         l+=200
    #     else:
    #         break

    if x == l:
        break

db_link = '127.0.0.1'

connection = pymysql.connect(
    database = 'frugal_foods',
    user = 'cvasquez',
    password = '242590909',
    host = db_link,
    cursorclass = pymysql.cursors.DictCursor
)
limit = []
for items in divs:
    limit.extend(items)
    if items in limit:
        continue
    else:
        Item_Name = items.find('h3', {'data-telemetry-id' : "storeMenuItem.title"})
        item_name = Item_Name.contents

        Price = items.find('span', {'data-anchor-id' : "StoreMenuItemPrice"})
        item_price = Price.contents
        item_price = [item.replace('$', '') for item in item_price]

        Picture = items.find('img')
        item_picture = Picture.attrs['src']

        Des = items.find('span', {'data-telemetry-id' : "storeMenuItem.subtitle"})
        item_des = Des.contents

        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO `items` (`item_name`, `picture`, `restaurant_id`, `item_description`, `category_id`) VALUES ("{item_name[0]}", "{item_picture}", "1", "{item_des[0]}", "1");')
        connection.commit()
        cursor.execute(f"SELECT `item_id` FROM `items` ORDER BY `item_id` DESC;")
        connection.commit()
        id = cursor.fetchone()
        result = id['item_id']
        cursor.execute(f'INSERT INTO `price` (`price_value`, `item_id`, `service_id`) VALUES ("{item_price[0]}", "{result}","1")')
        cursor.close()
        connection.commit()

print(f'Data has been submitted to the Database. Please check if data is correct in: {db_link}')

driver.quit()