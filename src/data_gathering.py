#Imports
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')

vasastan_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=925970"
kungsholmen_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=925968"
ostermalm_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=473448"
sodermalm_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=898472"
solna_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=18028"
norrmalm_url = "https://www.hemnet.se/salda/bostader?location_ids%5B%5D=925969"

area_list = [vasastan_url, kungsholmen_url, ostermalm_url, sodermalm_url, solna_url, norrmalm_url]

path = r"/chromedriver.exe"
driver = webdriver.Chrome(executable_path=path, options=options)


def attribute_extractor(text):
    text = text.lower()
    labels = ["adress", "location", "size:rooms", "fee", "features", "sale_price", "sold_date", "value_dev", "ppsqm"]
    accommodation_features = []

    value_dev_bool = -1
    text_list = text.split("\n")

    if text.find("%") == -1:
        value_dev_bool = 0
    else:
        value_dev_bool = 1

    print(text_list)

    if (len(text_list) < 9):
        if (len(text_list) == 7):
            text_list.insert(4, "null")
            text_list.insert(7, "null")
            accommodation_features = text_list
        if ((len(text_list) == 8) & (value_dev_bool == 1)):
            text_list.insert(4, "null")
            accommodation_features = text_list
        elif ((len(text_list) == 8) & (value_dev_bool == 0)):
            text_list.insert(7, "null")
            accommodation_features = text_list
    elif (len(text_list) == 9):
        if (value_dev_bool == 1):
            accommodation_features = text_list
        elif (value_dev_bool == 0):
            text_list[4] = "balkong&hiss"
            text_list.pop(5)
            accommodation_features = text_list

    elif (len(text_list) > 9):
        text_list[4] = "balkong&hiss"
        text_list.pop(5)
        accommodation_features = text_list

    housing_info_dict = dict(zip(labels, accommodation_features))
    return housing_info_dict


def hemnet_scraping(url, num_entries, counter):
    entries_per_page = 50
    outer_list = list(range(0, num_entries, entries_per_page))
    big_housing_dict = {}

    driver.get(url)
    time.sleep(2)
    if (counter == 0):
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="hcl-button hcl-button--primary"]'))).click()

        except(org.openqa.selenium.StaleElementReferenceException):
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="hcl-button hcl-button--primary"]'))).click()

    number = driver.find_elements_by_xpath('//*[@class = "result-type-toggle__count--with-upper-bound"]')
    upper_bound = number[0].text
    upper_bound = upper_bound.replace(" ", "")
    upper_bound = int(upper_bound)

    if (upper_bound < num_entries):
        num_entries = upper_bound
        outer_list = list(range(0, num_entries, entries_per_page))

    for adding_number in outer_list:

        elements = driver.find_elements_by_xpath('//*[@class ="sold-property-listing qa-sale-card"]')

        for i in range(0, len(elements)):
            big_housing_dict[i + adding_number] = attribute_extractor(elements[i].text)
            variable = elements[i].text

        # Identify next page element and scroll down to it
        try:
            next_page = driver.find_element_by_xpath(
                '//*[@class="next_page hcl-button hcl-button--primary hcl-button--full-width"]')
            # driver.execute_script("arguments[0].scrollIntoView();", next_page)
            time.sleep(1)
            # Change page
            next_page.click()
        except NoSuchElementException:
            print("cant find next button, returning current values")
            return big_housing_dict

    return big_housing_dict


counter = 0
for area in area_list:
    housing_info_dict = hemnet_scraping(area, 2500, counter)
    if (counter == 0):
        housing_info_df = pd.DataFrame(housing_info_dict).T
        counter = counter + 1
    elif (counter > 0):
        new_housing_info_df = pd.DataFrame(housing_info_dict).T
        housing_info_df = housing_info_df.append(new_housing_info_df, ignore_index=True)
        counter = counter + 1

housing_info_df.to_csv("stockholm_housing_df.csv",index=False)