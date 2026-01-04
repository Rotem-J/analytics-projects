from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
import os

url = "https://gemelnet.cma.gov.il/views/dafmakdim.aspx"
download_path = "/Users/rotemjablonsky/python/yields_scraper"

def check_new_file(category_name, sub_category):
    existing_files = set(os.listdir(download_path))
    timeout = 30
    start_time = time.time()

    continue_loop = True
    while continue_loop:
        current_files = set(os.listdir(download_path))
        new_files = current_files - existing_files

        print(f'New file detected: {new_files}')

        for file in new_files:
            if file.endswith('.xls') or file.endswith('.xlsx'):
                print(f'New file found: {file}')
                new_name = f'{category_name}_{sub_category}.xls'
                old_path = os.path.join(download_path, file)
                new_path = os.path.join(download_path, new_name)
                os.rename(old_path, new_path)
                continue_loop = False
                break

        if time.time() - start_time > timeout:
            print('No new file found')
            driver.quit()
            break

        time.sleep(1)

def yields_extractor(kupot, category_name):
    for kupa in kupot:
        try:
            text_entry.send_keys(f'{kupa}')
            WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.ID, 'selActiveKupot'), f'{kupa}'))
            add_button = driver.find_element(By.ID, 'btnAdd')
            add_button.click()
            WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.ID, 'selSelectedKupot'), f'{kupa}'))
            text_entry.clear()
        except TimeoutException:
            print(f'waiting time for kupa: {kupa} over')
            text_entry.clear()
        except NoSuchElementException:
            print(f'kupa: {kupa} does not found')
            text_entry.clear()

    load_table_and_export(load_table=load_table, export_to_excel_button=export_to_excel_button, category_name=category_name, sub_category='yields')
    alpha_button.click()
    load_table_and_export(load_table=load_table, export_to_excel_button=export_to_excel_button, category_name=category_name, sub_category='alpha')
    yield_button.click()
    remove_kupot()

def load_table_and_export(load_table, export_to_excel_button, category_name, sub_category):
    load_table.click()
    time.sleep(8)
    export_to_excel_button.click()
    print('Export to excel button clicked, waiting for a new file...')
    check_new_file(category_name, sub_category)

def remove_kupot():
    for option in list(selected_dropdown.options):
        value = option.get_attribute("value")
        selected_dropdown.select_by_value(value)
        remove_button.click()
        time.sleep(0.2)

hishtalmut_clali = [
    'הראל השתלמות כללי',
    'כלל השתלמות כללי',
    'מגדל השתלמות כללי',
    'מנורה השתלמות כללי',
    'מיטב השתלמות כללי',
    'אנליסט השתלמות כללי',
    'הפניקס השתלמות כללי',
    'אלטשולר שחם השתלמות כללי',
    'ילין לפידות קרן השתלמות מסלול כללי',
    'מור השתלמות - כללי'
]

hishtalmut_stocks = [
    'מגדל השתלמות מניות',
    'מיטב השתלמות מניות',
    'אנליסט השתלמות מניות',
    'הפניקס השתלמות מניות',
    'מנורה השתלמות מניות',
    'כלל השתלמות מניות',
    'אלטשולר שחם השתלמות מניות',
    'הראל השתלמות מסלול מניות',
    'ילין לפידות קרן השתלמות מסלול מניות',
    'מור השתלמות - מניות'
]

gemel_clali = [
    'אנליסט קופת גמל להשקעה כללי',
    'הפניקס גמל להשקעה כללי',
    'מגדל גמל להשקעה כללי',
    'מיטב גמל להשקעה כללי',
    'הראל גמל להשקעה כללי',
    'מנורה מבטחים גמל להשקעה כללי',
    'ילין לפידות קופת גמל להשקעה מסלול כללי',
    'אלטשולר שחם חיסכון פלוס כללי',
    'כלל גמל לעתיד כללי',
    'מור גמל להשקעה- כללי'
]

gemel_stocks = [
    'אנליסט קופת גמל להשקעה מניות',
    'מיטב גמל להשקעה מניות',
    'מגדל גמל להשקעה מניות',
    'הפניקס גמל להשקעה מניות',
    'הראל גמל להשקעה מניות',
    'מנורה מבטחים גמל להשקעה מניות סחיר',
    'ילין לפידות קופת גמל להשקעה מסלול מניות',
    'אלטשולר שחם חיסכון פלוס מניות',
    'כלל גמל לעתיד מניות',
    'מור גמל להשקעה - מניות'
]

options = Options()
options.add_experimental_option('prefs', {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "profile.default_content_settings.popups": 0,
    "directory_upgrade": True
})

driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(1)

enter_button = driver.find_element(By.ID, 'knisa')
enter_button.click()
time.sleep(3)

load_table = driver.find_element(By.ID, 'cbDisplay')
export_to_excel_button = driver.find_element(By.ID, 'cbExcel')
yield_button = driver.find_element(By.ID, 'rbKupotDefault')
alpha_button = driver.find_element(By.ID, 'rbKupotAlpha')
text_entry = driver.find_element(By.ID, 'txtFilterKupot')
text_entry.clear()
selected_dropdown = Select(driver.find_element(By.ID, 'selSelectedKupot'))
remove_button = driver.find_element(By.ID, 'btnRemove')

kupot_kind_list = [(hishtalmut_clali, 'השתלמות כללי'), 
                   (hishtalmut_stocks, 'השתלמות מנייתי'),
                   (gemel_clali, 'גמל להשקעה כללי'),
                   (gemel_stocks, 'גמל להשקעה מנייתי')]
for group, subgroup in kupot_kind_list:
    yields_extractor(group, subgroup)

time.sleep(4) #just to see result
driver.quit()
   

