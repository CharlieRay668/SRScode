from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import random
import datetime as dt
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get("https://twitter.com/search?f=live&q=food%20until%3A2007-12-31%20since%3A2006-01-01&src=typed_query")
time.sleep(4)


base = dt.date.today()
date_list = [base - dt.timedelta(days=x) for x in range(5498)]
print(date_list[0], date_list[-1])
date_list = date_list[-10:]
print(date_list)
total = set([])
search_terms = "food "
search_bar = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input")
for index, date in enumerate(date_list):
    if index != len(date_list)-1:
        until = date
        since = date_list[index+1]
        until = str(until.year) + "-" + str(until.month) + "-" + str(until.day)
        since = str(since.year) + "-" + str(since.month) + "-" + str(since.day)
        query = "until:"+until + " since:"+since
        search_bar.clear()
        search_bar.send_keys(search_terms + query)
        webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
        time.sleep(2)
        scroll_location = 0
        results = driver.find_elements_by_class_name("css-1dbjc4n")
        for item in results:
            total.add(item.text)
        prev = -1
        x = 0
        height = -2
        while height != prev:
            prev = height
            scroll_location += 10000
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script("window.scrollTo(0, "+str(scroll_location)+")")
            results = driver.find_elements_by_class_name("css-1dbjc4n")
            time.sleep(2)
            for item in results:
                total.add(item.text)
            print(height)
            print(len(total))

# for x in range(1,100):
#     while result != prev:
#         result = driver.find_element_by_xpath(format_path(1)).text
#         # if result not in results:
#         #     results.append(result)
#         scroll_location += 10
#         driver.execute_script("window.scrollTo(0, "+str(scroll_location)+")")
#     prev = result
#     print(prev)

#print(results)
    #     if scroll_location > 2500:
    #             result = "failed"
    #             break
    # if scroll_location > 2500:
    #             break

