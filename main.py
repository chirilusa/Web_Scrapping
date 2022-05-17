from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# import os
import pandas as pd

browser = webdriver.Chrome(ChromeDriverManager().install())
dictionary = {}

for date in range(20, 28):
    browser.get(f"https://www.mai.gov.ro/informare-covid-19-grupul-de-comunicare-strategica-{date}-ianuarie-ora-13-00/")

    table = browser.find_element(by=By.XPATH, value='//table')
    rows = table.text.split('\n')[1:43]
    correct_split_rows = []

    for row in rows:
        row_data = row.split(' ')
        correct_split_rows.append([row_data[0]] + [''.join(row_data[1:len(row_data) - 3])] + row_data[-3:])

    rows = correct_split_rows
    header = []
    for column_index in range(5):
        header.append(browser.find_element(by=By.XPATH, value=f'//table//td[{column_index + 1}]').text)

    if len(dictionary) == 0:
        dictionary = {date: [] for date in header}

    for row in correct_split_rows:
        for column in range(len(header)):
            dictionary[header[column]].append(row[column])

print(dictionary)

# os.remove('Covid_Information.csv')
df = pd.DataFrame(dictionary)
df.to_csv('Covid_Information.csv')
browser.close()